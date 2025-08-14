# Propify - Smart Property Price Estimator

Propify adalah aplikasi web cerdas yang dapat memprediksi harga properti di wilayah Jabodetabek berdasarkan fitur-fitur spesifik. Proyek ini menggunakan model machine learning yang telah dilatih untuk memberikan estimasi harga yang akurat dan informatif.

![Demo Aplikasi](sementara aplikasi dimatikan untuk menghemat biaya, jika ingin melihat demo aplikasi, hubungi 089609656714 atau instagram @mashivee - terimakasih :))

---

## 🌟 Fitur Utama

-   **Prediksi Harga Real-time**: Masukkan detail properti (luas tanah, jumlah kamar, lokasi, dll.) dan dapatkan estimasi harga secara instan.
-   **Analisis Faktor Harga**: Dapatkan wawasan tentang faktor-faktor utama yang paling mempengaruhi harga properti Anda (misalnya, lokasi premium, bangunan baru).
-   **Dropdown Dinamis**: Antarmuka pengguna yang interaktif dengan pilihan kota dan kecamatan yang saling terkait.
-   **Deployment Otomatis**: Di-deploy di AWS Elastic Beanstalk dengan pipeline CI/CD menggunakan AWS CodePipeline untuk pembaruan yang lancar.

---

## 💻 Teknologi yang Digunakan

-   **Backend**: Flask (Python)
-   **Frontend**: HTML, CSS, Bootstrap 5
-   **Machine Learning**: Scikit-learn, Pandas, Joblib, XGBoost
-   **Deployment**: AWS Elastic Beanstalk, AWS CodePipeline, Gunicorn

---

## 📂 Struktur Proyek

Berikut adalah struktur file dan direktori penting dalam proyek ini:

.
├── .ebextensions/      # Direktori untuk konfigurasi spesifik AWS Elastic Beanstalk
├── .github/            # (Opsional) Direktori untuk workflow GitHub Actions
├── data/               # Direktori untuk dataset (raw & processed)
│   └── raw/
├── model/              # Direktori untuk menyimpan file model machine learning (.joblib)
│   └── model.joblib
├── notebooks/          # Direktori untuk Jupyter Notebooks (eksplorasi & pemodelan)
├── static/             # Direktori untuk file statis (CSS, JavaScript, Gambar)
├── templates/          # Direktori untuk file HTML (Jinja2)
│   ├── index.html
│   └── predictor.html
├── .gitignore          # File untuk mengabaikan file/folder yang tidak perlu di-commit
├── app.py              # File utama aplikasi Flask (logika backend & routing)
├── Procfile            # Perintah untuk memberitahu server cara menjalankan aplikasi
├── README.md           # File ini (dokumentasi proyek)
└── requirements.txt    # Daftar semua dependensi Python yang dibutuhkan


---

## 🚀 Menjalankan Proyek Secara Lokal

Untuk menjalankan aplikasi ini di komputer Anda, ikuti langkah-langkah berikut:

1.  **Clone repositori ini:**
    ```bash
    git clone [https://github.com/Farmil23/Propify-Smart-Property-Price-Estimator.git](https://github.com/Farmil23/Propify-Smart-Property-Price-Estimator.git)
    cd Propify-Smart-Property-Price-Estimator
    ```

2.  **Buat dan aktifkan virtual environment:**
    ```bash
    # Untuk Mac/Linux
    python3 -m venv venv
    source venv/bin/activate

    # Untuk Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install semua dependensi:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Jalankan aplikasi Flask:**
    ```bash
    flask run
    ```

5.  Buka browser Anda dan akses `http://127.0.0.1:5000`

---

## ☁️ Info Deployment

Aplikasi ini di-deploy secara otomatis ke **AWS Elastic Beanstalk** menggunakan **AWS CodePipeline**. Setiap `push` ke branch `main` akan memicu pipeline untuk mengambil kode terbaru dan men-deploy-nya ke lingkungan production.

---

## 📄 Lisensi

Proyek ini dilisensikan di bawah [MIT License](LICENSE).

---

Dibuat dengan ❤️ oleh **Farhan kamil hermansyah**.
