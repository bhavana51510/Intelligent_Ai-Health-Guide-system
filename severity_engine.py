# severity_engine.py

MINOR_IMAGE_CLASSES = ["abrasion", "rash"]
MODERATE_IMAGE_CLASSES = ["cut", "burn", "bruise"]

MINOR_KEYWORDS = [
    "small",
    "minor",
    "slight",
    "little",
    "not deep",
    "surface",
    "light burn",
    "scratch"
]

SEVERE_KEYWORDS = [
    "deep",
    "bleeding heavily",
    "severe pain",
    "swelling badly",
    "pus",
    "infection",
    "fracture"
]


def is_minor_case(image_pred=None, image_conf=0, text=""):
    text = text.lower() if text else ""

    # 1️⃣ Severe override rule
    for word in SEVERE_KEYWORDS:
        if word in text:
            return False

    # 2️⃣ Image-based minor detection
    if image_pred in MINOR_IMAGE_CLASSES and image_conf >= 0.80:
        return True

    # 3️⃣ Cut/Burn special logic
    if image_pred in MODERATE_IMAGE_CLASSES and image_conf >= 0.85:
        if not any(word in text for word in SEVERE_KEYWORDS):
            return True

    # 4️⃣ Keyword-based minor detection
    for word in MINOR_KEYWORDS:
        if word in text:
            return True

    return False