import torch
import numpy as np
from transformers import DistilBertTokenizer, DistilBertModel

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

tokenizer = None
model = None

def load_model():
    global tokenizer, model

    if tokenizer is None or model is None:
        print("🚀 Loading DistilBERT...")

        tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")
        model = DistilBertModel.from_pretrained("distilbert-base-uncased")

        model.to(device)
        model.eval()

        print("✅ Model ready!")

    return tokenizer, model


def get_single_embedding(text, max_length=128):

    tokenizer, model = load_model()

    # 🔥 LIMIT TEXT (BIG SPEED BOOST)
    text = text

    with torch.no_grad():
        inputs = tokenizer(
            text,
            truncation=True,
            padding=True,
            max_length=max_length,
            return_tensors="pt"
        ).to(device)

        outputs = model(**inputs)

        embedding = outputs.last_hidden_state[:, 0, :]

    return embedding.cpu().numpy()