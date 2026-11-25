import argparse
import re
import unicodedata

from index import get_collection


def plain(text: str) -> str:
    """Lower case, no accents: 'Vivienda' and 'vivienda' and 'VIVIENDA' all match."""
    decomposed = unicodedata.normalize("NFD", text.lower())
    return "".join(c for c in decomposed if unicodedata.category(c) != "Mn")


def main() -> None:
    parser = argparse.ArgumentParser(description="Find a word or phrase in the indexed chunks.")
    parser.add_argument("phrase")
    parser.add_argument("--party", help="only this party, e.g. pp, psoe, sumar, vox")
    parser.add_argument("--show", type=int, default=8, help="how many snippets to print (default 8)")
    args = parser.parse_args()

    data = get_collection().get(include=["documents", "metadatas"])
    needle = plain(args.phrase)
    per_source: dict[str, int] = {}
    shown = 0
    for text, meta in zip(data["documents"], data["metadatas"]):
        if args.party and meta["party"].lower() != args.party.lower():
            continue
        haystack = plain(text)
        hits = [m.start() for m in re.finditer(re.escape(needle), haystack)]
        if not hits:
            continue
        per_source[meta["source"]] = per_source.get(meta["source"], 0) + len(hits)
        if shown < args.show:
            # plain() keeps string length for Spanish text, so positions line up with the original
            at = hits[0]
            snippet = text[max(0, at - 90): at + len(needle) + 90].replace("\n", " ")
            print(f"[{meta['source']}, {meta['location']}] ...{snippet}...")
            shown += 1
    print()
    if per_source:
        print("Matches per document:", ", ".join(f"{s}: {n}" for s, n in sorted(per_source.items())))
    else:
        print(f"0 matches for {args.phrase!r}: the index has no passage with this phrase.")


if __name__ == "__main__":
    main()
