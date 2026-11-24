"""
One-off script: copy the public part of the Guía fichas into data/.

The original fichas live in the Moysi Voice AI project. Besides the public
information of each trámite (what it is, who can apply, plazos, documents...)
they also contain the voice agent's conversation scripts (paso0, paso1...),
which are Moysi's own work and are not public. This script keeps only the
public, factual fields, so the repo can be shared and graded without them.
(documentacion_aviso is dropped too: it is an instruction to the voice agent,
not information about the trámite.)

It has already been run; its output (data/) is committed. To run it again:
    uv run python export_fichas.py ~/Moysi/moysi-api/provisioning/fichas/guia
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / "data" / "fichas"
EXTRA_DIR = ROOT / "data" / "extra"

# The fields we keep, in the order they will appear in the index.
PUBLIC_FIELDS = [
    "slug",
    "nombre_oficial",
    "sede_url",
    "ambito",
    "que_es",
    "quien_puede",
    "identificacion",
    "plazo_presentacion",
    "plazo_resolucion",
    "silencio_administrativo",
    "documentacion",
    "documentacion_kb",
    "notificacion",
    "normativa",
    "faq",
    "kb_extra",
]

# This ficha is kept out of the first index, to show the add_document tool later.
HELD_OUT = "matrimonio-civil"


def export(source_dir: Path) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    EXTRA_DIR.mkdir(parents=True, exist_ok=True)
    count = 0
    for path in sorted(source_dir.glob("*.json")):
        ficha = json.loads(path.read_text(encoding="utf-8"))
        public = {field: ficha[field] for field in PUBLIC_FIELDS if ficha.get(field)}
        target_dir = EXTRA_DIR if public["slug"] == HELD_OUT else OUT_DIR
        target = target_dir / f"{public['slug']}.json"
        target.write_text(json.dumps(public, ensure_ascii=False, indent=2), encoding="utf-8")
        count += 1
    print(f"Exported {count} fichas into {OUT_DIR} and {EXTRA_DIR}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: uv run python export_fichas.py <folder with the Guía fichas>")
    export(Path(sys.argv[1]).expanduser())
