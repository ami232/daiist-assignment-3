"""
Assignment 3: evaluación (`uv run python main.py evaluate`).

Hace cinco cosas y lo guarda todo en eval/:

  1. RETRIEVAL   hit rate @1/@3/@5 de cada diseño (chunking x método x filtro) sobre las
                 preguntas con respuesta, y palabras que añade al prompt  -> retrieval.md/.csv
  2. AGENTE      ejecuta el agente (agent.Harness) sobre TODAS las preguntas -> answers.jsonl
  3. CÓDIGO      comprueba lo que el código puede comprobar: rechazos y citas válidas
  4. JUEZ LLM    puntúa correct/supported del resto con TU rúbrica (eval/rubric.md) y los
                 fragmentos recuperados como evidencia                    -> judge.jsonl
  5. RESUMEN     acuerdo con tus notas (human_labels.csv), fallos con causa sugerida,
                 coste por pregunta                    -> summary.md, results.csv, failures.csv

Es REANUDABLE: las respuestas y veredictos ya calculados se reutilizan (no gastan cuota)
mientras no cambies AGENTS.md, el modelo, el diseño elegido o la rúbrica. Para rehacer
todo: EVAL_FRESH=1 uv run python main.py evaluate

Solo la parte 1 (para elegir diseño sin gastar llamadas al modelo):
    uv run python evaluate.py --retrieval-only
"""

from __future__ import annotations

import asyncio
import csv
import hashlib
import json
import os
import re
import statistics
import sys
import time
from collections import Counter, defaultdict

import config
from retrieval import Retriever, citation_is_valid, normalize

EVAL = config.EVAL_DIR
QUESTIONS = EVAL / "questions.csv"
HUMAN = EVAL / "human_labels.csv"
RUBRIC = EVAL / "rubric.md"
ANSWERS = EVAL / "answers.jsonl"
JUDGE = EVAL / "judge.jsonl"
FRESH = os.environ.get("EVAL_FRESH") == "1"
KS = (1, 3, 5)


def log(*args) -> None:
    print(*args, flush=True)


def sha(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()[:12]


# ======================================================================================
# Preguntas y "qué cuenta como acierto" en retrieval
# ======================================================================================
def load_questions() -> list[dict]:
    with QUESTIONS.open(newline="", encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if (r.get("question") or "").strip()]
    for r in rows:
        r["kind"] = r["kind"].strip().lower()
        r["expected"] = parse_expected(r)
    return rows


PAGE_SPEC = re.compile(r"^\s*(p+\.?|p[áa]g(s|inas?)?\.?)?\s*(\d+)(\s*[-–]\s*(\d+))?\s*$", re.I)


def parse_expected(row: dict) -> list[dict]:
    """expected_source "a;b" + expected_location "14;22" -> [{doc, pages|section}, ...]"""
    docs = [d.strip() for d in (row.get("expected_source") or "").split(";") if d.strip()]
    locs = [l.strip() for l in (row.get("expected_location") or "").split(";") if l.strip()]
    if len(locs) == 1 and len(docs) > 1:
        locs = locs * len(docs)
    out = []
    for i, doc in enumerate(docs):
        loc = locs[i] if i < len(locs) else ""
        m = PAGE_SPEC.match(loc)
        if m:
            a = int(m.group(3))
            b = int(m.group(5) or a)
            out.append({"doc": doc, "pages": (a, b), "section": None})
        else:
            out.append({"doc": doc, "pages": None, "section": loc or None})
    return out


def matches(hit: dict, exp: dict) -> bool:
    """¿Este fragmento contiene el pasaje esperado? (mismo documento y página/apartado)."""
    if hit["doc_id"] != exp["doc"]:
        return False
    if exp["pages"]:
        a, b = exp["pages"]
        return hit["page_start"] <= b and a <= hit["page_end"]      # los rangos se solapan
    if exp["section"]:
        return normalize(exp["section"]) in normalize(hit.get("section") or "")
    return True


# ======================================================================================
# 1. Retrieval
# ======================================================================================
def evaluate_retrieval(questions: list[dict]) -> list[dict]:
    answerable = [q for q in questions if q["kind"] != "unanswerable" and q["expected"]]
    rows = []
    for design in config.CHUNK_DESIGNS:
        r = Retriever(design)
        if not r.ids:
            log(f"  (diseño {design}: colección vacía, me lo salto)")
            continue
        for method in config.SEARCH_METHODS:
            for use_filter in (False, True):
                firsts, full5, words = [], [], []
                for q in answerable:
                    hits, _ = r.search(q["question"], k=max(KS), method=method, auto_filter=use_filter)
                    ranks = [i for i, h in enumerate(hits, 1) if any(matches(h, e) for e in q["expected"])]
                    firsts.append(ranks[0] if ranks else None)
                    full5.append(all(any(matches(h, e) for h in hits) for e in q["expected"]))
                    words.append(sum(h["words"] for h in hits[:config.TOP_K]))
                multi = [ok for ok, q in zip(full5, answerable) if q["kind"] == "multi"]
                rows.append({
                    "design": design, "method": method, "tender_filter": "sí" if use_filter else "no",
                    **{f"hit@{k}": round(sum(1 for f in firsts if f and f <= k) / len(answerable), 3) for k in KS},
                    "multi_all@5": round(sum(multi) / len(multi), 3) if multi else "",
                    "words_in_prompt@5": round(statistics.mean(words)),
                    "chunks": len(r.ids),
                })
                log(f"  {design:9} {method:7} filtro={rows[-1]['tender_filter']:2}  "
                    + "  ".join(f"hit@{k}={rows[-1][f'hit@{k}']:.2f}" for k in KS))
    write_csv(EVAL / "retrieval.csv", rows)
    with (EVAL / "retrieval.md").open("w", encoding="utf-8") as f:
        f.write(f"# Retrieval ({len(answerable)} preguntas con respuesta)\n\n")
        f.write(md_table(rows))
        f.write("\n\nhit@k: la pregunta cuenta como acierto si algún fragmento esperado está entre los k primeros. "
                "multi_all@5: en preguntas `multi`, todos los pasajes esperados entre los 5 primeros. "
                "words_in_prompt@5: palabras que se añaden al prompt con TOP_K fragmentos.\n")
    return rows


# ======================================================================================
# 2. Agente sobre todas las preguntas (con caché)
# ======================================================================================
def run_signature() -> str:
    agents = (config.ROOT / "AGENTS.md").read_text(encoding="utf-8")
    return sha("|".join([agents, config.CHAT_MODEL, config.CHOSEN_DESIGN, config.CHOSEN_METHOD,
                         str(config.CHOSEN_TENDER_FILTER), str(config.TOP_K)]))


def read_jsonl(path) -> list[dict]:
    if not path.exists() or FRESH:
        return []
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def had_tool_error(rec: dict) -> bool:
    """Una respuesta en la que search falló por un error NUESTRO (no del modelo) no es
    representativa: se vuelve a calcular en la siguiente ejecución."""
    return any(step.get("error") or str(step.get("result", "")).startswith("Error executing tool")
               for step in rec.get("trace", []))


def lost_guardrail_text(rec: dict) -> bool:
    """Respuestas antiguas en las que saltó el guardarraíl sin guardar el texto bloqueado:
    se recalculan una vez para poder analizarlas (ver_respuesta.py)."""
    g = rec.get("guardrail", {})
    return bool(g.get("fired")) and "original_answer" not in g


async def run_agent_on_all(questions: list[dict]) -> dict[str, dict]:
    from agent import Harness

    signature = run_signature()
    cached = {r["id"]: r for r in read_jsonl(ANSWERS)
              if r.get("signature") == signature and not had_tool_error(r) and not lost_guardrail_text(r)}
    todo = [q for q in questions if not (q["id"] in cached and cached[q["id"]]["question"] == q["question"])]
    log(f"  {len(questions) - len(todo)} respuestas reutilizadas de answers.jsonl, {len(todo)} por calcular")
    if todo:
        # add_document nunca se aprueba durante la evaluación
        async with Harness(approve=lambda path: False) as h:
            for n, q in enumerate(todo, 1):
                try:
                    rec = await h.ask(q["question"])
                except Exception as e:  # noqa: BLE001
                    log(f"  ! {q['id']}: {type(e).__name__}: {str(e)[:200]}")
                    if "429" in str(e) or "quota" in str(e).lower() or "RESOURCE_EXHAUSTED" in str(e):
                        log("  ! Cuota del modelo agotada: guardo lo hecho. Repite `main.py evaluate` más tarde.")
                        break
                    continue
                rec.update(id=q["id"], signature=signature, model=config.CHAT_MODEL)
                cached[q["id"]] = rec
                with ANSWERS.open("w", encoding="utf-8") as f:   # reescribimos: siempre coherente
                    for r in cached.values():
                        f.write(json.dumps(r, ensure_ascii=False) + "\n")
                log(f"  [{n}/{len(todo)}] {q['id']} {rec['seconds']:.1f}s {rec['total_tokens']} tok "
                    f"{'RECHAZO' if rec['refusal'] else 'respuesta'}{' · guardarraíl' if rec['guardrail']['fired'] else ''}")
                time.sleep(1)   # respeta el límite de peticiones por minuto
    return cached


# ======================================================================================
# 3. Comprobaciones en código
# ======================================================================================
def code_checks(q: dict, rec: dict) -> dict:
    from retrieval import find_citations

    cites = find_citations(rec["answer"]) if not rec["refusal"] else []
    invalid = [f"[{d}, p. {p}]" for d, p in cites if not citation_is_valid(d, p, rec["retrieved"])]
    # Una pregunta multi solo cuenta como "pasaje recuperado" si se recuperaron TODOS sus pasajes
    # (antes bastaba uno, y q30 salía como "wrong answer from right passage" sin haber visto giss_ted).
    expected_retrieved = (all(any(matches(h, e) for h in rec["retrieved"]) for e in q["expected"])
                          if q["expected"] else None)
    expected_cited = (any(d == e["doc"] for d, _ in cites for e in q["expected"]) if q["expected"] else None)
    return {
        "refusal": rec["refusal"],
        "n_citations": len(cites),
        "invalid_citations": "; ".join(invalid),
        "citations_ok": (not invalid) and (rec["refusal"] or bool(cites)),
        "expected_retrieved": expected_retrieved,
        "expected_doc_cited": expected_cited,
        "correct_refusal": q["kind"] == "unanswerable" and rec["refusal"],
        "wrong_refusal": q["kind"] != "unanswerable" and rec["refusal"],
        "missed_refusal": q["kind"] == "unanswerable" and not rec["refusal"],
    }


# ======================================================================================
# 4. Juez LLM
# ======================================================================================
JUDGE_INSTRUCTIONS = """Eres un evaluador estricto. Sigue la rúbrica de arriba. Evalúa SOLO la respuesta
del agente frente a la respuesta de referencia y la evidencia. Devuelve:
- correct: 1 si la respuesta es correcta según la rúbrica, 0 si no.
- supported: 1 si TODAS sus afirmaciones aparecen en la evidencia, 0 si alguna no.
- reason: una o dos frases que justifiquen ambas notas."""


def judge_one(q: dict, rec: dict, rubric: str) -> dict:
    import httpx
    from google.genai import errors, types
    from pydantic import BaseModel

    from index import genai_client

    class Verdict(BaseModel):
        correct: int
        supported: int
        reason: str

    evidence = "\n\n".join(f"[{h['doc_id']}, p. {h['page_start']}] {h['text']}" for h in rec["retrieved"]) or "(ninguna)"
    prompt = (f"{rubric}\n\n{JUDGE_INSTRUCTIONS}\n\n## Caso\nTipo de pregunta: {q['kind']}\n"
              f"Pregunta: {q['question']}\nRespuesta de referencia: {q['reference_answer']}\n\n"
              f"## Evidencia recuperada por el agente\n{evidence}\n\n## Respuesta del agente\n{rec['answer']}")
    for attempt in range(5):
        try:
            resp = genai_client().models.generate_content(
                model=config.JUDGE_MODEL, contents=prompt,
                config=types.GenerateContentConfig(temperature=0, response_mime_type="application/json",
                                                   response_schema=Verdict),
            )
            v = resp.parsed or Verdict.model_validate_json(resp.text)
            usage = resp.usage_metadata
            return {"correct": int(v.correct), "supported": int(v.supported), "reason": v.reason,
                    "judge_tokens": getattr(usage, "total_token_count", 0) or 0}
        except errors.ClientError as e:
            if e.code != 429 or "perday" in str(e).lower().replace(" ", "").replace("_", ""):
                raise
            wait = 15 * (attempt + 1)
            log(f"    juez: límite de peticiones por minuto de Gemini (429); espero {wait}s ...")
            time.sleep(wait)
        except errors.ServerError as e:
            # 500/503: el modelo está saturado ("high demand"). Suele pasar en segundos.
            wait = 20 * (attempt + 1)
            log(f"    juez: Gemini saturado ({e.code}); reintento en {wait}s ...")
            time.sleep(wait)
        except httpx.TimeoutException:
            log("    juez: Gemini tarda más de 2 minutos en responder; reintento ...")
    raise RuntimeError("El juez sigue sin responder tras varios reintentos (429/503)")


def run_judge(questions: list[dict], answers: dict) -> dict[str, dict]:
    rubric = RUBRIC.read_text(encoding="utf-8") if RUBRIC.exists() else ""
    if not rubric.strip() or "TU CRITERIO" in rubric:
        log("  AVISO: eval/rubric.md sigue siendo la plantilla. Escribe tu rúbrica antes de entregar.")
    key_base = sha(rubric + config.JUDGE_MODEL)
    cached = {r["key"]: r for r in read_jsonl(JUDGE)}
    out = {}
    for q in questions:
        rec = answers.get(q["id"])
        if not rec or rec["refusal"]:
            continue       # los rechazos los puntúa el código, no el juez
        key = f"{q['id']}|{key_base}|{sha(rec['answer'])}"
        if key in cached:
            out[q["id"]] = cached[key]
            continue
        try:
            v = judge_one(q, rec, rubric)
        except Exception as e:  # noqa: BLE001
            log(f"  ! juez {q['id']}: {type(e).__name__}: {str(e)[:160]}. Paro el juez; repite más tarde.")
            break
        v.update(key=key, id=q["id"], judge_model=config.JUDGE_MODEL)
        cached[key] = out[q["id"]] = v
        with JUDGE.open("w", encoding="utf-8") as f:
            for r in cached.values():
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        log(f"  juez {q['id']}: correct={v['correct']} supported={v['supported']}")
        time.sleep(1)
    return out


# ======================================================================================
# 5. Acuerdo con tus notas, fallos y resumen
# ======================================================================================
def kappa(a: list[int], b: list[int]) -> float | None:
    if not a:
        return None
    po = sum(x == y for x, y in zip(a, b)) / len(a)
    pa, pb = sum(a) / len(a), sum(b) / len(b)
    pe = pa * pb + (1 - pa) * (1 - pb)
    return 1.0 if pe == 1 else round((po - pe) / (1 - pe), 3)


def suggest_cause(q: dict, checks: dict, final: dict) -> str:
    """Causa SUGERIDA. La definitiva (y 'bad test question') la decides tú en failures.csv."""
    if checks["wrong_refusal"]:
        return "wrong refusal" if checks["expected_retrieved"] else "retrieval miss"
    if checks["missed_refusal"]:
        return "unsupported claim"
    if not final["correct"]:
        return "wrong answer from right passage" if checks["expected_retrieved"] else "retrieval miss"
    if not final["supported"]:
        return "unsupported claim"
    return ""


def write_csv(path, rows: list[dict]) -> None:
    if not rows:
        return
    keys = list(dict.fromkeys(k for r in rows for k in r))
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        w.writerows(rows)


def md_table(rows: list[dict], cols: list[str] | None = None) -> str:
    if not rows:
        return "(sin datos)\n"
    cols = cols or list(rows[0])
    lines = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    lines += ["| " + " | ".join(str(r.get(c, "")) for c in cols) + " |" for r in rows]
    return "\n".join(lines) + "\n"


def pct(n: int, d: int) -> str:
    return f"{n}/{d} ({100 * n / d:.0f} %)" if d else "0/0"


def main() -> None:
    if not QUESTIONS.exists():
        raise SystemExit("Falta eval/questions.csv")
    questions = load_questions()
    log(f"{len(questions)} preguntas: {dict(Counter(q['kind'] for q in questions))}")

    log("\n1/5 Retrieval: hit rate por diseño ...")
    retrieval_rows = evaluate_retrieval(questions)
    if "--retrieval-only" in sys.argv:
        log("\nSolo retrieval (--retrieval-only): mira eval/retrieval.md y elige el diseño en config.py.")
        return

    log(f"\n2/5 Agente ({config.CHAT_MODEL}, diseño {config.CHOSEN_DESIGN}/{config.CHOSEN_METHOD}) sobre todas las preguntas ...")
    answers = asyncio.run(run_agent_on_all(questions))

    log("\n3/5 Comprobaciones en código ...")
    checks = {q["id"]: code_checks(q, answers[q["id"]]) for q in questions if q["id"] in answers}

    log("\n4/5 Juez LLM ...")
    verdicts = run_judge(questions, answers)

    log("\n5/5 Resumen ...")
    results, to_label, failures = [], [], []
    for q in questions:
        rec, c = answers.get(q["id"]), checks.get(q["id"])
        if not rec:
            continue
        if rec["refusal"]:     # lo decide el código
            final = {"correct": int(q["kind"] == "unanswerable"), "supported": 1, "graded_by": "código"}
        elif q["id"] in verdicts:
            v = verdicts[q["id"]]
            final = {"correct": v["correct"], "supported": int(v["supported"] and c["citations_ok"]),
                     "graded_by": "juez"}
        else:
            final = {"correct": "", "supported": "", "graded_by": "pendiente"}
        cause = suggest_cause(q, c, final) if final["graded_by"] != "pendiente" else ""
        results.append({
            "id": q["id"], "kind": q["kind"], "question": q["question"], "answer": rec["answer"],
            "reference_answer": q["reference_answer"], **final, **c,
            "judge_reason": verdicts.get(q["id"], {}).get("reason", ""),
            "guardrail_fired": rec["guardrail"]["fired"], "guardrail_blocked": rec["guardrail"]["blocked"],
            "tool_calls": rec["tool_calls"], "input_tokens": rec["input_tokens"],
            "output_tokens": rec["output_tokens"], "total_tokens": rec["total_tokens"], "seconds": rec["seconds"],
            "suggested_cause": cause,
        })
        to_label.append({"id": q["id"], "kind": q["kind"], "question": q["question"],
                         "reference_answer": q["reference_answer"], "answer": rec["answer"],
                         "evidence": " || ".join(f"[{h['doc_id']}, p. {h['page_start']}] {h['text'][:400]}"
                                                 for h in rec["retrieved"])})
        if cause:
            failures.append({"id": q["id"], "kind": q["kind"], "question": q["question"],
                             "suggested_cause": cause, "your_cause": "", "notes": ""})

    write_csv(EVAL / "results.csv", results)
    write_csv(EVAL / "to_label.csv", to_label)       # para tus notas a ciegas (sin veredictos)
    fail_path = EVAL / "failures.csv"
    if fail_path.exists():                            # no pisamos lo que ya hayas escrito
        with fail_path.open(newline="", encoding="utf-8") as f:
            mine = {r["id"]: r for r in csv.DictReader(f)}
        for r in failures:
            if r["id"] in mine:
                r["your_cause"], r["notes"] = mine[r["id"]].get("your_cause", ""), mine[r["id"]].get("notes", "")
    write_csv(fail_path, failures)

    # --- acuerdo humano-juez ---------------------------------------------------------
    agreement = {}
    if HUMAN.exists():
        with HUMAN.open(newline="", encoding="utf-8") as f:
            human = {r["id"]: r for r in csv.DictReader(f) if (r.get("id") or "").strip()}
        both = [r for r in results if r["id"] in human and r["graded_by"] != "pendiente"]
        for field in ("correct", "supported"):
            a = [int(human[r["id"]][field]) for r in both]
            b = [int(r[field]) for r in both]
            agreement[field] = {"n": len(both), "agreement": round(sum(x == y for x, y in zip(a, b)) / len(both), 3) if both else None,
                                "kappa": kappa(a, b)}
        agreement["disagreements"] = [
            {"id": r["id"], "human": f"{human[r['id']]['correct']}/{human[r['id']]['supported']}",
             "sistema": f"{r['correct']}/{r['supported']}", "graded_by": r["graded_by"], "judge_reason": r["judge_reason"]}
            for r in both if int(human[r["id"]]["correct"]) != int(r["correct"]) or int(human[r["id"]]["supported"]) != int(r["supported"])
        ]

    # --- números del resumen -----------------------------------------------------------
    graded = [r for r in results if r["graded_by"] != "pendiente"]
    by_kind = defaultdict(list)
    for r in graded:
        by_kind[r["kind"]].append(r)
    answered = [r for r in graded if not r["refusal"]]
    unans = [r for r in graded if r["kind"] == "unanswerable"]
    ans = [r for r in graded if r["kind"] != "unanswerable"]
    tokens = [r["total_tokens"] for r in results]
    secs = [r["seconds"] for r in results]
    summary = {
        "questions": len(questions), "answered_by_agent": len(results), "graded": len(graded),
        "correct": sum(int(r["correct"]) for r in graded),
        "correct_by_kind": {k: sum(int(r["correct"]) for r in v) for k, v in by_kind.items()},
        "n_by_kind": {k: len(v) for k, v in by_kind.items()},
        "unsupported_answers": sum(1 for r in answered if not int(r["supported"])),
        "answered": len(answered),
        "correct_refusals": sum(r["correct_refusal"] for r in unans), "unanswerable": len(unans),
        "wrong_refusals": sum(r["wrong_refusal"] for r in ans), "answerable": len(ans),
        "missed_refusals": sum(r["missed_refusal"] for r in unans),
        "invalid_citation_answers": sum(1 for r in results if r["invalid_citations"]),
        "guardrail_fired": sum(r["guardrail_fired"] for r in results),
        "guardrail_blocked": sum(r["guardrail_blocked"] for r in results),
        "tokens_mean": round(statistics.mean(tokens)) if tokens else None,
        "tokens_median": round(statistics.median(tokens)) if tokens else None,
        "seconds_mean": round(statistics.mean(secs), 1) if secs else None,
        "seconds_median": round(statistics.median(secs), 1) if secs else None,
        "seconds_max": max(secs) if secs else None,
        "tool_calls_mean": round(statistics.mean(r["tool_calls"] for r in results), 2) if results else None,
        "failures_by_suggested_cause": dict(Counter(f["suggested_cause"] for f in failures)),
        "human_judge_agreement": agreement,
        "chat_model": config.CHAT_MODEL, "judge_model": config.JUDGE_MODEL,
        "design": f"{config.CHOSEN_DESIGN} / {config.CHOSEN_METHOD} / filtro={config.CHOSEN_TENDER_FILTER} / k={config.TOP_K}",
    }
    (EVAL / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    s = summary
    md = ["# Resumen de la evaluación\n",
          f"Agente: `{s['chat_model']}` · juez: `{s['judge_model']}` · diseño: `{s['design']}`\n",
          f"## Resultados ({s['graded']} de {s['questions']} preguntas puntuadas)\n",
          f"- **Correctas:** {pct(s['correct'], s['graded'])}  "
          + " · ".join(f"{k}: {pct(s['correct_by_kind'][k], s['n_by_kind'][k])}" for k in sorted(s['n_by_kind'])),
          f"- **Respuestas con afirmaciones no respaldadas:** {pct(s['unsupported_answers'], s['answered'])} de las respuestas que no son rechazo",
          f"- **Rechazos correctos:** {pct(s['correct_refusals'], s['unanswerable'])} de las preguntas sin respuesta",
          f"- **Rechazos indebidos (wrong refusals):** {pct(s['wrong_refusals'], s['answerable'])} de las preguntas con respuesta",
          f"- **Rechazos que faltaron** (contestó una pregunta sin respuesta): {s['missed_refusals']}",
          f"- **Citas inválidas:** {s['invalid_citation_answers']} respuestas · guardarraíl de citas: "
          f"saltó {s['guardrail_fired']} veces, bloqueó {s['guardrail_blocked']}",
          "\n## Coste por pregunta\n",
          f"- Tokens del agente: media {s['tokens_mean']}, mediana {s['tokens_median']}",
          f"- Segundos: media {s['seconds_mean']}, mediana {s['seconds_median']}, máximo {s['seconds_max']}",
          f"- Llamadas a herramientas: media {s['tool_calls_mean']}",
          "\n## Acuerdo con tus notas (human_labels.csv)\n"]
    if agreement:
        for field in ("correct", "supported"):
            a = agreement[field]
            md.append(f"- {field}: acuerdo {a['agreement']} en {a['n']} respuestas (kappa de Cohen {a['kappa']})")
        md.append("\nDesacuerdos (humano vs. sistema, correct/supported):\n")
        md.append(md_table(agreement["disagreements"]) if agreement["disagreements"] else "(ninguno)\n")
    else:
        md.append("(eval/human_labels.csv vacío: puntúa al menos 20 respuestas de eval/to_label.csv)\n")
    md.append("\n## Fallos por causa sugerida (revísalos en failures.csv)\n")
    md.append(md_table([{"causa": k, "n": v} for k, v in s["failures_by_suggested_cause"].items()]))
    md.append("\n## Retrieval\n")
    md.append(md_table(retrieval_rows))
    (EVAL / "summary.md").write_text("\n".join(md), encoding="utf-8")
    log("\n".join(md[:12]))
    log("\nGuardado en eval/: summary.md, summary.json, results.csv, failures.csv, to_label.csv, retrieval.md")
    if len(results) < len(questions):
        log(f"\nAVISO: faltan {len(questions) - len(results)} respuestas (cuota). Repite `main.py evaluate` más tarde.")


if __name__ == "__main__":
    main()
