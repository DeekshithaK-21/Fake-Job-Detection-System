# 🧠 Fake Job Post Detection System

A machine learning-powered web application that detects **fraudulent job postings** from text, images, or PDFs using **OCR + NLP + XGBoost**.

---

## 🚀 Features

* 📄 **Text Input Analysis**
* 🖼️ **Image OCR Detection**
* 📑 **PDF Job Post Analysis**
* 🤖 **ML Model (XGBoost) for Fraud Detection**
* ⚠️ **Suspicious Keyword Highlighting**
* 📊 **Confidence Score Visualization**
* 🌐 **Web Interface (Flask)**

---

## 🏗️ Project Structure

```
FakeJobDetection/
│
├── app/                    # Flask backend (routes, main app)
├── models/                 # ML model files
│   └── saved_models/
│       └── xgboost_model.pkl
├── ocr/                    # OCR logic (image + PDF)
├── preprocessing/          # Text cleaning & NLP
├── templates/              # HTML UI
├── static/                 # CSS / assets
├── uploads/                # Temporary uploaded files
├── requirements.txt
├── build.sh                # (for deployment)
├── Procfile                # (for deployment)
└── README.md
```

---

## ⚙️ Installation (Local Setup)

### 1️⃣ Clone the Repository

```
git clone https://github.com/DeekshithaK-21/Fake-Job-Detection-System.git
cd Fake-Job-Detection-System
```

---

### 2️⃣ Create Virtual Environment

```
python -m venv tf_env
```

#### Activate:

**Windows**

```
tf_env\Scripts\activate
```

**Mac/Linux**

```
source tf_env/bin/activate
```

---

### 3️⃣ Install Dependencies

```
pip install -r requirements.txt
```

---

## 🔍 OCR Setup (IMPORTANT)

This project uses **Tesseract OCR**.

### 📥 Install Tesseract

Download from:
https://github.com/UB-Mannheim/tesseract/wiki

---

### 🛠️ Windows Users Only

Add path in:

```
ocr/image_ocr.py
```

```python
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
```

---

## ▶️ Run the Application

```
python -m app.main
```

---

## 🌐 Open in Browser

```
http://127.0.0.1:5000
```

---

## 🤖 Model Information

* Model: **XGBoost Classifier**
* Input: Cleaned job description text
* Output:

  * ✅ Real Job
  * ❌ Fake Job
* Also provides:

  * Confidence score
  * Suspicious words

---

## 📦 Important Notes

* ✔ Pre-trained model included:

  ```
  models/saved_models/xgboost_model.pkl
  ```
* ❌ No need to train model again
* ❌ Dataset not required to run app

---

## ⚠️ NLTK Setup (Auto Handled)

Required resource:

```
wordnet
```

Installed automatically during setup.

---

## 🧪 Example Inputs

Try:

* "Earn ₹50,000/week without interview"
* "Work from home data entry job, no experience needed"

---

## 🚀 Deployment

Supports:

* Render (lightweight version)
* Hugging Face Spaces (full ML version)
* Railway / Cloud platforms

---

## 🧠 Tech Stack

* **Backend:** Flask
* **ML Model:** XGBoost
* **OCR:** Tesseract
* **NLP:** NLTK
* **Image Processing:** OpenCV
* **PDF Processing:** pdfplumber

---

## 📌 Future Improvements

* 🔍 Better fraud keyword detection
* 📊 Dashboard analytics
* ⚡ Faster inference pipeline
* 📱 Mobile-friendly UI

---

## 👩‍💻 Author

**Deekshitha K**
GitHub: https://github.com/DeekshithaK-21

---

## ⭐ If you like this project

Give it a ⭐ on GitHub!

