"""Validate citation identity and answer structure; semantic support is judged later."""
from collections.abc import Awaitable, Callable
import re
from typing import Literal

from pydantic import BaseModel, Field


class CitedClaim(BaseModel):
    text: str = Field(description="One factual explanation or formula. Put bracket citations only in the citations list, not in this text.")
    citations: list[str] = Field(default_factory=list, description="Exact [source | location] labels returned by search.")


class AnswerDraft(BaseModel):
    status: Literal["supported", "partial", "unanswerable"]
    answer_claims: list[CitedClaim] = Field(default_factory=list, description="Supported answers to what was actually asked. Empty for unanswerable questions.")
    missing_information: str = Field(default="", description="Only identify missing company, period, figure or evidence. Do not place uncited factual background here.")
    general_background: list[CitedClaim] = Field(default_factory=list, description="Optional cited concepts, separate from the requested company-specific answer.")


CITATION = re.compile(r"\[([^\[\]\n|]+)\s*\|\s*([^\[\]\n|]+)\]")
BLOCKED_ANSWER = "I couldn't produce an answer with verified citations from the retrieved passages."


def canonical_citation(value):
    match = CITATION.fullmatch(value.strip())
    return f"[{match[1].strip()} | {match[2].strip()}]" if match else None


def retrieved_passages(trace):
    passages = {}
    for event in trace:
        if event["tool"] == "search" and event["status"] == "success":
            for hit in event["result"].get("results", []):
                passages[hit["id"]] = hit
    return list(passages.values())


def validate_draft(draft, trace):
    if draft is None:
        return ["No valid structured answer was produced"]
    issues = []
    if not any(event["tool"] == "search" and event["status"] == "success" for event in trace):
        issues.append("No successful search before the answer")
    allowed = {canonical_citation(hit["citation"]) for hit in retrieved_passages(trace)}
    if draft.status in {"partial", "unanswerable"} and not draft.missing_information.strip():
        issues.append("Missing-information statement required")
    if draft.status == "unanswerable" and draft.answer_claims:
        issues.append("An unanswerable question cannot contain requested-answer claims")
    if draft.status in {"supported", "partial"} and not draft.answer_claims:
        issues.append("Supported or partial answers require at least one cited answer claim")
    if draft.status == "supported" and draft.missing_information.strip():
        issues.append("An answer with missing evidence must be marked partial or unanswerable")
    for claim in draft.answer_claims + draft.general_background:
        if not claim.text.strip():
            issues.append("Empty claim")
        if not claim.citations:
            issues.append("Factual claim has no citation")
        for citation in claim.citations:
            if canonical_citation(citation) not in allowed or canonical_citation(citation) is None:
                issues.append(f"Citation was not returned by search: {citation}")
    texts = [draft.missing_information] + [claim.text for claim in draft.answer_claims + draft.general_background]
    for text in texts:
        for match in CITATION.finditer(text):
            if canonical_citation(match[0]) not in allowed:
                issues.append("Unrecognized citation embedded in answer text")
    return sorted(set(issues))


def render_answer(draft):
    def render(claim):
        citations = claim.citations + [match[0] for match in CITATION.finditer(claim.text)]
        text = CITATION.sub("", claim.text)
        text = re.sub(r"\(\s*[,;]?\s*\)", "", text)
        text = re.sub(r"(?:,\s*)+([.!?;:])", r"\1", text)
        text = re.sub(r"\s+([.,;:!?])", r"\1", text)
        text = re.sub(r"[ \t]{2,}", " ", text).strip()
        return text + " " + " ".join(dict.fromkeys(canonical_citation(c) for c in citations))
    paragraphs = []
    if draft.missing_information.strip():
        paragraphs.append(draft.missing_information.strip())
    paragraphs.extend(render(claim) for claim in draft.answer_claims)
    if draft.general_background:
        paragraphs.append("General background:\n" + "\n\n".join(render(claim) for claim in draft.general_background))
    return "\n\n".join(paragraphs)


async def guard_answer(draft, trace, repair: Callable[..., Awaitable[AnswerDraft]]):
    """At most one correction call, then a transparent, deterministic refusal."""
    issues = validate_draft(draft, trace)
    events, corrections = [], 0
    if issues:
        events.append({"attempt": 0, "issues": issues})
        corrections = 1
        try:
            draft = await repair(draft, issues)
            issues = validate_draft(draft, trace)
        except Exception as error:
            issues = [f"Correction failed: {type(error).__name__}"]
        events.append({"attempt": 1, "issues": issues})
    blocked = bool(issues)
    return {"answer": BLOCKED_ANSWER if blocked else render_answer(draft),
            "draft": draft.model_dump() if draft is not None else None,
            "guardrail_blocked": blocked, "guardrail_events": events,
            "correction_attempts": corrections}
