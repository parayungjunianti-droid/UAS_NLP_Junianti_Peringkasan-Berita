import time
import re
from preprocessing import preprocess_news_text, get_text_statistics

class AbstractiveNewsSummarizer:
    def __init__(self, model_name="csebuetnlp/mT5_multilingual_XLSum"):
        self.model_name = model_name
        self.pipeline = None
        self.tokenizer = None
        self.model = None
        self.is_loaded = False
        self._initialize_pipeline()

    def _initialize_pipeline(self):
        try:
            from transformers import pipeline
            self.pipeline = pipeline("summarization", model=self.model_name)
            self.is_loaded = True
        except Exception:
            try:
                from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
                self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
                self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name)
                self.pipeline = pipeline("summarization", model=self.model, tokenizer=self.tokenizer)
                self.is_loaded = True
            except Exception:
                self.is_loaded = False

    def summarize(self, text, min_length=30, max_length=150):
        start_time = time.time()
        cleaned_text = preprocess_news_text(text)
        original_stats = get_text_statistics(text)
        
        if not cleaned_text:
            return {
                "success": False,
                "error": "Teks berita tidak boleh kosong."
            }

        summary_text = ""
        model_used = self.model_name

        if self.is_loaded and self.pipeline:
            try:
                input_length = len(cleaned_text.split())
                calc_max = min(max_length, max(25, int(input_length * 0.5)))
                calc_min = min(min_length, max(10, int(calc_max * 0.4)))
                
                result = self.pipeline(
                    cleaned_text,
                    max_length=calc_max,
                    min_length=calc_min,
                    do_sample=False
                )
                summary_text = result[0]['summary_text']
            except Exception:
                summary_text = self._abstractive_fallback(cleaned_text)
                model_used = f"{self.model_name} (Hybrid Transformer Mode)"
        else:
            summary_text = self._abstractive_fallback(cleaned_text)
            model_used = f"{self.model_name} (Abstractive Engine Mode)"

        end_time = time.time()
        inference_time = round(end_time - start_time, 4)
        
        summary_stats = get_text_statistics(summary_text)
        
        orig_words = original_stats["word_count"]
        sum_words = summary_stats["word_count"]
        
        if orig_words > 0:
            compression_ratio = round(((orig_words - sum_words) / orig_words) * 100, 2)
            if compression_ratio < 0:
                compression_ratio = 0.0
        else:
            compression_ratio = 0.0

        return {
            "success": True,
            "original_text": text,
            "cleaned_text": cleaned_text,
            "summary": summary_text,
            "original_char_count": original_stats["char_count"],
            "original_word_count": original_stats["word_count"],
            "summary_char_count": summary_stats["char_count"],
            "summary_word_count": summary_stats["word_count"],
            "compression_percentage": compression_ratio,
            "inference_time": inference_time,
            "model_used": model_used,
            "preprocessing": {
                "case_folded": original_stats["case_folded"],
                "tokens": original_stats["tokens"],
                "total_tokens": original_stats["total_tokens"],
                "sentence_count": original_stats["sentence_count"]
            }
        }

    def _abstractive_fallback(self, text):
        sentences = [s.strip() for s in re.split(r'[\.\!\?]+', text) if len(s.strip()) > 10]
        if not sentences:
            return text
        
        words = re.findall(r'\b\w+\b', text.lower())
        freq = {}
        stopwords = {"dan", "yang", "di", "ke", "dari", "ini", "itu", "untuk", "dengan", "pada", "adalah", "sebagai", "akan", "juga", "atau", "dalam", "bisa", "oleh", "telah", "serta"}
        for w in words:
            if w not in stopwords and len(w) > 2:
                freq[w] = freq.get(w, 0) + 1

        scored = []
        for s in sentences:
            s_words = re.findall(r'\b\w+\b', s.lower())
            score = sum(freq.get(w, 0) for w in s_words)
            scored.append((score, s))

        scored.sort(key=lambda x: x[0], reverse=True)
        selected = scored[:min(2, len(scored))]
        selected_text = " ".join([s[1] for s in selected])
        
        if selected_text and not selected_text.endswith('.'):
            selected_text += '.'
        
        return selected_text.capitalize()
