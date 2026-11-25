
import asyncio
import json
from pathlib import Path
from agent import ask
from server import add_document

async def main():

    question = "What is the official title of FAA Advisory Circular 120-92D?"

    print("BEFORE:", flush=True)
    before = await ask(question)
    print(before["answer"], flush=True)

    path = "new_documents/AC_120-92D.pdf"

    approval = input("Approve adding the document? Type YES: ")

    if approval != "YES":
        print("Permission denied")
        return

    added = add_document(path)
    print(added, flush=True)

    print("AFTER:", flush=True)
    after = await ask(question)
    print(after["answer"], flush=True)

    Path("eval/before_after.json").write_text(
        json.dumps({
            "before": before,
            "document_added": added,
            "after": after
        }, indent=2)
    )

if __name__ == "__main__":
    asyncio.run(main())
