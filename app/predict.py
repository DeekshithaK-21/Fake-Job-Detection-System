# app/predict.py

from models.xgboost_model import predict_job
from models.explainability import highlight_words
from models.rules import rule_score
from preprocessing.text_cleaner import clean_text
from app.input_handler import get_text


def predict_pipeline(input_data, input_type="text"):
    """
    Hybrid prediction pipeline (optimized & stable)
    """

    # ---------------- STEP 1: TEXT EXTRACTION ----------------
    if input_type == "text":
        raw_text = input_data
    else:
        raw_text = get_text(input_data, input_type)
    print("DEBUG TEXT:", raw_text)
    # ---------------- HANDLE EMPTY OCR ----------------
    if not raw_text or not raw_text.strip():
        return {
            "prediction": "Fake",
            "confidence": {"real": 0.2, "fake": 0.8},
            "suspicious_words": ["No readable text detected"],
            "raw_text": raw_text
        }

    # ---------------- STEP 2: CLEANING ----------------
    cleaned = clean_text(raw_text)

    # Limit length for speed
    cleaned = cleaned[:500]

    # ---------------- STEP 3: ML PREDICTION ----------------
    pred, prob = predict_job(cleaned)

    prob_real = float(prob[0])
    prob_fake = float(prob[1])

    # ---------------- STEP 4: EXPLAINABILITY ----------------
    suspicious_words = highlight_words(cleaned)

    # ---------------- STEP 5: RULE SCORE ----------------
    score = rule_score(raw_text)
    normalized_score = min(score / 5, 1.0)
    alpha = 0.6

    # ---------------- PROBABILITY ADJUSTMENT ----------------
    adjusted_fake = prob_fake + (alpha * normalized_score)
    adjusted_fake = min(adjusted_fake, 1.0)
    adjusted_real = 1 - adjusted_fake

    # ---------------- FINAL DECISION ----------------
    final_prediction = "Fake" if adjusted_fake > 0.5 else "Real"

    # ---------------- OUTPUT ----------------
    return {
        "prediction": final_prediction,
        "confidence": {
            "real": round(adjusted_real, 4),
            "fake": round(adjusted_fake, 4)
        },
        "suspicious_words": suspicious_words,
        "raw_text": raw_text
    }