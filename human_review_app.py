"""Local blind review: real user ratings are written only when Save is clicked."""

from __future__ import annotations

import csv
import hashlib
import json
import secrets
from datetime import UTC, datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from io import StringIO
from pathlib import Path

import mistune

ROOT = Path(__file__).resolve().parent
META = json.loads((ROOT / "eval/latest_run.json").read_text())
RUN = ROOT / META["directory"]
QUESTIONS = list(
    csv.DictReader((ROOT / "eval/questions.csv").open(newline="", encoding="utf-8"))
)
ANSWERS = json.loads((RUN / "answers.json").read_text())
TOKEN = secrets.token_urlsafe(32)
LABELS = ROOT / "eval/human_labels.csv"
markdown = mistune.create_markdown(escape=True)
# Sampling depends only on question IDs and kind, never on outcomes or verdicts.
SAMPLE = []
for kind, n in [("single", 12), ("multi", 4), ("unanswerable", 4)]:
    group = [q["id"] for q in QUESTIONS if q["kind"] == kind]
    group.sort(
        key=lambda x: hashlib.sha256(("jimena-review-2026:" + x).encode()).hexdigest()
    )
    SAMPLE.extend(group[:n])
SAMPLE.sort(key=lambda x: int(x[1:]))
DATA = [
    {
        "id": q["id"],
        "question": q["question"],
        "reference": q["reference_answer"],
        "answer_html": markdown(ANSWERS[q["id"]]["answer"]),
        "evidence": [
            {
                "id": c["id"],
                "source": c["source"],
                "location": c["location"],
                "text": c["text"],
            }
            for c in ANSWERS[q["id"]]["retrieved"]
        ],
    }
    for q in QUESTIONS
]


def ratings():
    binding = ROOT / "eval/human_labels_run.txt"
    if not binding.exists() or binding.read_text().strip() != META["run_id"]:
        return {}
    with LABELS.open(newline="", encoding="utf-8") as f:
        return {r["id"]: r for r in csv.DictReader(f) if r.get("id")}


def validate(value):
    if value.get("id") not in ANSWERS:
        raise ValueError("Unknown question.")
    if str(value.get("correct")) not in {"0", "1"} or str(
        value.get("supported")
    ) not in {"0", "1"}:
        raise ValueError("Choose Yes or No for both Correct and Supported.")
    notes = str(value.get("notes", "")).strip()
    if ("0" in [str(value["correct"]), str(value["supported"])]) and not notes:
        raise ValueError("Add a short explanation for a No grade.")
    if len(notes) > 5000:
        raise ValueError("Keep notes under 5,000 characters.")
    return {
        "id": value["id"],
        "correct": str(value["correct"]),
        "supported": str(value["supported"]),
        "notes": notes,
    }


def csv_text(rows):
    output = StringIO(newline="")
    writer = csv.DictWriter(output, fieldnames=["id", "correct", "supported", "notes"])
    writer.writeheader()
    writer.writerows(rows)
    return output.getvalue()


HTML = r"""<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Jimena · Answer review</title>
<style>
:root{--navy:#18344d;--teal:#147d78;--coral:#b9523d;--line:#d8e4e8;--paper:#fff;--bg:#f3f7f8}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--navy);font:16px/1.6 system-ui,sans-serif}header{padding:22px max(24px,calc((100vw - 1400px)/2));background:white;border-bottom:1px solid var(--line)}h1{font-size:27px;margin:0 0 5px}h2{font-size:20px;margin:0 0 12px}h3{font-size:17px;margin:12px 0 8px}p{margin:8px 0 14px}.small{font-size:14px;color:#4b6572}.layout{max-width:1450px;margin:auto;padding:24px;display:grid;grid-template-columns:205px minmax(0,1fr);gap:24px}.main{min-width:0}.columns{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:24px}.panel{background:white;padding:24px;border:1px solid var(--line);border-radius:9px;margin-bottom:20px}.question{border-left:5px solid var(--teal)}.question p{font-size:20px;font-weight:550}.answer{overflow-wrap:anywhere}.answer code{font-size:12px}.answer p,.answer li{margin-bottom:12px}.answer a{color:var(--teal)}.cite{display:inline-block;font-size:13px;border:1px solid var(--line);border-radius:4px;padding:0 5px;text-decoration:none;font-weight:600}button{font:inherit;cursor:pointer;border:1px solid #adc6cc;border-radius:6px;background:white;color:var(--navy);padding:8px 13px}button:hover{border-color:var(--teal)}button:focus-visible,a:focus-visible,input:focus-visible,textarea:focus-visible,summary:focus-visible{outline:3px solid #cc795f;outline-offset:2px}.primary{background:var(--teal);color:white;border-color:var(--teal)}button[disabled]{opacity:.5;cursor:default}.nav{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;margin:15px 0}.nav button{padding:7px 2px;font-size:14px}.nav button.current{border:2px solid var(--teal);font-weight:750}.nav button.saved{background:#e5f1ed}.toolbar{display:flex;gap:8px;flex-wrap:wrap;align-items:center}.badge{font-weight:700;color:var(--teal)}fieldset{border:0;padding:0;margin:18px 0}legend{font-weight:700}label.choice{display:inline-flex;gap:9px;align-items:center;padding:9px 16px;border:1px solid var(--line);border-radius:7px;margin:5px 10px 0 0}input[type=radio]{width:19px;height:19px;accent-color:var(--teal)}textarea{display:block;width:100%;min-height:90px;font:inherit;border:1px solid #a9bfc8;border-radius:6px;padding:10px;color:var(--navy)}details{border-top:1px solid var(--line);padding:12px 0}summary{cursor:pointer;font-weight:650}.passage{white-space:pre-wrap;line-height:1.75;margin:10px 0 5px}#status{min-height:26px;font-weight:600}.error{color:#a12d20}.success{color:var(--teal)}.help{border-left:4px solid #d27a62;padding-left:12px}.sticky{position:sticky;top:16px}.pill{font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:var(--teal)}@media(max-width:1050px){.columns{grid-template-columns:1fr}.layout{grid-template-columns:155px 1fr}}@media(max-width:660px){.layout{display:block;padding:14px}.sticky{position:static}.nav{grid-template-columns:repeat(10,1fr)}.panel{padding:18px}.question p{font-size:18px}}
</style>
<header><div class="pill">Jimena · Assignment 3</div><h1>Review the assistant’s answers</h1><div>Read the question, compare the answer with its source passages, and give your own two grades.</div></header>
<div class="layout"><aside><div class="sticky"><strong id="progress">0 / 20 reviewed</strong><p class="small">A fixed sample of 20 covers all question types. You can review the full set if you prefer.</p><button id="toggle">Show all questions</button><nav id="nav" class="nav" aria-label="Questions"></nav><button id="export">Download saved CSV</button><p class="small">Each Save writes directly to this draft’s <code>eval/human_labels.csv</code>. No judge scores are shown.</p><details><summary>How to grade</summary><p><strong>Correct:</strong> it answers the question fully and accurately.</p><p><strong>Supported:</strong> every important factual claim follows from the passages shown.</p><p>A true but incomplete answer can be Correct: No, Supported: Yes.</p><p>A refusal is Correct: Yes only when the corpus cannot establish the requested answer. It can be Supported: Yes if it avoids inventing facts.</p><p>If a reference seems wrong, note that. It is a checking aid, not a verdict to copy.</p></details></div></aside>
<main class="main"><section class="panel question"><div class="toolbar"><span class="badge" id="qid"></span><span class="small" id="position"></span></div><p id="question"></p></section>
<div class="columns"><div><section class="panel"><h2>Assistant’s answer</h2><div id="answer" class="answer"></div></section><section class="panel"><h2>Your grades</h2><fieldset><legend>Correct?</legend><div class="small">Does it answer all important parts accurately?</div><label class="choice"><input type="radio" name="correct" value="1">Yes (1)</label><label class="choice"><input type="radio" name="correct" value="0">No (0)</label></fieldset><fieldset><legend>Supported?</legend><div class="small">Do the source passages support every important factual claim?</div><label class="choice"><input type="radio" name="supported" value="1">Yes (1)</label><label class="choice"><input type="radio" name="supported" value="0">No (0)</label></fieldset><label for="notes"><strong>Notes</strong><span class="small"> — required for any No; one sentence is enough</span></label><textarea id="notes" placeholder="For example: it answers only the first half of the question."></textarea><div id="status" role="status" aria-live="polite"></div><div class="toolbar"><button id="prev">Previous</button><button id="save" class="primary">Save & next</button><button id="next">Next without saving</button></div></section></div>
<div><section class="panel"><h2>What to compare it with</h2><details id="referenceBox" open><summary>Reference answer</summary><p id="reference"></p><p class="small">Check this against the sources. Don’t assume the reference is infallible.</p></details><h3>Retrieved source passages</h3><p class="small">Citation numbers in the answer jump to the matching passage. Relevance scores and judge grades are hidden.</p><div id="evidence"></div><details><summary>Corpus scope</summary><p class="small">The baseline contains the Operations Management textbook, FEMA’s Supply Chain Resilience Guide, and the UK Critical Imports and Supply Chains Strategy. It has no private company records or live shipment data. The optional SBA page is outside the baseline.</p></details></section></div></div></main></div>
<script>
const TOKEN=__TOKEN__, DATA=__DATA__, SAMPLE=__SAMPLE__;
let grades={},scope=SAMPLE.slice(),index=0,dirty=false;
const $=id=>document.getElementById(id);
function escapeText(s){return String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));}
function notify(text,error=false){$('status').textContent=text;$('status').className=error?'error':'success';}
function render(){const id=scope[index],q=DATA.find(x=>x.id===id),g=grades[id]||{};dirty=false;
 $('qid').textContent=id.toUpperCase();$('position').textContent=`Question ${index+1} of ${scope.length}`;$('question').textContent=q.question;$('reference').textContent=q.reference;
 let html=q.answer_html;const known=new Map(q.evidence.map((c,i)=>[c.id,i+1]));html=html.replace(/\[chunk:([0-9a-f]{64})\]/g,(all,cid)=>known.has(cid)?`<a class="cite" href="#source-${cid}" onclick="document.getElementById('source-${cid}').open=true">[${known.get(cid)}]</a>`:all);$('answer').innerHTML=html;
 $('evidence').innerHTML=q.evidence.length?q.evidence.map((c,i)=>`<details id="source-${c.id}" ${i===0?'open':''}><summary>[${i+1}] ${escapeText(c.source)} · ${escapeText(c.location)}</summary><div class="passage">${escapeText(c.text)}</div></details>`).join(''):'<p class="help">No passages were retrieved. Absence of retrieval alone does not prove the corpus lacks an answer; consider the reference explanation and corpus scope.</p>';
 for(const name of ['correct','supported'])document.querySelectorAll(`input[name=${name}]`).forEach(r=>r.checked=r.value===g[name]);$('notes').value=g.notes||'';notify(g.id?'Your saved grades are loaded.':'Choose both grades, then Save.');
 $('prev').disabled=index===0;$('next').disabled=index===scope.length-1;drawNav();}
function drawNav(){const total=Object.keys(grades).length;$('progress').textContent=`${total} / 20 reviewed`;$('nav').innerHTML=scope.map((id,i)=>`<button class="${i===index?'current ':''}${grades[id]?'saved':''}" data-i="${i}" aria-label="${id}${grades[id]?', saved':''}" ${i===index?'aria-current="step"':''}>${escapeText(id)}</button>`).join('');$('nav').querySelectorAll('button').forEach(b=>b.onclick=()=>go(Number(b.dataset.i)));$('export').disabled=!total;}
function go(n){if(dirty&&!confirm('Leave this question without saving your changes?'))return;index=n;render();window.scrollTo(0,0);}
async function save(){const value={id:scope[index],correct:document.querySelector('input[name=correct]:checked')?.value,supported:document.querySelector('input[name=supported]:checked')?.value,notes:$('notes').value};
 $('save').disabled=true;try{const r=await fetch('/api/grade',{method:'POST',headers:{'Content-Type':'application/json','X-Review-Token':TOKEN},body:JSON.stringify(value)});const state=await r.json();if(!r.ok){notify(state.error||'Could not save.',true);return;}grades=state.grades;dirty=false;const next=scope.findIndex((id,i)=>i>index&&!grades[id]);if(next>=0){index=next;render();window.scrollTo(0,0);}else{drawNav();notify(Object.keys(grades).length>=20?'20 or more answers reviewed. Your grades are saved. You can review more or return to the chat.':'Saved. Continue with an unreviewed question.');}}catch(e){notify('Connection lost. Keep this page open and ask to restart the local reviewer.',true);}finally{$('save').disabled=false;}}
$('save').onclick=save;$('prev').onclick=()=>go(index-1);$('next').onclick=()=>go(index+1);$('toggle').onclick=()=>{if(dirty&&!confirm('Change view without saving?'))return;const all=scope.length===DATA.length;scope=all?SAMPLE.slice():DATA.map(x=>x.id);index=0;$('toggle').textContent=all?'Show all questions':'Use sample of 20';render();};$('export').onclick=()=>{window.location.href='/api/export';};document.querySelectorAll('input,textarea').forEach(e=>e.addEventListener('input',()=>dirty=true));window.addEventListener('beforeunload',e=>{if(dirty){e.preventDefault();e.returnValue='';}});
fetch('/api/state').then(r=>r.json()).then(s=>{grades=s.grades;const n=scope.findIndex(id=>!grades[id]);index=n<0?0:n;render();}).catch(()=>notify('Could not load saved grades.',true));
</script></html>"""


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def response(self, code, payload, kind="application/json; charset=utf-8"):
        body = (
            json.dumps(payload, ensure_ascii=False).encode()
            if kind.startswith("application/json")
            else payload.encode()
        )
        self.send_response(code)
        self.send_header("Content-Type", kind)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def allowed_host(self):
        return self.headers.get("Host") in {
            f"127.0.0.1:{self.server.server_port}",
            f"localhost:{self.server.server_port}",
        }

    def do_GET(self):
        if not self.allowed_host():
            return self.response(403, {"error": "Local access only."})
        if self.path == "/":
            html = (
                HTML.replace("__TOKEN__", json.dumps(TOKEN))
                .replace(
                    "__DATA__",
                    json.dumps(DATA, ensure_ascii=False).replace("<", "\\u003c"),
                )
                .replace("__SAMPLE__", json.dumps(SAMPLE))
            )
            return self.response(200, html, "text/html; charset=utf-8")
        if self.path == "/api/state":
            return self.response(
                200,
                {
                    "run_id": META["run_id"],
                    "grades": ratings(),
                    "sample": SAMPLE,
                    "count": len(DATA),
                },
            )
        if self.path == "/api/export":
            return self.response(
                200, csv_text(ratings().values()), "text/csv; charset=utf-8"
            )
        return self.response(404, {"error": "Not found."})

    def do_POST(self):
        if not self.allowed_host() or not secrets.compare_digest(
            self.headers.get("X-Review-Token", ""), TOKEN
        ):
            return self.response(403, {"error": "Invalid local session."})
        if self.path not in {"/api/grade", "/api/validate"}:
            return self.response(404, {"error": "Not found."})
        try:
            size = int(self.headers.get("Content-Length", "0"))
            if size > 15000:
                raise ValueError("Request too large.")
            value = validate(json.loads(self.rfile.read(size)))
        except (ValueError, TypeError, json.JSONDecodeError) as error:
            return self.response(400, {"error": str(error)})
        if self.path == "/api/validate":
            return self.response(200, {"valid": True})
        existing = ratings()
        existing[value["id"]] = value
        ordered = [existing[q["id"]] for q in QUESTIONS if q["id"] in existing]
        temporary = LABELS.with_suffix(".tmp")
        temporary.write_text(csv_text(ordered), encoding="utf-8")
        temporary.replace(LABELS)
        (ROOT / "eval/human_labels_run.txt").write_text(META["run_id"] + "\n")
        session = {
            "run_id": META["run_id"],
            "saved_answers": len(ordered),
            "updated_at": datetime.now(UTC).isoformat(),
            "method": "Ratings entered by the user through the local blind review form; no scores preselected.",
            "sample_method": "12 single, 4 multi, 4 unanswerable, ranked by SHA256 of fixed seed plus question ID; selection does not use outcomes.",
            "sample_ids": SAMPLE,
            "judge_scores_shown": False,
        }
        (ROOT / "eval/human_review_session.json").write_text(
            json.dumps(session, indent=2) + "\n"
        )
        return self.response(200, {"grades": existing})


if __name__ == "__main__":
    server = HTTPServer(("127.0.0.1", 0), Handler)
    info = {"url": f"http://127.0.0.1:{server.server_port}", "run_id": META["run_id"]}
    (ROOT / "review/local_review_server.json").write_text(
        json.dumps(info, indent=2) + "\n"
    )
    print(info["url"], flush=True)
    server.serve_forever()
