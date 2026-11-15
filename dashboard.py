"""
Build dashboard.html from the evaluation results in eval/.

    uv run python dashboard.py

The page is a single self-contained HTML file (no internet needed): key
numbers, three charts (retrieval designs, my grades vs the AI judge, failures
by cause) and a filterable table of all questions with the full answers and
the passages the assistant saw. Re-run it after evaluate.py to refresh it.
"""

from __future__ import annotations

import csv
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EVAL = ROOT / "eval"
OUT = ROOT / "dashboard.html"

# Failure causes from my own grading (REPORT.md, "Failures in the answers").
FAILURE_CAUSES = [
    ("Adds advice or facts not in the passages", 8, "u01, u03, u04, u06, u07, m01, m02, m04"),
    ("Concludes more than the passage says", 2, "q03, q16"),
    ("Misleading first sentence", 1, "m03"),
    ("Doesn't finish the calculation", 1, "m04"),
    ("Cites a page it never saw", 1, "q12 (caught by the citation check)"),
]
COST_PER_QUESTION = 0.0035  # USD; third-party price lists, Nov 2026 (REPORT.md, Decision)


def esc(text) -> str:
    return html.escape(str(text), quote=True)


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def read_csv(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as f:
        return [r for r in csv.DictReader(f) if (r.get("id") or "").strip()]


# --------------------------------------------------------------------------- charts (inline SVG)

def column_chart(title: str, subtitle: str, categories: list[str], series: list[tuple[str, str, list[float], list[str]]],
                 y_max: float = 100, y_suffix: str = "%") -> str:
    """Grouped columns. series = [(name, css var, values, tooltip per value)]."""
    w, h = 340, 220  # drawn close to its on-screen size so 12px text stays 12px
    left, right, top, bottom = 40, 8, 18, 30
    plot_w, plot_h = w - left - right, h - top - bottom
    bar_w, gap = 24, 2
    group_w = len(series) * bar_w + (len(series) - 1) * gap
    band = plot_w / len(categories)

    def y(v):
        return top + plot_h * (1 - v / y_max)

    parts = [f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="{esc(title)}">']
    for tick in range(0, int(y_max) + 1, int(y_max // 4)):
        ty = y(tick)
        parts.append(f'<line class="grid" x1="{left}" x2="{w - right}" y1="{ty:.1f}" y2="{ty:.1f}"/>')
        parts.append(f'<text class="tick" x="{left - 8}" y="{ty + 4:.1f}" text-anchor="end">{tick}{y_suffix}</text>')
    parts.append(f'<line class="axis" x1="{left}" x2="{w - right}" y1="{top + plot_h}" y2="{top + plot_h}"/>')
    for ci, cat in enumerate(categories):
        gx = left + band * ci + (band - group_w) / 2
        parts.append(f'<text class="tick cat" x="{left + band * ci + band / 2:.1f}" y="{h - 10}" text-anchor="middle">{esc(cat)}</text>')
        for si, (name, color, values, tips) in enumerate(series):
            v = values[ci]
            x0 = gx + si * (bar_w + gap)
            y0, base, r = y(v), top + plot_h, 4
            r = min(r, max(0, base - y0))
            path = (f"M{x0:.1f},{base:.1f} V{y0 + r:.1f} Q{x0:.1f},{y0:.1f} {x0 + r:.1f},{y0:.1f} "
                    f"H{x0 + bar_w - r:.1f} Q{x0 + bar_w:.1f},{y0:.1f} {x0 + bar_w:.1f},{y0 + r:.1f} V{base:.1f} Z")
            tip = esc(f"{name} · {cat}: {tips[ci]}")
            # Invisible wider hit target for the tooltip, then the mark.
            parts.append(f'<rect class="hit" x="{x0 - 2:.1f}" y="{top}" width="{bar_w + 4}" height="{plot_h}" '
                         f'data-tip="{tip}" tabindex="0"/>')
            parts.append(f'<path d="{path}" fill="var({color})" pointer-events="none"/>')
            parts.append(f'<text class="value" x="{x0 + bar_w / 2:.1f}" y="{y0 - 6:.1f}" text-anchor="middle">{tips[ci].split(" ")[0]}</text>')
    parts.append("</svg>")
    legend = "".join(f'<span class="key"><span class="swatch" style="background:var({c})"></span>{esc(n)}</span>'
                     for n, c, _, _ in series)
    return (f'<section class="card chart"><h2>{esc(title)}</h2><p class="sub">{esc(subtitle)}</p>'
            f'<div class="legend">{legend}</div>{"".join(parts)}</section>')


def bar_list(title: str, subtitle: str, rows: list[tuple[str, int, str]]) -> str:
    """Horizontal bars for one series (no legend needed), value at the tip."""
    top = max(v for _, v, _ in rows)
    items = []
    for label, value, detail in rows:
        pct = 100 * value / top
        items.append(
            f'<div class="hbar" data-tip="{esc(f"{label}: {value} answer(s): {detail}")}" tabindex="0">'
            f'<div class="hbar-label">{esc(label)}</div>'
            f'<div class="hbar-track"><div class="hbar-fill" style="width:{pct:.0f}%"></div>'
            f'<span class="hbar-value">{value}</span></div></div>')
    return (f'<section class="card chart"><h2>{esc(title)}</h2><p class="sub">{esc(subtitle)}</p>'
            f'{"".join(items)}</section>')


# --------------------------------------------------------------------------- page

def build() -> str:
    summary = json.loads((EVAL / "summary.json").read_text(encoding="utf-8"))
    retrieval = json.loads((EVAL / "retrieval_summary.json").read_text(encoding="utf-8"))
    answers = {r["id"]: r for r in read_jsonl(EVAL / "agent_answers.jsonl")}
    # Re-run the current citation check: the saved results may predate fixes to it.
    from agent import Passage, check_citations
    for a in answers.values():
        a["citation_check"] = check_citations(a["answer"], [Passage(**p) for p in a["passages"]])
    judge = {r["id"]: r for r in read_jsonl(EVAL / "judge.jsonl")}
    human = {r["id"]: r for r in read_csv(EVAL / "human_labels.csv")}
    questions = read_csv(EVAL / "questions.csv")

    checks, results = summary["code_checks"], summary["results"]
    n_answerable = results["answerable_judged"]
    n_human = len(human)
    human_correct = sum(int(r["correct"]) for r in human.values())
    human_supported = sum(int(r["supported"]) for r in human.values())
    judge_full = sum(1 for v in judge.values() if v["correct"] and v["supported"])
    hit5 = round(retrieval["structure"]["hit@5"] * retrieval["structure"]["questions"])

    tiles = [
        ("Correct refusals", f'{results["correct_refusals"]} / {results["unanswerable"]}', "unanswerable → “I don't know” (code check)"),
        ("Wrong refusals", f'{results["wrong_refusals"]} / {n_answerable}', "answerable → “I don't know” (code check)"),
        ("Supported, my grading", f"{human_supported} / {n_human}", "every claim in the passages"),
        ("Full marks from the AI judge", f"{judge_full} / {len(judge)}", "too generous: see the chart below"),
        ("Right chunk in first 5", f"{hit5} / {retrieval['structure']['questions']}", "structure design"),
        ("Time per question", f'{checks["mean_seconds"]:.0f} s', f'{checks["mean_model_calls"]:.0f} AI calls, {checks["mean_searches"]} searches'),
        ("Cost per question", f"≈ ${COST_PER_QUESTION}", "paid plan estimate; 0 € on the free plan"),
    ]
    tiles_html = "".join(f'<div class="tile"><div class="tile-label">{esc(l)}</div>'
                         f'<div class="tile-value">{esc(v)}</div><div class="tile-note">{esc(n)}</div></div>'
                         for l, v, n in tiles)

    def pct(design, k):
        return round(retrieval[design][f"hit@{k}"] * 100)

    def count(design, k):
        return round(retrieval[design][f"hit@{k}"] * retrieval[design]["questions"])

    n_ret = retrieval["structure"]["questions"]
    chart_retrieval = column_chart(
        "Retrieval: fixed vs structure chunks",
        f"How often the right chunk is among the first k results ({n_ret} answerable questions)",
        ["1st result", "First 3", "First 5"],
        [("Structure", "--series-1", [pct("structure", k) for k in (1, 3, 5)],
          [f"{pct('structure', k)}% ({count('structure', k)}/{n_ret})" for k in (1, 3, 5)]),
         ("Fixed", "--series-2", [pct("fixed", k) for k in (1, 3, 5)],
          [f"{pct('fixed', k)}% ({count('fixed', k)}/{n_ret})" for k in (1, 3, 5)])],
    )
    judge_on_mine = [judge[i] for i in human]
    jc, js = sum(v["correct"] for v in judge_on_mine), sum(v["supported"] for v in judge_on_mine)
    chart_judge = column_chart(
        "My grades vs the AI judge",
        f"Share of the same {n_human} answers graded 1 (correct / every claim supported)",
        ["Correct", "Supported"],
        [("Me", "--series-1", [100 * human_correct / n_human, 100 * human_supported / n_human],
          [f"{100 * human_correct / n_human:.0f}% ({human_correct}/{n_human})", f"{100 * human_supported / n_human:.0f}% ({human_supported}/{n_human})"]),
         ("AI judge", "--series-2", [100 * jc / n_human, 100 * js / n_human],
          [f"{100 * jc / n_human:.0f}% ({jc}/{n_human})", f"{100 * js / n_human:.0f}% ({js}/{n_human})"])],
    )
    chart_failures = bar_list("Failures by cause", f"From my grading of {n_human} answers and the citation check", FAILURE_CAUSES)

    # Table data for the client-side filters.
    rows = []
    for q in questions:
        a = answers.get(q["id"], {})
        h, j = human.get(q["id"]), judge.get(q["id"], {})
        spanish = any(c in q["question"] for c in "¿¡ñáéíóú")
        disagree = bool(h) and (int(h["correct"]) != j.get("correct") or int(h["supported"]) != j.get("supported"))
        rows.append({
            "id": q["id"], "kind": q["kind"], "lang": "Spanish" if spanish else "English",
            "question": q["question"], "reference": q["reference_answer"],
            "expected": f'{q["expected_source"]} {q["expected_location"]}'.strip() or "—",
            "answer": a.get("answer", ""), "seconds": a.get("seconds"),
            "searches": [c["args"].get("query") for c in a.get("tool_calls", []) if c["tool"] == "search"],
            "cited_check": "fired" if a.get("citation_check", {}).get("fired") else "ok",
            "me": f'{h["correct"]}/{h["supported"]}' if h else "", "me_note": (h or {}).get("notes", ""),
            "judge": f'{j.get("correct", "")}/{j.get("supported", "")}', "judge_reason": j.get("reason", ""),
            "disagree": disagree,
            "passages": [{"title": p["title"], "location": p["location"], "text": p["text"]} for p in a.get("passages", [])],
        })

    data_json = json.dumps(rows, ensure_ascii=False).replace("</", "<\\/")
    return TEMPLATE.replace("{{TILES}}", tiles_html) \
        .replace("{{CHARTS}}", chart_retrieval + chart_judge + chart_failures) \
        .replace("{{N}}", str(len(rows))).replace("{{DATA}}", data_json)


TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Erasmus+ Assistant Dashboard</title>
<style>
:root {
  color-scheme: light;
  --page: #f9f9f7; --surface-1: #fcfcfb; --text-primary: #0b0b0b; --text-secondary: #52514e;
  --muted: #898781; --grid: #e1e0d9; --axis: #c3c2b7; --border: rgba(11,11,11,0.10);
  --series-1: #2a78d6; --series-2: #eb6834; --wash: rgba(42,120,214,0.08); --critical: #d03b3b;
}
@media (prefers-color-scheme: dark) {
  :root:where(:not([data-theme="light"])) {
    color-scheme: dark;
    --page: #0d0d0d; --surface-1: #1a1a19; --text-primary: #f0efec; --text-secondary: #c3c2b7;
    --grid: #2c2c2a; --axis: #383835; --border: rgba(255,255,255,0.10);
    --series-1: #3987e5; --series-2: #d95926; --wash: rgba(57,135,229,0.12);
  }
}
:root[data-theme="dark"] {
  color-scheme: dark;
  --page: #0d0d0d; --surface-1: #1a1a19; --text-primary: #f0efec; --text-secondary: #c3c2b7;
  --grid: #2c2c2a; --axis: #383835; --border: rgba(255,255,255,0.10);
  --series-1: #3987e5; --series-2: #d95926; --wash: rgba(57,135,229,0.12);
}
* { box-sizing: border-box; }
body { margin: 0; background: var(--page); color: var(--text-primary);
       font: 15px/1.5 system-ui, -apple-system, "Segoe UI", sans-serif; }
main { max-width: 1120px; margin: 0 auto; padding: 24px 16px 48px; }
header h1 { font-size: 26px; margin: 0 0 4px; }
header p { margin: 0; color: var(--text-secondary); }
.card { background: var(--surface-1); border: 1px solid var(--border); border-radius: 12px; padding: 16px; }
.tiles { display: grid; grid-template-columns: repeat(auto-fit, minmax(128px, 1fr)); gap: 10px; margin: 20px 0; }
.tile { background: var(--surface-1); border: 1px solid var(--border); border-radius: 12px; padding: 14px; }
.tile-label { font-size: 13px; color: var(--text-secondary); }
.tile-value { font-size: 26px; font-weight: 600; margin: 2px 0; }
.tile-note { font-size: 12px; color: var(--muted); }
.charts { display: grid; grid-template-columns: repeat(auto-fit, minmax(min(320px, 100%), 1fr)); gap: 12px; }
.chart h2 { font-size: 16px; margin: 0; }
.chart .sub { margin: 2px 0 8px; font-size: 13px; color: var(--text-secondary); }
.legend { display: flex; gap: 16px; font-size: 13px; color: var(--text-secondary); margin-bottom: 4px; }
.key { display: inline-flex; align-items: center; gap: 6px; }
.swatch { width: 10px; height: 10px; border-radius: 3px; display: inline-block; }
svg { width: 100%; height: auto; display: block; overflow: visible; }
svg .grid { stroke: var(--grid); stroke-width: 1; }
svg .axis { stroke: var(--axis); stroke-width: 1; }
svg .tick { fill: var(--muted); font-size: 12px; font-variant-numeric: tabular-nums; }
svg .cat { fill: var(--text-secondary); font-size: 13px; }
svg .value { fill: var(--text-primary); font-size: 10.5px; font-weight: 600; }
svg .hit { fill: transparent; cursor: default; }
svg .hit:focus { outline: none; fill: var(--wash); }
.hbar { display: grid; grid-template-columns: minmax(120px, 44%) 1fr; gap: 10px; align-items: center; padding: 6px 0; }
.hbar:focus { outline: 2px solid var(--series-1); outline-offset: 2px; border-radius: 4px; }
.hbar-label { font-size: 13px; color: var(--text-secondary); }
.hbar-track { display: flex; align-items: center; gap: 8px; }
.hbar-fill { height: 18px; background: var(--series-1); border-radius: 0 4px 4px 0; min-width: 4px; }
.hbar-value { font-size: 13px; font-weight: 600; font-variant-numeric: tabular-nums; }
#tip { position: fixed; pointer-events: none; background: var(--text-primary); color: var(--surface-1);
       font-size: 12px; padding: 6px 8px; border-radius: 6px; max-width: 280px; opacity: 0; transition: opacity .1s; z-index: 10; }
.table-card { margin-top: 12px; }
.table-card h2 { font-size: 16px; margin: 0 0 8px; }
.filters { display: flex; flex-wrap: wrap; gap: 8px 16px; align-items: center; margin-bottom: 10px; font-size: 13px; }
.filters select, .filters input[type=search] { font: inherit; padding: 4px 8px; border-radius: 6px;
  border: 1px solid var(--border); background: var(--surface-1); color: var(--text-primary); }
.table-wrap { overflow-x: auto; }
table { width: 100%; border-collapse: collapse; font-size: 13px; }
th { text-align: left; color: var(--text-secondary); font-weight: 600; border-bottom: 1px solid var(--axis); padding: 6px; white-space: nowrap; }
td { border-bottom: 1px solid var(--grid); padding: 6px; vertical-align: top; }
td.num { font-variant-numeric: tabular-nums; white-space: nowrap; }
tr.row { cursor: pointer; }
tr.row:hover, tr.row:focus { background: var(--wash); outline: none; }
.badge { display: inline-block; padding: 0 6px; border-radius: 10px; border: 1px solid var(--border); font-size: 12px; white-space: nowrap; }
.badge.warn::before { content: "⚠ "; color: var(--critical); }
.detail td { background: var(--page); }
.detail h3 { font-size: 13px; margin: 10px 0 4px; color: var(--text-secondary); }
.answer { white-space: pre-wrap; margin: 0; font: inherit; }
details { margin: 4px 0; }
summary { cursor: pointer; color: var(--text-secondary); }
.passage { white-space: pre-wrap; font-size: 12px; color: var(--text-secondary); margin: 4px 0 8px 14px; }
footer { margin-top: 20px; font-size: 12px; color: var(--muted); }
</style>
</head>
<body>
<main>
<header>
  <h1>Erasmus+ grant assistant: evaluation dashboard</h1>
  <p>RAG assistant over four European Commission documents, evaluated on {{N}} test questions. Hover or tab to any bar for details; click a table row to read the full answer.</p>
</header>
<div class="tiles">{{TILES}}</div>
<div class="charts">{{CHARTS}}</div>
<section class="card table-card">
  <h2>All questions</h2>
  <div class="filters">
    <label>Kind <select id="f-kind"><option value="">All</option><option>single</option><option>multi</option><option>unanswerable</option></select></label>
    <label>Language <select id="f-lang"><option value="">All</option><option>English</option><option>Spanish</option></select></label>
    <label><input type="checkbox" id="f-graded"> Graded by me</label>
    <label><input type="checkbox" id="f-disagree"> Me and the judge disagree</label>
    <label><input type="checkbox" id="f-fired"> Citation check fired</label>
    <input type="search" id="f-text" placeholder="Search questions…" aria-label="Search questions">
    <span id="f-count"></span>
  </div>
  <div class="table-wrap"><table>
    <thead><tr><th>ID</th><th>Kind</th><th>Language</th><th>Question</th><th>Me (c/s)</th><th>Judge (c/s)</th><th>Citation check</th><th>Time</th></tr></thead>
    <tbody id="rows"></tbody>
  </table></div>
</section>
<footer>Generated by dashboard.py from eval/. “c/s” = correct / supported (1 = yes, 0 = no). Charts use the four EU documents only; the SEPIE test document is not part of the index.</footer>
</main>
<div id="tip" role="tooltip"></div>
<script>
const DATA = {{DATA}};
const esc = s => String(s ?? "").replace(/[&<>"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const tip = document.getElementById("tip");
function showTip(el, x, y) { tip.textContent = el.dataset.tip; tip.style.opacity = 1;
  const r = tip.getBoundingClientRect();
  tip.style.left = Math.min(x + 12, innerWidth - r.width - 8) + "px"; tip.style.top = Math.max(8, y - r.height - 10) + "px"; }
document.querySelectorAll("[data-tip]").forEach(el => {
  el.addEventListener("mousemove", e => showTip(el, e.clientX, e.clientY));
  el.addEventListener("mouseleave", () => tip.style.opacity = 0);
  el.addEventListener("focus", () => { const b = el.getBoundingClientRect(); showTip(el, b.left + b.width / 2, b.top); });
  el.addEventListener("blur", () => tip.style.opacity = 0);
});
const tbody = document.getElementById("rows");
function render() {
  const kind = document.getElementById("f-kind").value, lang = document.getElementById("f-lang").value;
  const graded = document.getElementById("f-graded").checked, dis = document.getElementById("f-disagree").checked;
  const fired = document.getElementById("f-fired").checked, text = document.getElementById("f-text").value.toLowerCase();
  const shown = DATA.filter(r => (!kind || r.kind === kind) && (!lang || r.lang === lang) && (!graded || r.me)
    && (!dis || r.disagree) && (!fired || r.cited_check === "fired") && (!text || r.question.toLowerCase().includes(text)));
  document.getElementById("f-count").textContent = `${shown.length} of ${DATA.length} questions`;
  tbody.innerHTML = shown.map(r => `
    <tr class="row" tabindex="0" data-id="${esc(r.id)}" aria-expanded="false">
      <td class="num">${esc(r.id)}</td><td>${esc(r.kind)}</td><td>${esc(r.lang)}</td><td>${esc(r.question)}</td>
      <td class="num">${r.me ? esc(r.me) : "—"}</td><td class="num">${esc(r.judge)}</td>
      <td><span class="badge ${r.cited_check === "fired" ? "warn" : ""}">${r.cited_check === "fired" ? "fired" : "ok"}</span></td>
      <td class="num">${r.seconds != null ? Math.round(r.seconds) + " s" : "—"}</td>
    </tr>`).join("");
}
function detailHtml(r) {
  const passages = r.passages.map((p, i) => `<details><summary>[${i + 1}] ${esc(p.title)} — ${esc(p.location)}</summary><div class="passage">${esc(p.text)}</div></details>`).join("");
  return `<tr class="detail"><td colspan="8">
    <h3>Reference answer</h3><div>${esc(r.reference)}</div>
    <h3>Assistant's answer</h3><pre class="answer">${esc(r.answer)}</pre>
    <h3>Searches</h3><div>${r.searches.map(esc).join(" · ") || "—"}</div>
    ${r.me ? `<h3>My grade</h3><div>${esc(r.me)}${r.me_note ? " — " + esc(r.me_note) : ""}</div>` : ""}
    <h3>Judge</h3><div>${esc(r.judge)} — ${esc(r.judge_reason)}</div>
    <h3>Passages the assistant saw (${r.passages.length})</h3>${passages}
  </td></tr>`;
}
function toggle(tr) {
  const next = tr.nextElementSibling;
  if (next && next.classList.contains("detail")) { next.remove(); tr.setAttribute("aria-expanded", "false"); return; }
  tr.insertAdjacentHTML("afterend", detailHtml(DATA.find(r => r.id === tr.dataset.id)));
  tr.setAttribute("aria-expanded", "true");
}
tbody.addEventListener("click", e => { const tr = e.target.closest("tr.row"); if (tr) toggle(tr); });
tbody.addEventListener("keydown", e => { const tr = e.target.closest("tr.row"); if (tr && (e.key === "Enter" || e.key === " ")) { e.preventDefault(); toggle(tr); } });
["f-kind", "f-lang", "f-graded", "f-disagree", "f-fired", "f-text"].forEach(id => document.getElementById(id).addEventListener("input", render));
render();
</script>
</body>
</html>
"""

if __name__ == "__main__":
    OUT.write_text(build(), encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)} ({OUT.stat().st_size / 1024:.0f} KB)")
