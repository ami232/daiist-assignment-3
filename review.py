"""Local, blind human review. Reads saved answers; never calls an LLM.

Run after evaluate.py --answers-only, then open the printed local address.
Only the student's explicit grades are written to eval/human_labels.csv.
"""
from __future__ import annotations

import argparse
import csv
import hmac
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import io
import json
from pathlib import Path
import secrets
import tempfile
import threading

from evaluation_support import digest, load_human_labels

ROOT = Path(__file__).resolve().parent


class Review:
    def __init__(self, directory):
        self.directory = Path(directory)
        self.questions = json.loads((self.directory / "human_review.json").read_text())
        self.ids = {q["id"] for q in self.questions}
        if not self.questions or len(self.ids) != len(self.questions):
            raise ValueError("Review requires saved answers with unique IDs.")
        self.review_hash = digest(self.questions)
        self.labels_path = self.directory / "human_labels.csv"

    def locked(self):
        if (self.directory / "judge_results.jsonl").exists():
            return True
        current = {q["id"]: q["answer_review_sha256"] for q in self.questions}
        for path in (self.directory / "runs").glob("*/human_binding.json"):
            bound = json.loads(path.read_text()).get("reviewed_answers", {})
            if bound and all(current.get(k) == v for k, v in bound.items()):
                return True
        return False

    def labels_hash(self):
        return digest(self.labels_path.read_bytes())

    def payload(self):
        return {"questions": self.questions,
                "labels": load_human_labels(self.labels_path, self.ids, minimum=0),
                "review_hash": self.review_hash, "labels_hash": self.labels_hash(),
                "locked": self.locked(), "minimum": 20}

    def save(self, body):
        if not isinstance(body, dict):
            raise ValueError("Invalid review request.")
        if self.locked():
            raise ValueError("These blind grades are already bound or judge results exist. Grades are locked.")
        if digest(json.loads((self.directory / "human_review.json").read_text())) != self.review_hash:
            raise ValueError("The answers or evidence changed. Restart review before grading.")
        if body.get("review_hash") != self.review_hash:
            raise ValueError("This page refers to different answers. Reload before saving.")
        if body.get("labels_hash") != self.labels_hash():
            raise ValueError("Grades changed in another window. Reload before saving.")
        labels = body.get("labels")
        if not isinstance(labels, list) or len(labels) > len(self.ids):
            raise ValueError("Invalid grade list.")
        out = io.StringIO(newline="")
        writer = csv.DictWriter(out, fieldnames=["id", "correct", "supported", "notes"], lineterminator="\n")
        writer.writeheader()
        for label in labels:
            if not isinstance(label, dict) or set(label) != {"id", "correct", "supported", "notes"}:
                raise ValueError("Each grade needs id, correctness, support and notes.")
            if any(type(label[k]) is not int or label[k] not in (0, 1) for k in ("correct", "supported")):
                raise ValueError("Choose your own yes/no grade for both fields.")
            if not isinstance(label["notes"], str) or len(label["notes"]) > 4000:
                raise ValueError("Notes must be text of at most 4,000 characters.")
            writer.writerow(label)
        temporary = None
        try:
            with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", newline="", dir=self.directory,
                                             prefix=".human-review-", suffix=".csv", delete=False) as stream:
                stream.write(out.getvalue())
                temporary = Path(stream.name)
            validated = load_human_labels(temporary, self.ids, minimum=0)
            temporary.replace(self.labels_path)
            return {"saved": len(validated), "labels_hash": self.labels_hash()}
        finally:
            if temporary is not None:
                temporary.unlink(missing_ok=True)


def handler_for(review):
    token = secrets.token_urlsafe(32)
    save_lock = threading.Lock()
    page = (ROOT / "eval/review_template.html").read_text().replace("__REVIEW_TOKEN__", token)

    class Handler(BaseHTTPRequestHandler):
        def local_host(self):
            if self.headers.get("Host") != f"127.0.0.1:{self.server.server_port}":
                self.respond(403, {"error": "Use the printed local review address."})
                return False
            return True

        def respond(self, status, content, content_type="application/json; charset=utf-8"):
            encoded = content.encode() if isinstance(content, str) else json.dumps(content, ensure_ascii=False).encode()
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(encoded)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Content-Security-Policy", "default-src 'self'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; connect-src 'self'; frame-ancestors 'none'; base-uri 'none'")
            self.end_headers()
            self.wfile.write(encoded)

        def do_GET(self):
            if not self.local_host():
                return
            if self.path == "/":
                self.respond(200, page, "text/html; charset=utf-8")
            elif self.path == "/api/review":
                self.respond(200, review.payload())
            else:
                self.respond(404, {"error": "Not found"})

        def do_POST(self):
            if not self.local_host():
                return
            if self.path != "/api/labels":
                self.respond(404, {"error": "Not found"})
                return
            if not hmac.compare_digest(self.headers.get("X-Review-Token", ""), token):
                self.respond(403, {"error": "Open the review page before saving."})
                return
            try:
                length = int(self.headers.get("Content-Length", "0"))
                if not 0 < length <= 150000:
                    raise ValueError("Invalid request size.")
                body = json.loads(self.rfile.read(length))
                with save_lock:
                    saved = review.save(body)
                self.respond(200, saved)
            except (ValueError, TypeError, KeyError) as error:
                self.respond(400, {"error": str(error)})

        def log_message(self, format, *args):
            pass

    return Handler


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    try:
        review = Review(ROOT / "eval")
    except FileNotFoundError:
        parser.error("Generate the saved answers first: python evaluate.py --answers-only")
    # Browsers can open idle connections ahead of their next request. One such
    # connection must not prevent the review page or its data from loading.
    server = ThreadingHTTPServer(("127.0.0.1", args.port), handler_for(review))
    print(f"Blind review: http://127.0.0.1:{args.port}/", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
