# models/rules.py

import re

def rule_score(text):
    text = text.lower()
    score = 0

    # ---------------- BASIC SCAM KEYWORDS ----------------
    basic_keywords = [
        "work from home",
        "earn money",
        "income potential",
        "no experience",
        "part time",
        "easy job",
        "guaranteed",
        "smartphone",
        "call now",
        "limited seats",
        "apply fast"
    ]

    score += sum(1 for k in basic_keywords if k in text)

    # ---------------- SALARY DETECTION ----------------
    salary_matches = re.findall(r'\b\d{4,}\b', text)

    high_salary_flag = False

    for s in salary_matches:
        val = int(s)

        # High salary threshold
        if val >= 50000:
            score += 1
            high_salary_flag = True

        # Very high salary
        if val >= 100000:
            score += 2
            high_salary_flag = True

    # Lakhs detection
    if "lakh" in text or "lakhs" in text:
        score += 2
        high_salary_flag = True

    # ---------------- SHORT TIME HIGH PAY ----------------
    if "per week" in text or "per day" in text:
        if high_salary_flag:
            score += 2   # strong suspicion

    # ---------------- LOW EFFORT + HIGH PAY ----------------
    easy_keywords = [
        "no experience",
        "2 hours",
        "3 hours",
        "few hours",
        "simple work",
        "data entry",
        "typing job"
    ]

    if high_salary_flag and any(k in text for k in easy_keywords):
        score += 2

    # ---------------- PAYMENT / FEE SCAM ----------------
    fee_keywords = [
        "processing fee",
        "registration fee",
        "pay fee",
        "security deposit",
        "advance payment",
        "registration charges",
        "payment required",
        "pay amount",
        "send money"
    ]

    if any(k in text for k in fee_keywords):
        score += 3  # very strong fraud signal

    # ---------------- INFORMAL APPLY (DM / WHATSAPP) ----------------
    dm_keywords = [
        "dm your resume",
        "dm resume",
        "send resume on whatsapp",
        "contact on whatsapp",
        "apply via whatsapp",
        "message me",
        "telegram"
    ]

    if any(k in text for k in dm_keywords):
        score += 2

    # ---------------- URGENCY SCAM ----------------
    urgency_keywords = [
        "urgent hiring",
        "limited slots",
        "only today",
        "join immediately",
        "hurry up"
    ]

    if any(k in text for k in urgency_keywords):
        score += 1

    return score