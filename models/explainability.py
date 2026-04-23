SUSPICIOUS_WORDS = [
    "urgent", "limited seats", "registration fee",
    "guaranteed job", "work from home", "earn money",
    "no experience required", "whatsapp", "call now",
    "click here", "apply immediately"
]

def highlight_words(text):
    found = []
    text_lower = text.lower()

    for word in SUSPICIOUS_WORDS:
        if word in text_lower:
            found.append(word)

    return found