import numpy as np
import xgboost as xgb
import joblib
import os
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

print("🚀 Starting XGBoost Training Pipeline...\n")

# ---------------- LOAD DATA ----------------
print("📂 Loading embeddings...")

X_train = np.load("data/processed/X_train.npy")
X_test = np.load("data/processed/X_test.npy")
y_train = np.load("data/processed/y_train.npy")
y_test = np.load("data/processed/y_test.npy")

print("✅ Data Loaded Successfully!")
print(f"X_train shape: {X_train.shape}")
print(f"X_test shape: {X_test.shape}")
print(f"y_train distribution: {np.bincount(y_train)}")
print(f"y_test distribution: {np.bincount(y_test)}\n")

# ---------------- MODEL INIT ----------------
print("⚙️ Initializing XGBoost model...")

model = xgb.XGBClassifier(
    n_estimators=300,
    max_depth=6,
    learning_rate=0.05,
    scale_pos_weight=1.4,
    eval_metric='logloss',
    verbosity=1
)

print("✅ Model initialized!\n")

# ---------------- TRAIN ----------------
print("🏋️ Training model...")

model.fit(X_train, y_train)

print("✅ Training completed!\n")

# ---------------- PREDICT ----------------
print("🔍 Running predictions...")

y_pred = model.predict(X_test)

print("✅ Predictions completed!\n")

# ---------------- EVALUATION ----------------
print("📊 Evaluating model performance...\n")

accuracy = accuracy_score(y_test, y_pred)

print(f"🎯 Accuracy: {accuracy:.4f}\n")

print("📄 Classification Report:")
print(classification_report(y_test, y_pred))

print("📌 Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# ---------------- SAVE MODEL ----------------
print("\n💾 Saving model...")

os.makedirs("models/saved_models", exist_ok=True)

joblib.dump(model, "models/saved_models/xgboost_model.pkl")

print("✅ Model saved successfully at: models/saved_models/xgboost_model.pkl\n")

print("🎉 DONE! Your model is ready for prediction.")