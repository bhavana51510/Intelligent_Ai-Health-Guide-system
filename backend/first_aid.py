# backend/first_aid.py

FIRST_AID_GUIDE = {

    # ---------------- TEXT SYMPTOMS ----------------
    "eye pain": [
        "Avoid rubbing your eyes",
        "Rinse eyes gently with clean water",
        "Rest your eyes and avoid screens",
        "Use prescribed eye drops if available"
    ],

    "headache": [
        "Rest in a quiet, dark room",
        "Drink sufficient water",
        "Apply a cold or warm compress",
        "Avoid loud noises and bright light"
    ],

    "fever": [
        "Drink plenty of fluids",
        "Take adequate rest",
        "Use a damp cloth to cool the body",
        "Monitor temperature regularly"
    ],

    "cough": [
        "Drink warm fluids",
        "Use honey (if not allergic)",
        "Avoid cold air exposure",
        "Rest your throat"
    ],

    "throat pain": [
        "Gargle with warm salt water",
        "Drink warm fluids",
        "Avoid very cold foods",
        "Rest your voice"
    ],

    # ---------------- IMAGE INJURIES ----------------
    "abrasion": [
        "Clean the wound with clean water",
        "Apply antiseptic solution",
        "Cover with sterile bandage",
        "Keep area clean and dry"
    ],

    "cut": [
        "Apply gentle pressure to stop bleeding",
        "Clean with antiseptic",
        "Apply sterile bandage",
        "Seek medical help if bleeding persists"
    ],

    "burn": [
        "Cool the burn under running water for 10 minutes",
        "Do NOT apply ice directly",
        "Cover loosely with sterile cloth",
        "Avoid applying oil or toothpaste"
    ],

    "rash": [
        "Keep the area clean and dry",
        "Avoid scratching",
        "Apply mild soothing cream",
        "Wear loose cotton clothing"
    ],

    "bruise": [
        "Apply cold compress for 10–15 minutes",
        "Rest the affected area",
        "Elevate if swollen",
        "Avoid applying pressure"
    ]
}


def show_first_aid(user_input):
    """
    Works for:
    - Full symptom sentences
    - Single injury labels
    - Partial keyword matches
    """

    if not user_input:
        print("\n🩹 No first aid information available.")
        return

    text = user_input.lower().strip()

    # 1️⃣ Direct exact match
    if text in FIRST_AID_GUIDE:
        print("\n🩹 First Aid Steps:")
        for step in FIRST_AID_GUIDE[text]:
            print("-", step)
        return

    # 2️⃣ Keyword match inside sentence
    for key in FIRST_AID_GUIDE:
        if key in text:
            print("\n🩹 First Aid Steps:")
            for step in FIRST_AID_GUIDE[key]:
                print("-", step)
            return

    print("\n🩹 No specific first aid guide available for this case.")