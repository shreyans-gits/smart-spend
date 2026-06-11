import os
import cv2

def load_image(source: str):
    if source.strip().lower() == "webcam":
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            raise RuntimeError("Could not open or initialize the default webcam.")
        
        try:
            ret, frame = cap.read()
            if not ret or frame is None:
                raise RuntimeError("Failed to capture a valid frame from the webcam.")
            return frame
        finally:
            cap.release()

    else:
        if not os.path.exists(source):
            raise FileNotFoundError(f"The specified image file path does not exist: '{source}'")
        
        image = cv2.imread(source)

        if image is None:
            raise ValueError(f"Failed to decode the image. The file at '{source}' may be corrupted.")
        
        return image
    