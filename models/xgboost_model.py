import joblib
import os
from embeddings.distilbert_embedder import get_single_embedding

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "saved_models", "xgboost_model.pkl")

model = None

def load_model():
    global model
    if model is None:
        print("Loading model from:", MODEL_PATH)
        model = joblib.load(MODEL_PATH)

def predict_job(text):
    load_model()   # 🔥 safe lazy loading
    emb = get_single_embedding(text)
    pred = model.predict(emb)[0]
    prob = model.predict_proba(emb)[0]
    return pred, prob