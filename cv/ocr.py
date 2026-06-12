import numpy as np
import pytesseract
import config

if getattr(config, "TESSERACT_PATH", None):
    pytesseract.pytesseract.tesseract_cmd = config.TESSERACT_PATH
    
def extract_text(image: np.ndarray) -> str:
    custom_config = r"--psm 6"
    
    try:
        raw_text = pytesseract.image_to_string(image, config=custom_config)
        return raw_text.strip()
    except Exception as e:
        raise RuntimeError(f"OCR Extraction Engine failed: {e}") from e