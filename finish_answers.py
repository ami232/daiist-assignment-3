
import asyncio
import csv
import json
import os
from pathlib import Path
from agent import ask

async def main():

    questions = list(csv.DictReader(
        open("eval/questions.csv")
    ))

    output = Path("eval/agent_results.json")
    errors = Path("eval/errors.json")

    results = json.loads(
        output.read_text()
    ) if output.exists() else []

    failures = []

    completed = {r["id"] for r in results}

    models = list(dict.fromkeys([
        Path("selected_model.txt").read_text().strip(),
        "gemini-3.5-flash-lite",
        "gemini-3.1-flash-lite",
        "gemini-3.8-flash"
    ]))

    for q in questions:

        if q["id"] in completed:
            continue

        print("QUESTION:", q["id"], flush=True)

        for model in models:

            os.environ["GEMINI_CHAT_MODEL"] = model

            try:

                result = await asyncio.wait_for(
                    ask(q["question"]),
                    timeout=60
                )

                row = {
                    **q,
                    **result,
                    "model": model,
                    "label": "pending",
                    "reason": ""
                }

                results.append(row)

                output.write_text(
                    json.dumps(results, indent=2)
                )

                print(
                    "SAVED:",
                    q["id"],
                    len(results),
                    "/35",
                    flush=True
                )

                break

            except Exception as e:

                failures.append({
                    "id": q["id"],
                    "model": model,
                    "error": str(e)
                })

                errors.write_text(
                    json.dumps(failures, indent=2)
                )

                print(
                    "Model failed:", str(e)[:200],
                    flush=True
                )

        else:
            print("Question unsuccessful:", q["id"])

        await asyncio.sleep(0.2)

    print("TOTAL COMPLETED:", len(results), "/35")

if __name__ == "__main__":
    asyncio.run(main())
