document.addEventListener('DOMContentLoaded', function () {
    const newsForm = document.getElementById('news-form');
    const newsInput = document.getElementById('news-input');
    const btnSummarize = document.getElementById('btn-summarize');
    const btnSample = document.getElementById('btn-sample');
    const btnClear = document.getElementById('btn-clear');
    const loadingOverlay = document.getElementById('loading-overlay');
    const resultCard = document.getElementById('result-card');
    const notificationContainer = document.getElementById('notification-container');

    const sampleNewsText = "Pemerintah Republik Indonesia melalui Kementerian Komunikasi dan Informatika secara resmi meresmikan Pusat Riset Kecerdasan Buatan (AI Research Center) nasional di Jakarta. Fasilitas ini didirikan untuk mendorong inovasi riset teknologi mutakhir serta mempercepat transformasi digital di berbagai sektor publik dan industri. Menteri Kominfo menyampaikan bahwa pusat riset ini akan berkolaborasi dengan berbagai perguruan tinggi terkemuka dan perusahaan teknologi global. Diharapkan fasilitas ini dapat menghasilkan talenta digital yang berdaya saing internasional serta menciptakan solusi berbasis AI untuk permasalahan nasional.";

    function showNotification(message, type = 'success') {
        if (!notificationContainer) return;
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type === 'success' ? 'warning' : 'danger'} alert-dismissible fade show border-0 shadow-sm rounded-4`;
        alertDiv.role = 'alert';
        alertDiv.innerHTML = `
            <div class="d-flex align-items-center gap-2">
                <i class="bi bi-${type === 'success' ? 'check-circle-fill' : 'exclamation-triangle-fill'} fs-5"></i>
                <span class="fw-semibold">${message}</span>
            </div>
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        `;
        notificationContainer.appendChild(alertDiv);
        setTimeout(() => {
            alertDiv.remove();
        }, 5000);
    }

    if (btnSample && newsInput) {
        btnSample.addEventListener('click', function () {
            newsInput.value = sampleNewsText;
            showNotification('Contoh berita berhasil dimasukkan ke dalam form.', 'success');
        });
    }

    if (btnClear && newsInput) {
        btnClear.addEventListener('click', function () {
            newsInput.value = '';
            if (resultCard) {
                resultCard.style.display = 'none';
            }
            showNotification('Form dan hasil ringkasan berhasil dibersihkan.', 'success');
        });
    }

    if (newsForm) {
        newsForm.addEventListener('submit', function (e) {
            e.preventDefault();
            const text = newsInput.value.trim();

            if (!text) {
                showNotification('Silakan masukkan teks berita terlebih dahulu.', 'error');
                newsInput.focus();
                return;
            }

            if (text.length < 50) {
                showNotification('Teks berita terlalu pendek! Minimal panjang teks adalah 50 karakter.', 'error');
                newsInput.focus();
                return;
            }

            if (loadingOverlay) loadingOverlay.style.display = 'flex';
            if (btnSummarize) btnSummarize.disabled = true;

            fetch('/summarize', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    text: text,
                    min_length: 30,
                    max_length: 150
                })
            })
                .then(response => response.json())
                .then(data => {
                    if (loadingOverlay) loadingOverlay.style.display = 'none';
                    if (btnSummarize) btnSummarize.disabled = false;

                    if (data.success) {
                        renderResults(data);
                        showNotification('Proses ringkasan berita berhasil dilakukan!', 'success');
                    } else {
                        showNotification(data.error || 'Terjadi kesalahan saat meringkas berita.', 'error');
                    }
                })
                .catch(error => {
                    if (loadingOverlay) loadingOverlay.style.display = 'none';
                    if (btnSummarize) btnSummarize.disabled = false;
                    showNotification('Gagal terhubung ke server backend.', 'error');
                });
        });
    }

    function renderResults(data) {
        if (!resultCard) return;

        document.getElementById('res-original-text').innerText = data.original_text;
        document.getElementById('res-original-char').innerText = data.original_char_count + ' Karakter';
        document.getElementById('res-original-word').innerText = data.original_word_count + ' Kata';
        document.getElementById('res-summary-text').innerText = data.summary;
        document.getElementById('res-compression').innerText = data.compression_percentage + '%';
        document.getElementById('res-inference-time').innerText = data.inference_time + ' Detik';
        document.getElementById('res-model-used').innerText = data.model_used;

        if (data.preprocessing) {
            document.getElementById('prep-case-folding').innerText = data.preprocessing.case_folded;
            document.getElementById('prep-total-tokens').innerText = data.preprocessing.total_tokens + ' Token';
            document.getElementById('prep-sentence-count').innerText = data.preprocessing.sentence_count + ' Kalimat';

            const tokensContainer = document.getElementById('prep-tokens-list');
            if (tokensContainer) {
                tokensContainer.innerHTML = '';
                data.preprocessing.tokens.forEach(token => {
                    const badge = document.createElement('span');
                    badge.className = 'badge bg-light text-dark border me-1 mb-1 font-monospace fw-normal';
                    badge.innerText = token;
                    tokensContainer.appendChild(badge);
                });
            }
        }

        resultCard.style.display = 'block';
        resultCard.scrollIntoView({ behavior: 'smooth' });
    }

    const btnCopy = document.getElementById('btn-copy');
    if (btnCopy) {
        btnCopy.addEventListener('click', function () {
            const summaryText = document.getElementById('res-summary-text').innerText;
            if (!summaryText) return;

            navigator.clipboard.writeText(summaryText)
                .then(() => {
                    showNotification('Teks ringkasan berhasil disalin ke clipboard!', 'success');
                })
                .catch(() => {
                    showNotification('Gagal menyalin teks ringkasan.', 'error');
                });
        });
    }

    const btnDownloadTxt = document.getElementById('btn-download-txt');
    if (btnDownloadTxt) {
        btnDownloadTxt.addEventListener('click', function () {
            const summaryText = document.getElementById('res-summary-text').innerText;
            if (!summaryText) return;

            const blob = new Blob([summaryText], { type: 'text/plain;charset=utf-8' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'ringkasan_berita.txt';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
            showNotification('File TXT ringkasan berhasil diunduh.', 'success');
        });
    }

    const btnDownloadPdf = document.getElementById('btn-download-pdf');
    if (btnDownloadPdf) {
        btnDownloadPdf.addEventListener('click', function () {
            const summaryText = document.getElementById('res-summary-text').innerText;
            const originalText = document.getElementById('res-original-text').innerText;
            const modelUsed = document.getElementById('res-model-used').innerText;
            if (!summaryText) return;

            const printWindow = window.open('', '_blank');
            printWindow.document.write(`
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Ringkasan Berita - NLP Summarizer</title>
                    <style>
                        body { font-family: sans-serif; padding: 40px; color: #0f172a; line-height: 1.6; }
                        h2 { color: #fbc02d; border-bottom: 2px solid #ffd54f; padding-bottom: 10px; }
                        .meta { background: #fff8e1; padding: 15px; border-radius: 8px; margin-bottom: 20px; font-size: 14px; }
                        .section { margin-bottom: 30px; }
                        .section h3 { color: #334155; }
                        .content { background: #f8fafc; padding: 15px; border-radius: 8px; border: 1px solid #e2e8f0; }
                    </style>
                </head>
                <body>
                    <h2>Laporan Ringkasan Berita Otomatis</h2>
                    <div class="meta">
                        <strong>Model:</strong> ${modelUsed}<br>
                        <strong>Tanggal:</strong> ${new Date().toLocaleDateString('id-ID')}
                    </div>
                    <div class="section">
                        <h3>Ringkasan Berita</h3>
                        <div class="content"><strong>${summaryText}</strong></div>
                    </div>
                    <div class="section">
                        <h3>Berita Asli</h3>
                        <div class="content">${originalText}</div>
                    </div>
                </body>
                </html>
            `);
            printWindow.document.close();
            printWindow.focus();
            setTimeout(() => {
                printWindow.print();
                printWindow.close();
            }, 500);
            showNotification('Dokumen PDF berhasil disiapkan untuk diunduh.', 'success');
        });
    }
});
