
from google import genai
from api_key import load_api_key
from pathlib import Path

client = genai.Client(api_key=load_api_key())

models = [
    "gemini-3.5-flash-lite",
    "gemini-3.1-flash-lite",
    "gemini-3.8-flash",
    "gemini-flash-lite-latest",
    "gemini-flash-latest"
]

for model in models:
    try:
        print("Testing:", model, flush=True)

        response = client.models.generate_content(
            model=model,
            contents="Reply with OK."
        )

        if response.text:
            Path("selected_model.txt").write_text(model)
            print("WORKING MODEL:", model, flush=True)
            break

    except Exception as e:
        print(str(e)[:250], flush=True)
else:
    raise RuntimeError("All Gemini models failed.")
