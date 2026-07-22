import os
from flask import Flask, render_template, request, jsonify
from summarizer import AbstractiveNewsSummarizer
from evaluation import run_dataset_evaluation
from utils import SAMPLE_NEWS_LIST

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret-key-nlp-uas-2026'

summarizer = AbstractiveNewsSummarizer(model_name="csebuetnlp/mT5_multilingual_XLSum")

@app.route('/')
def index():
    return render_template('index.html', sample_news=SAMPLE_NEWS_LIST)

@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.get_json() or {}
    text = data.get('text', '').strip()
    
    if not text:
        return jsonify({
            'success': False,
            'error': 'Teks berita tidak boleh kosong. Silakan masukkan teks berita terlebih dahulu.'
        }), 400

    if len(text) < 50:
        return jsonify({
            'success': False,
            'error': 'Teks berita terlalu pendek. Minimal panjang teks adalah 50 karakter.'
        }), 400

    min_len = int(data.get('min_length', 30))
    max_len = int(data.get('max_length', 150))

    result = summarizer.summarize(text, min_length=min_len, max_length=max_len)
    
    if not result.get('success'):
        return jsonify(result), 500

    return jsonify(result), 200

@app.route('/evaluation')
def evaluation():
    dataset_path = os.path.join(app.root_path, 'dataset', 'news_dataset.csv')
    eval_data = run_dataset_evaluation(dataset_path, summarizer)
    return render_template('evaluation.html', eval_data=eval_data)

@app.route('/documentation')
def documentation():
    return render_template('documentation.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
