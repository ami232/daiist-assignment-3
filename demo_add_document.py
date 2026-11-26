"""
Demo "añadir un documento": respuesta ANTES y DESPUÉS de añadirlo.

    uv run python demo_add_document.py "tu pregunta sin respuesta" ruta/al/documento.pdf

Pasos:
  1. Copia index/ a una carpeta temporal (para NO tocar el índice que entregas y que tu
     evaluación siga siendo reproducible). Con --keep trabaja sobre el índice real.
  2. Pregunta al agente -> respuesta "antes" (debería ser un rechazo).
  3. Llama a add_document con aprobación automática (la das tú al lanzar este script).
  4. Vuelve a preguntar -> respuesta "después", con citas al documento nuevo.
  5. Lo guarda todo en eval/add_document_demo.md para pegarlo en el REPORT.

El documento tiene que estar dentro de la carpeta del proyecto (p. ej. nuevos/).
"""

import asyncio
import os
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent


async def demo(question: str, path: str) -> str:
    import config
    from agent import Harness

    out = ["# Añadir un documento: antes y después\n", f"**Pregunta:** {question}\n",
           f"**Documento añadido:** `{path}`\n", f"**Índice usado:** `{config.INDEX_DIR}`\n"]
    async with Harness(approve=lambda p: False) as h:
        before = await h.ask(question)
    out += ["## Antes\n", before["answer"], f"\n_Citas: {before['citations'] or 'ninguna'}_\n"]

    async with Harness(approve=lambda p: True) as h:
        added = await h.session.call_tool("add_document", {"path": path})
        result = "\n".join(getattr(c, "text", "") for c in added.content)
        out += ["## add_document\n", f"```\n{result}\n```\n"]
        after = await h.ask(question)
    out += ["## Después\n", after["answer"], f"\n_Citas: {after['citations'] or 'ninguna'}_\n",
            f"\n_Coste: antes {before['total_tokens']} tokens / {before['seconds']} s · "
            f"después {after['total_tokens']} tokens / {after['seconds']} s_\n"]
    return "\n".join(out)


def main() -> None:
    args = [a for a in sys.argv[1:] if a != "--keep"]
    if len(args) != 2:
        raise SystemExit(__doc__)
    question, path = args
    if "--keep" not in sys.argv:
        tmp = Path(tempfile.mkdtemp(prefix="index_demo_")) / "index"
        shutil.copytree(ROOT / "index", tmp)
        os.environ["RAG_INDEX_DIR"] = str(tmp)      # lo hereda el servidor MCP
        import config                               # y lo usa este proceso
        config.INDEX_DIR, config.CHROMA_DIR, config.QUERY_CACHE = tmp, tmp / "chroma", tmp / "query_cache.json"
    text = asyncio.run(demo(question, path))
    (ROOT / "eval" / "add_document_demo.md").write_text(text, encoding="utf-8")
    print(text)
    print("\nGuardado en eval/add_document_demo.md")


if __name__ == "__main__":
    main()
