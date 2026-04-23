import joblib
import os
from embeddings.distilbert_embedder import get_single_embedding

# Safe path (no errors later)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "saved_models", "xgboost_model.pkl")

model = joblib.load(MODEL_PATH)


def predict_job(text):
    emb = get_single_embedding(text)
    pred = model.predict(emb)[0]
    prob = model.predict_proba(emb)[0]
    return pred, prob