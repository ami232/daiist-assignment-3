
import fitz
from pathlib import Path

topics = [
    "critical angle of attack",
    "four forces",
    "density altitude",
    "center of gravity",
    "hypoxia",
    "carburetor icing",
    "wake turbulence",
    "load factor",
    "airworthiness",
    "corrosion",
    "hydraulic systems",
    "weight and balance",
    "moment arm",
    "empty weight",
    "stress",
    "fatigue",
    "electrical systems",
    "pitot-static",
    "gyroscopic",
    "weather",
    "oxygen"
]

for path in sorted(Path("corpus").glob("*.pdf")):

    print("\nDOCUMENT:", path.name)

    with fitz.open(path) as pdf:

        for topic in topics:

            matches = []

            for i, page in enumerate(pdf):

                text = " ".join(page.get_text().split())

                position = text.lower().find(topic.lower())

                if position >= 0:

                    excerpt = text[
                        max(0, position-100):position+400
                    ]

                    matches.append((i+1, excerpt))

            for page, excerpt in matches[:2]:

                print(f"\nTOPIC: {topic}")
                print(f"PAGE: {page}")
                print(excerpt)
