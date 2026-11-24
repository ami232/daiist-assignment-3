"""Read the selected documentation straight from a checksum-pinned PostgreSQL release."""
import hashlib
import re
import tarfile
import tempfile
import urllib.request
from dataclasses import dataclass
from pathlib import Path

from bs4 import BeautifulSoup, Comment

ROOT = Path(__file__).resolve().parent
VERSION = "17.12"
ARCHIVE = f"postgresql-{VERSION}.tar.bz2"
DOWNLOAD = f"https://ftp.postgresql.org/pub/source/v{VERSION}/{ARCHIVE}"
SHA256 = "9cf136a703d8ee2f83465c43be4e9e8e7930c82b0bfba13be7e2537be769ac55"
TAG = "REL_17_12"
# The optional second field selects a single chapter section before extraction.
DOCUMENTS = {
    "backup": ("backup.sgml", None),
    "standby": ("high-availability.sgml", None),
    "wal": ("wal.sgml", None),
    "wal-settings": ("config.sgml", "runtime-config-wal"),
    "replication-settings": ("config.sgml", "runtime-config-replication"),
    **{name: (f"ref/{name}.sgml", None) for name in (
        "pg_dump", "pg_dumpall", "pg_restore", "pg_basebackup", "pg_combinebackup",
        "pg_receivewal", "pg_verifybackup",
    )},
}
TOOLS_BY_ID = {
    "app-pgdump": "pg_dump", "app-pg-dumpall": "pg_dumpall", "app-pgrestore": "pg_restore",
    "app-pgbasebackup": "pg_basebackup", "app-pgcombinebackup": "pg_combinebackup",
    "app-pgverifybackup": "pg_verifybackup", "app-pgreceivewal": "pg_receivewal",
    "app-psql": "psql",
}
SECTIONS = re.compile(r"^(?:chapter|appendix|refentry|(?:ref)?sect[1-5])$")


@dataclass(frozen=True)
class Section:
    source: str
    location: str
    url: str
    text: str


def archive_path():
    folder = ROOT / "corpus"
    folder.mkdir(exist_ok=True)
    target = folder / ARCHIVE
    if target.exists():
        with target.open("rb") as stream:
            if hashlib.file_digest(stream, "sha256").hexdigest() == SHA256:
                return target
    with tempfile.NamedTemporaryFile(dir=folder, delete=False) as output:
        temporary = Path(output.name)
    try:
        urllib.request.urlretrieve(DOWNLOAD, temporary)
        with temporary.open("rb") as stream:
            if hashlib.file_digest(stream, "sha256").hexdigest() != SHA256:
                raise ValueError("PostgreSQL release checksum mismatch")
        temporary.replace(target)
    finally:
        temporary.unlink(missing_ok=True)
    return target


def extract_sections(raw, source, filename, selection):
    soup = BeautifulSoup(raw, "html.parser")
    for tag in soup.find_all(["indexterm", "refmeta", "refnamediv", "refsynopsisdiv"]):
        tag.decompose()
    for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
        comment.extract()
    for ref in soup.find_all("xref"):
        target = ref.get("linkend", "")
        if target.startswith("guc-"):
            target = target[4:].replace("-", "_")
        ref.replace_with(TOOLS_BY_ID.get(target, target))
    for quote in soup.find_all("quote"):
        quote.insert_before('“')
        quote.insert_after('”')
    for tag in soup.find_all(["para", "term", "entry", "row", "listitem", "screen",
                              "programlisting", "synopsis", "title", "simpara"]):
        tag.insert_before("\n\n")
        tag.insert_after("\n\n")

    root = soup.find(id=selection) if selection else soup.find(SECTIONS)
    if root is None:
        raise ValueError(f"Missing documentation section in {filename}")
    nodes = [root, *root.find_all(SECTIONS)]
    # Extract each section's own text once. Children remain independently citable.
    records = []
    for node in reversed(nodes):
        heading = node.find("title", recursive=False)
        title = heading.get_text(strip=True) if heading else source
        if heading:
            heading.decompose()
        location = node.get("id") or title
        url = f"https://github.com/postgres/postgres/blob/{TAG}/doc/src/sgml/{filename}#L{node.sourceline}"
        paragraphs = [" ".join(part.split()) for part in node.get_text().replace("\u200b", "").split("\n\n")]
        content = "\n\n".join(part for part in paragraphs if part)
        if content:
            records.append(Section(source, location, url, content))
        node.extract()
    return list(reversed(records))


def load_corpus():
    archive = archive_path()
    with tarfile.open(archive) as release:
        members = {member.name: member for member in release}
        result = []
        for source, (filename, selection) in DOCUMENTS.items():
            member = members[f"postgresql-{VERSION}/doc/src/sgml/{filename}"]
            raw = release.extractfile(member).read().decode("utf-8")
            result.extend(extract_sections(raw, source, filename, selection))
    return result


def write_reading_copy(sections):
    folder = ROOT / "corpus" / "reading"
    folder.mkdir(parents=True, exist_ok=True)
    for source in DOCUMENTS:
        records = [r for r in sections if r.source == source]
        blocks = [f"# {source} · PostgreSQL {VERSION}", "Source text under the PostgreSQL License. See POSTGRESQL-LICENSE.txt in the project root."]
        for record in records:
            blocks.extend([f"## {record.location}", record.url, record.text])
        (folder / f"{source}.md").write_text("\n\n".join(blocks) + "\n", encoding="utf-8")


if __name__ == "__main__":
    sections = load_corpus()
    write_reading_copy(sections)
    for source in DOCUMENTS:
        rows = [s for s in sections if s.source == source]
        print(f"{source:22s} {sum(len(s.text.split()) for s in rows):6d} words, {len(rows):3d} sections")
    print("Total words:", sum(len(s.text.split()) for s in sections))
