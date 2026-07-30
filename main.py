# https://github.com/RapidAI/RapidOCR

from rapidocr import RapidOCR
import re

# --- Konfiguration ---
IMAGE_PATH = "data/20260730110422904.jpg"
OUTPUT_PATH = "data/output.txt"
VIZ_PATH = "viz/output.jpg"

keyord_schema_gnd_dnb = """
<datafield tag="650" ind1=" " ind2="7">
    <subfield code="0">(DE-588){gnd_code}</subfield>
    <subfield code="0">https://d-nb.info/gnd/{gnd_code}</subfield>
    <subfield code="0">(DE-101){dnb_code}</subfield>
    <subfield code="a">{keyword}</subfield>
    <subfield code="9">rswk-swf</subfield>
    <subfield code="2">gnd</subfield>
  </datafield>
"""

keyord_schema = """
<datafield tag="650" ind1=" " ind2="7">
    <subfield code="a">{keyword}</subfield>
  </datafield>
"""

# --- OCR ausführen ---
engine = RapidOCR(
    params={
        "Rec.lang_type": "german",
        "Det.lang_type": "german",
    }
)

result = engine(IMAGE_PATH)
print(result)
# result.vis("vis_result.jpg")

# Cleaning
# - remove charcters after the number
# - remove special characters
# - remove sub categories? Can I sort them in some way?
# TODO: Remove blank strings
result = sorted(
    [''.join([i for i in text if not i.isdigit()]) for text in result.txts]
    )

result = [i.strip() for i in result if i != ""]

for i in result:
    print(i)
    # print(keyord_schema_gnd_dnb.format(gnd_code=0, dnb_code=0, keyword=i)) # Test
    # break


# - Connect to GND and DNB via API
# - save kexwords in MarcXML format, if possible





# ---------------------------------
# For literature source recognition
# ---------------------------------


# lines = []
# for box, text, score in zip(result.boxes, result.txts, result.scores):
#     x_left = min(p[0] for p in box)
#     y_top = min(p[1] for p in box)
#     lines.append({"text": text, "x_left": x_left, "y_top": y_top})

# nach Y-Position sortieren, damit die Lesereihenfolge stimmt
# lines.sort(key=lambda l: l["y_top"])

# --- Zeilen zu Quellen gruppieren (Einrückung relativ zur Baseline der Quelle) ---
# entries = []
# current_entry = []
# baseline_x = None

# for line in lines:
#     if baseline_x is None:
#         baseline_x = line["x_left"]
#         current_entry.append(line["text"])
#         continue

#     is_continuation = line["x_left"] > baseline_x + INDENT_THRESHOLD

#     if is_continuation:
#         current_entry.append(line["text"])
#     else:
#         entries.append(" ".join(current_entry))
#         current_entry = [line["text"]]
#         baseline_x = line["x_left"]

# if current_entry:
#     entries.append(" ".join(current_entry))

# --- Ergebnis in txt speichern ---
# with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
#     for i, entry in enumerate(entries, 1):
#         f.write(f"[{i}] {entry}\n\n")

# print(f"{len(entries)} Quellen erkannt. Gespeichert in: {OUTPUT_PATH}")
