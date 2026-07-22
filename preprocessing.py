import re

def case_folding(text):
    if not text:
        return ""
    return text.lower()

def normalize_whitespace(text):
    if not text:
        return ""
    return re.sub(r'\s+', ' ', text).strip()

def remove_unwanted_characters(text):
    if not text:
        return ""
    cleaned = re.sub(r'[\r\n\t]', ' ', text)
    cleaned = re.sub(r'[^\w\s\.\,\!\?\-\"\']', '', cleaned)
    return normalize_whitespace(cleaned)

def preprocess_news_text(text):
    if not text:
        return ""
    folded = case_folding(text)
    normalized = normalize_whitespace(folded)
    cleaned = remove_unwanted_characters(normalized)
    return cleaned

def tokenize_text(text):
    if not text:
        return []
    cleaned = preprocess_news_text(text)
    tokens = re.findall(r'\b\w+\b', cleaned)
    return tokens

def get_sentence_length(text):
    if not text:
        return 0
    sentences = [s.strip() for s in re.split(r'[\.\!\?]+', text) if s.strip()]
    return len(sentences)

def get_text_statistics(text):
    cleaned = preprocess_news_text(text)
    tokens = tokenize_text(cleaned)
    char_count = len(text) if text else 0
    word_count = len(tokens)
    sentence_count = get_sentence_length(text)
    return {
        "case_folded": cleaned,
        "tokens": tokens[:20],
        "total_tokens": word_count,
        "char_count": char_count,
        "word_count": word_count,
        "sentence_count": sentence_count
    }
