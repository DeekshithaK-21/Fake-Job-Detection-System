import pandas as pd
import numpy as np
from distilbert_embedder import get_embedding

# ---------------- LOAD DATA ----------------
train_df = pd.read_csv("data/processed/train.csv")
test_df = pd.read_csv("data/processed/test.csv")

train_texts = train_df["text"].tolist()
test_texts = test_df["text"].tolist()

y_train = train_df["label"].values
y_test = test_df["label"].values

print("📊 Train size:", len(train_texts))
print("📊 Test size:", len(test_texts))

# ---------------- GENERATE EMBEDDINGS ----------------
print("\n🔥 Generating TRAIN embeddings...")
X_train = get_embedding(train_texts)

print("\n🔥 Generating TEST embeddings...")
X_test = get_embedding(test_texts)

# ---------------- SAVE ----------------
np.save("data/processed/X_train.npy", X_train)
np.save("data/processed/X_test.npy", X_test)
np.save("data/processed/y_train.npy", y_train)
np.save("data/processed/y_test.npy", y_test)

print("\n✅ Embeddings saved successfully!")
print("X_train shape:", X_train.shape)
print("X_test shape:", X_test.shape)