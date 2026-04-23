import re
import emoji
import nltk
from nltk.stem import WordNetLemmatizer

# ---------------- NLTK SETUP ----------------
# Ensure required resources are available (avoids runtime errors in Flask)
try:
    nltk.data.find('corpora/wordnet')
except:
    nltk.download('wordnet')

# Initialize lemmatizer
lemmatizer = WordNetLemmatizer()


# ---------------- HELPER FUNCTION ----------------
def normalize_repeated_chars(text):
    """
    Normalize repeated alphabetic characters.

    Example:
    "goooood" → "good"

    Note:
    Only letters are normalized, numbers are left unchanged.
    """
    return re.sub(r'([a-zA-Z])\1{2,}', r'\1\1', text)


# ---------------- MAIN CLEANING FUNCTION ----------------
def clean_text(text):
    """
    Perform comprehensive text preprocessing for job postings.

    This function is designed to be:
    ✔ OCR-safe
    ✔ Numeric-safe
    ✔ Suitable for ML models

    Steps included:
    1. Lowercasing
    2. Emoji removal
    3. Repeated character normalization
    4. URL removal
    5. Currency symbol removal
    6. OCR number correction
    7. Special character removal
    8. Tokenization
    9. Lemmatization
    """

    # 1. Convert text to lowercase
    text = text.lower()

    # 2. Remove emojis (important for noisy inputs)
    text = emoji.replace_emoji(text, replace='')

    # 3. Normalize repeated letters (e.g., "goooood" → "good")
    text = normalize_repeated_chars(text)

    # 4. Remove URLs (http, https, www)
    text = re.sub(r'http\S+|www\S+', '', text)

    # 5. Remove currency symbols (₹, $, €, £)
    text = re.sub(r'[₹$€£]', '', text)

    # 6. Fix OCR-split numbers (e.g., "50 000" → "50000")
    text = re.sub(r'(?<=\d)\s+(?=\d)', '', text)

    # 7. Remove commas inside numbers (e.g., "50,000" → "50000")
    text = re.sub(r'(?<=\d),(?=\d)', '', text)

    # 8. Remove special characters (keep letters, numbers, space, !)
    text = re.sub(r'[^a-z0-9\s!]', ' ', text)

    # 9. Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()

    # 10. Tokenization (fast split instead of nltk word_tokenize)
    tokens = text.split()

    # 11. Lemmatization (convert words to base form)
    tokens = [lemmatizer.lemmatize(token) for token in tokens]

    # 12. Join tokens back into cleaned text
    return " ".join(tokens)


# ---------------- TEST BLOCK ----------------
if __name__ == "__main__":
    sample = "🔥 Earn ₹50,000 per month!!! No interview!!! Data entry job 😍😍"
    print(clean_text(sample))
