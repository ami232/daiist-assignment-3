"""LangChain RAG agent using *MCP* search and approval-gated add-document.

API: await ask(question) -> (answer, trace). CLI: python agent.py QUESTION
"""
from __future__ import annotations

import asyncio
import json
import os
import re
import sys
import time
from pathlib import Path

from api_key import load_api_key
from rag_core import CHAT_MODEL

ROOT = Path(__file__).resolve().parent

CITATION_PATTERN = re.compile(r'\[CITE:([0-9a-f]{20})\]')
ANY_CITATION_TAG = re.compile(r'\[CITE:[^\]]*\]')

REFUSAL_PATTERN = re.compile(
    r"\b(?:don't know|do not know|not covered|not in the (?:corpus|documentation)|insufficient evidence|cannot determine|can't determine|no evidence|does not specify)\b",
    re.I
)

SEARCH_LIMIT = 4

CANONICAL_REFUSAL = 'I do not know based on the indexed Python 3.13 documentation.'

LOOSE_CITATION = re.compile(r'\[\s*cite\s*:([^\]]*)\]', re.I)
ID_20 = re.compile(r'[0-9a-fA-F]{20}')


def normalize_citations(text: str) -> str:
    """Accept harmless format variants ([cite: id], [CITE:id1, id2]) by rewriting them into
    one [CITE:id] tag per id. Anything that is not purely ids stays untouched, so the
    guardrail still rejects it. Whether an id is real is checked later."""
    def fix(m):
        inner = m.group(1)
        ids = ID_20.findall(inner)
        leftover = re.sub(r'(?i)cite\s*:', '', ID_20.sub('', inner))
        if ids and not leftover.strip(' ,;'):
            return ' '.join(f'[CITE:{i.lower()}]' for i in ids)
        return m.group(0)
    return LOOSE_CITATION.sub(fix, text)

def extract_citations(message: str) -> list[str]:
    return list(dict.fromkeys(CITATION_PATTERN.findall(message)))


def is_refusal(message: str) -> bool:
    return bool(REFUSAL_PATTERN.search(message))


def validate_answer(answer: str, shown: set[str]) -> tuple[str, dict]:
    """Guardrail: do not emit uncited or fabricated citations as sourced answers."""
    cites = extract_citations(answer)

    malformed = [
        tag for tag in ANY_CITATION_TAG.findall(answer)
        if not CITATION_PATTERN.fullmatch(tag)
    ]

    invalid = sorted(set(cites) - shown)

    if malformed or invalid:
        invalid = sorted(set(invalid + malformed))
        return (
            'I do not know based on the retrieved corpus: the draft answer used invalid citations.',
            {'guardrail_fired': 'invalid_citations', 'invalid': invalid}
        )

    if not cites:
        if answer.strip().rstrip('.').casefold() == CANONICAL_REFUSAL.rstrip('.').casefold():
            return CANONICAL_REFUSAL, {
                'guardrail_fired': None,
                'invalid': []
            }

        return CANONICAL_REFUSAL, {
            'guardrail_fired': 'missing_citations',
            'invalid': []
        }

    return answer, {
        'guardrail_fired': None,
        'invalid': []
    }


def _approval(path: str, *, interactive: bool) -> bool:
    if not interactive or not sys.stdin.isatty():
        return False
    try:
        response = input(f'Allow add_document to ingest {path!r}? [yes/NO] ').strip().lower()
    except EOFError:
        return False
    return response == 'yes'


def _tool_text(result) -> str:
    return '\n'.join(getattr(part, 'text', '') for part in result.content).strip()


async def answer_with_session(session, question: str, *, interactive: bool = False) -> tuple[str, dict]:
    """Use one existing MCP session; helpful for 30+ evaluation questions."""
    from langchain.agents import create_agent
    from langchain_core.tools import tool
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langgraph.errors import GraphRecursionError

    load_api_key()  # also exports a .env-only key for langchain-google-genai
    start = time.perf_counter()
    events: list[dict] = []
    presented: set[str] = set()
    counts = {'search': 0, 'add_document': 0}

    @tool('search', description='Retrieve verbatim documentation passages with [CITE:id] evidence from the Python 3.13 corpus.')
    async def search_tool(query: str) -> str:
        """Search the reference index for evidence of a Python rule."""
        if counts['search'] >= SEARCH_LIMIT:
            events.append({'tool': 'search', 'query': query, 'blocked': 'call_limit'})
            return 'Search call limit reached. Answer only from previously returned passages or refuse.'
        counts['search'] += 1
        response = await session.call_tool('search', {'query': query})
        text = _tool_text(response)
        presented.update(extract_citations(text))
        events.append({'tool': 'search', 'query': query, 'citation_ids': extract_citations(text),
                       'characters': len(text), 'evidence_text': text, 'error': bool(response.is_error)})
        return text

    @tool('add_document', description='Add a user-authorized local file under incoming/ to the corpus; approval is mandatory.')
    async def add_document_tool(path: str) -> str:
        """Requires explicit terminal confirmation before indexing a file."""
        if not _approval(path, interactive=interactive):
            events.append({'tool': 'add_document', 'path': path, 'blocked': 'approval_denied'})
            return 'Permission denied. No file was indexed. Ask user to approve explicitly.'
        counts['add_document'] += 1
        response = await session.call_tool('add_document', {'path': path})
        events.append({'tool': 'add_document', 'path': path, 'error': bool(response.is_error)})
        return _tool_text(response)

    prompt = (ROOT / 'AGENTS.md').read_text(encoding='utf-8')
    model = ChatGoogleGenerativeAI(model=CHAT_MODEL, max_retries=6)
    graph = create_agent(model=model, tools=[search_tool, add_document_tool], system_prompt=prompt)
    agent_error = None
    try:
        result = await graph.ainvoke({'messages': [{'role': 'user', 'content': question}]},
                                     config={'recursion_limit': 20})
        messages = result['messages']
        final = messages[-1].content
    except GraphRecursionError:
        # The model kept calling tools instead of answering. Treat as no usable answer;
        # the guardrail below turns an empty draft into the standard refusal.
        agent_error = 'recursion_limit'
        messages, final = [], ''
    if isinstance(final, list):
        final = '\n'.join(part.get('text', '') for part in final if isinstance(part, dict))
    if not isinstance(final, str):
        final = str(final)
    raw_model_answer = final.strip()
    final, validation = validate_answer(normalize_citations(raw_model_answer), presented)
    usage = {'input_tokens': 0, 'output_tokens': 0}
    for m in messages:
        stat = getattr(m, 'usage_metadata', None) or {}
        usage['input_tokens'] += stat.get('input_tokens', 0) or 0
        usage['output_tokens'] += stat.get('output_tokens', 0) or 0
    return final, {'tools': events, 'raw_model_answer': raw_model_answer,
                   'citation_ids': extract_citations(final),
                   'shown_ids': sorted(presented), 'search_calls': counts['search'],
                   'add_calls': counts['add_document'], 'agent_error': agent_error, **validation,
                   'tokens': usage, 'seconds': round(time.perf_counter()-start, 3)}


async def ask(question: str, *, interactive: bool = False) -> tuple[str, dict]:
    """Run over actual MCP stdio transport, not an imported server shortcut."""
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
    load_api_key()
    params = StdioServerParameters(command=sys.executable, args=[str(ROOT / 'server.py')],
                                   cwd=str(ROOT))
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            return await answer_with_session(session, question, interactive=interactive)


def main() -> None:
    question = ' '.join(sys.argv[1:]).strip()
    if not question:
        raise SystemExit('Usage: python agent.py "Question about Python 3.13"')
    answer, trace = asyncio.run(ask(question, interactive=True))
    print(answer)
    if trace['guardrail_fired']:
        print(f"\n[Evidence guardrail: {trace['guardrail_fired']}]", file=sys.stderr)


if __name__ == '__main__':
    main()
