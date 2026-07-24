# https://github.com/RapidAI/RapidOCR

from rapidocr import RapidOCR

# --- Konfiguration ---
IMAGE_PATH = "Adobe Scan 24 Jul 2026.jpg"   # Pfad zu deinem Bild anpassen
OUTPUT_PATH = "output.txt"                # Ausgabedatei
INDENT_THRESHOLD = 20                     # Pixel, ggf. anpassen

# --- OCR ausführen ---
engine = RapidOCR()
result = engine(IMAGE_PATH)

lines = []
for box, text, score in zip(result.boxes, result.txts, result.scores):
    x_left = min(p[0] for p in box)
    y_top = min(p[1] for p in box)
    lines.append({"text": text, "x_left": x_left, "y_top": y_top})

# nach Y-Position sortieren, damit die Lesereihenfolge stimmt
lines.sort(key=lambda l: l["y_top"])

# --- Zeilen zu Quellen gruppieren (Einrückung relativ zur Baseline der Quelle) ---
entries = []
current_entry = []
baseline_x = None

for line in lines:
    if baseline_x is None:
        baseline_x = line["x_left"]
        current_entry.append(line["text"])
        continue

    is_continuation = line["x_left"] > baseline_x + INDENT_THRESHOLD

    if is_continuation:
        current_entry.append(line["text"])
    else:
        entries.append(" ".join(current_entry))
        current_entry = [line["text"]]
        baseline_x = line["x_left"]

if current_entry:
    entries.append(" ".join(current_entry))

# --- Ergebnis in txt speichern ---
with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    for i, entry in enumerate(entries, 1):
        f.write(f"[{i}] {entry}\n\n")

print(f"{len(entries)} Quellen erkannt. Gespeichert in: {OUTPUT_PATH}")