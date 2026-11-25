import xml.etree.ElementTree as ET
from pathlib import Path

for f in sorted(Path("corpus/raw").glob("*.xml")):
    root = ET.parse(f).getroot()
    print(f.name)
    for child in root:
        tag = child.tag.split("}")[-1]
        words = len(" ".join(child.itertext()).split())
        print(f"   {tag}: {words:,}")
        for sub in child:
            stag = sub.tag.split("}")[-1]
            swords = len(" ".join(sub.itertext()).split())
            if swords > 1000:
                print(f"      {stag}: {swords:,}")
