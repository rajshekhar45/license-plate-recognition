import cv2
import easyocr
import numpy as np

# ✅ Initialize once (safe)
reader = easyocr.Reader(['en'], gpu=False)

def extract_plate(image_path):
    try:
        print(f"[DEBUG] Loading image: {image_path}")

        img = cv2.imread(image_path)
        if img is None:
            return "Image not loaded❌"

        img = cv2.resize(img, (600, 400))

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.bilateralFilter(gray, 11, 17, 17)
        edges = cv2.Canny(gray, 30, 200)

        # Handle OpenCV versions
        contours_info = cv2.findContours(edges.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = contours_info[0] if len(contours_info) == 2 else contours_info[1]

        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

        plate_img = None

        # 🔥 Try to detect plate region
        for contour in contours:
            perimeter = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)

            # relaxed condition (not strictly 4)
            if 4 <= len(approx) <= 6:
                x, y, w, h = cv2.boundingRect(contour)

                # basic size filter
                if w > 100 and h > 30:
                    plate_img = img[y:y+h, x:x+w]
                    break

        # 🔥 fallback (very important)
        if plate_img is None:
            print("[DEBUG] Using full image for OCR")
            plate_img = img

        print("[DEBUG] Running EasyOCR...")

        result = reader.readtext(plate_img)

        if not result:
            return "Text not detected❌"

        # Extract best text
        text = " ".join([res[1] for res in result])

        # Clean text
        text = "".join(e for e in text if e.isalnum())

        print(f"[DEBUG] OCR Output: {text}")

        return text if text else "No valid plate❌"

    except Exception as e:
        return f"Error: {str(e)}❌"
