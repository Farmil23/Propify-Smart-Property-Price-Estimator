from flask import Flask, render_template, request
import pandas as pd
import joblib
from datetime import datetime

app = Flask(__name__)

# --- Data Kecamatan per Kota (untuk dropdown dinamis) ---
KECAMATAN_DATA = {
    'Jakarta Selatan': ['Kebayoran Baru', 'Pondok Indah', 'Cilandak', 'Tebet', 'Setiabudi', 'Pasar Minggu', 'Kebayoran Lama'],
    'Jakarta Pusat': ['Menteng', 'Tanah Abang', 'Gambir', 'Senen', 'Cempaka Putih'],
    'Jakarta Timur': ['Cakung', 'Jatinegara', 'Duren Sawit', 'Ciracas', 'Kramat Jati'],
    'Jakarta Barat': ['Kembangan', 'Grogol Petamburan', 'Cengkareng', 'Palmerah'],
    'Jakarta Utara': ['Kelapa Gading', 'Penjaringan', 'Tanjung Priok', 'Pademangan'],
    'Tangerang Selatan': ['Bintaro', 'BSD City', 'Serpong', 'Ciputat', 'Pamulang'],
    'Tangerang': ['Cikokol', 'Karawaci', 'Cipondoh', 'Tangerang Kota'],
    'Bekasi': ['Summarecon Bekasi', 'Bekasi Barat', 'Bekasi Timur', 'Jatiasih', 'Pondok Gede'],
    'Depok': ['Margonda', 'Cimanggis', 'Sawangan', 'Beji', 'Pancoran Mas'],
    'Bogor': ['Bogor Kota', 'Sentul City', 'Ciomas', 'Cibinong']
}

# --- Pemuatan Model ---
try:
    model = joblib.load("model/model.joblib")
except FileNotFoundError:
    model = None
    print("Error: File model/model.joblib tidak ditemukan. Pastikan file ada di direktori yang benar.")

EXPECTED_FEATURES = [
    'district', 'city', 'bedrooms', 'bathrooms', 'land_size_m2',
    'building_size_m2', 'carports', 'electricity', 'floors', 'building_age',
    'garages', 'condition'
]

# --- (BARU) Fungsi untuk menganalisis faktor harga ---
def get_price_factors(data):
    """
    Menganalisis input form dan menghasilkan daftar faktor penentu harga.
    Ini adalah simulasi, di dunia nyata bisa menggunakan SHAP atau LIME.
    """
    factors = []
    
    # Faktor 1: Lokasi (District)
    premium_districts = ['Kebayoran Baru', 'Pondok Indah', 'Menteng', 'BSD City', 'Kelapa Gading', 'Summarecon Bekasi', 'Sentul City']
    if data['district'] in premium_districts:
        factors.append({
            "icon": "bi-geo-alt-fill",
            "impact": "positif",
            "text": f"Berada di lokasi premium <strong>{data['district']}</strong> secara signifikan meningkatkan nilai properti."
        })

    # Faktor 2: Luas Tanah
    land_size = float(data['land_size_m2'])
    if land_size > 200:
        factors.append({
            "icon": "bi-aspect-ratio-fill",
            "impact": "positif",
            "text": f"Luas tanah <strong>({int(land_size)} m²)</strong> yang sangat besar memberikan kontribusi positif yang kuat pada harga."
        })
    elif land_size < 70:
        factors.append({
            "icon": "bi-aspect-ratio",
            "impact": "negatif",
            "text": f"Luas tanah <strong>({int(land_size)} m²)</strong> yang relatif kecil menjadi faktor penekan harga."
        })

    # Faktor 3: Usia Bangunan
    age = int(data['building_age'])
    if age > 15:
        factors.append({
            "icon": "bi-calendar-x",
            "impact": "negatif",
            "text": f"Usia bangunan yang lebih dari <strong>{age} tahun</strong> dapat sedikit menurunkan nilai pasar."
        })
    elif age <= 1:
        factors.append({
            "icon": "bi-stars",
            "impact": "positif",
            "text": "Properti ini adalah <strong>bangunan baru</strong>, menjadi daya tarik utama yang meningkatkan harga."
        })
        
    # Faktor 4: Furnishing
    if data['condition'] == 'furnished':
        factors.append({
            "icon": "bi-house-heart-fill",
            "impact": "positif",
            "text": "Kondisi <strong>fully furnished</strong> menambah nilai jual properti Anda."
        })

    # Pastikan selalu ada minimal 2-3 faktor yang ditampilkan
    if len(factors) < 2:
        factors.append({
            "icon": "bi-arrows-fullscreen",
            "impact": "netral",
            "text": f"Luas bangunan <strong>({int(float(data['building_size_m2']))} m²)</strong> menjadi dasar perhitungan utama."
        })
    
    return factors[:3] # Ambil 3 faktor teratas

# --- Context Processor untuk Variabel Global ---
@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

# --- Routes Aplikasi ---
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predictor')
def predictor_page():
    return render_template('predictor.html', cities=KECAMATAN_DATA.keys(), district_data=KECAMATAN_DATA)

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return render_template('predictor.html', prediction_text="Error: Model tidak dapat dimuat.", cities=KECAMATAN_DATA.keys(), district_data=KECAMATAN_DATA)

    form_data = request.form.to_dict()
    try:
        input_df = pd.DataFrame([form_data], columns=EXPECTED_FEATURES)
        
        input_df = input_df.astype({
            'bedrooms': int, 'bathrooms': int, 'land_size_m2': float,
            'building_size_m2': float, 'carports': int, 'electricity': int,
            'floors': int, 'building_age': int, 'garages': int
        })

        prediction = model.predict(input_df)[0]
        predicted_price = f"Rp {prediction * 1_000_000:,.0f}".replace(',', '.')
        
        # (BARU) Panggil fungsi untuk mendapatkan analisis faktor
        price_factors = get_price_factors(form_data)
        
        return render_template('predictor.html', 
                               prediction_text=predicted_price,
                               cities=KECAMATAN_DATA.keys(), 
                               district_data=KECAMATAN_DATA,
                               form_data=form_data,
                               factors=price_factors, # Kirim faktor ke template
                               scroll_to_result=True)

    except Exception as e:
        error_message = f"Terjadi kesalahan: Pastikan semua kolom terisi dengan benar. ({str(e)})"
        return render_template('predictor.html', 
                               prediction_text=error_message,
                               cities=KECAMATAN_DATA.keys(), 
                               district_data=KECAMATAN_DATA,
                               form_data=form_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
