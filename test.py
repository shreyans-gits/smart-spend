from cv.capture import load_image
from cv.preprocess import preprocess
from cv.ocr import extract_text
from cv.extractor import extract_total

image = load_image("test/image.png")
processed = preprocess(image)
raw_text = extract_text(processed)
total = extract_total(raw_text)

print("--- RAW OCR TEXT ---")
print(raw_text)
print("--- EXTRACTED TOTAL ---")
print(total)