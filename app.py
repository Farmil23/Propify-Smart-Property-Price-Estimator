from flask import Flask, render_template, request
import pandas as pd
import joblib
import numpy as np

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
    print("Error: File model.joblib tidak ditemukan.")

EXPECTED_FEATURES = [
    'district', 'city', 'bedrooms', 'bathrooms', 'land_size_m2',
    'building_size_m2', 'carports', 'electricity', 'floors', 'building_age',
    'garages', 'condition'
]

# --- Routes Aplikasi ---
@app.route('/')
def home():
    """Menampilkan halaman utama (hero section dan info)."""
    return render_template('index.html')

@app.route('/predictor')
def predictor_page():
    """Menampilkan halaman form prediktor."""
    return render_template('predictor.html', cities=KECAMATAN_DATA.keys(), district_data=KECAMATAN_DATA)

@app.route('/predict', methods=['POST'])
def predict():
    """Memproses data form dan menampilkan hasil prediksi."""
    if model is None:
        return render_template('predictor.html', prediction_text="Error: Model tidak dapat dimuat.", cities=KECAMATAN_DATA.keys(), district_data=KECAMATAN_DATA)

    try:
        data = request.form.to_dict()
        input_df = pd.DataFrame([data], columns=EXPECTED_FEATURES)
        
        input_df = input_df.astype({
            'bedrooms': int, 'bathrooms': int, 'land_size_m2': float,
            'building_size_m2': float, 'carports': int, 'electricity': int,
            'floors': int, 'building_age': int, 'garages': int
        })

        prediction = model.predict(input_df)[0]
        predicted_price = f"Rp {prediction * 1_000_000:,.0f}"
        
        return render_template('predictor.html', 
                               prediction_text=predicted_price,
                               cities=KECAMATAN_DATA.keys(), 
                               district_data=KECAMATAN_DATA,
                               scroll_to_result=True)

    except Exception as e:
        error_message = f"Terjadi kesalahan: {str(e)}"
        return render_template('predictor.html', 
                               prediction_text=error_message,
                               cities=KECAMATAN_DATA.keys(), 
                               district_data=KECAMATAN_DATA)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)