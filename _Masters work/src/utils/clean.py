import re

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)  # убираем мусор
    text = re.sub(r'\s+', ' ', text)
    return text