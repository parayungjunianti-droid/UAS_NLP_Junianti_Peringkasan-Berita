import os
import pandas as pd

SAMPLE_NEWS_LIST = [
    {
        "title": "Pusat Riset AI Nasional",
        "text": "Pemerintah Republik Indonesia melalui Kementerian Komunikasi dan Informatika secara resmi meresmikan Pusat Riset Kecerdasan Buatan (AI Research Center) nasional di Jakarta. Fasilitas ini didirikan untuk mendorong inovasi riset teknologi mutakhir serta mempercepat transformasi digital di berbagai sektor publik dan industri. Menteri Kominfo menyampaikan bahwa pusat riset ini akan berkolaborasi dengan berbagai perguruan tinggi terkemuka dan perusahaan teknologi global. Diharapkan fasilitas ini dapat menghasilkan talenta digital yang berdaya saing internasional serta menciptakan solusi berbasis AI untuk permasalahan nasional."
    },
    {
        "title": "Pertumbuhan Ekonomi Indonesia",
        "text": "Badan Pusat Statistik (BPS) melaporkan bahwa pertumbuhan ekonomi Indonesia pada kuartal ini mencatatkan tren positif sesuai dengan target pemerintah. Sektor konsumsi rumah tangga dan investasi menjadi penyumbang utama terhadap pertumbuhan ekonomi nasional. Kepala BPS menjelaskan bahwa stabilitas harga pangan dan inflasi yang terkendali memberikan dampak langsung terhadap daya beli masyarakat. Selain itu peningkatan aktivitas manufaktur dan ekspor komoditas utama turut memperkuat ketahanan ekonomi nasional di tengah ketidakpastian global."
    },
    {
        "title": "Peluncuran Satelit Komunikasi",
        "text": "Indonesia sukses meluncurkan satelit komunikasi generasi terbaru dari fasilitas peluncuran ruang angkasa. Satelit ini dirancang khusus untuk memperluas jangkauan internet pita lebar di daerah tertinggal, terdepan, dan terluar (3T). Direktur Utama penyedia layanan komunikasi menyatakan bahwa dengan beroperasinya satelit ini, fasilitas sekolah, pusat kesehatan masyarakat, dan kantor pemerintahan di pelosok Nusantara akan mendapatkan akses internet berkecepatan tinggi. Langkah ini diharapkan dapat memangkas kesenjangan digital di seluruh wilayah Indonesia."
    }
]

def load_dataset(dataset_path):
    if not os.path.exists(dataset_path):
        return pd.DataFrame()
    return pd.read_csv(dataset_path)

def get_random_sample():
    import random
    return random.choice(SAMPLE_NEWS_LIST)

def format_number(val):
    return f"{val:,}"
