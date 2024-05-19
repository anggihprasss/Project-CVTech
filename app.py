# Import Module

import numpy as np
import PIL
from PIL import Image, ImageOps
import tensorflow as tf
from tensorflow import keras
import streamlit as st
import cv2
import time
import os
import base64
from base64 import b64encode

# Class names dan explanation
class_names=['Blight', 'Common Rust (Karatan Umum)', 'Gray Leaf Spot (Bercak Daun Abu-abu)', 'Sehat']
class_explanations={
    'Blight': [
        "Blight adalah penyakit yang disebabkan oleh jamur atau bakteri. Penyakit ini biasanya menyebabkan daun-daun tanaman jagung menjadi layu, berubah warna menjadi coklat atau hitam, dan kemudian mati. Blight dapat menyebar dengan cepat, terutama dalam kondisi lembab.",
        "Penanganan atau pengendalian Blight pada tanaman jagung dapat melibatkan beberapa langkah pencegahan dan tindakan pengendalian. Berikut adalah beberapa metode umum yang dapat dilakukan:",
        "1. Rotasi Tanaman: Praktik rotasi tanaman dapat membantu mengurangi risiko infeksi Blight. Dengan merotasi tanaman secara berkala, Anda dapat mengurangi jumlah patogen Blight yang bertahan di tanah.",
        "2. Pemilihan Varietas Tahan Penyakit: Memilih varietas jagung yang tahan terhadap Blight dapat membantu mengurangi risiko infeksi. Konsultasikan dengan penjual benih atau katalog varietas untuk mencari varietas yang memiliki ketahanan terhadap penyakit ini.",
        "3. Pengaturan Jarak Tanam: Menjaga jarak yang cukup antara tanaman jagung dapat membantu meningkatkan sirkulasi udara di antara tanaman, mengurangi kelembaban, dan mengurangi risiko penyebaran Blight.",
        "4. Pengendalian Hama Penghambat: Beberapa hama seperti kutu daun atau ulat daun dapat melemahkan tanaman jagung, membuatnya lebih rentan terhadap infeksi Blight. Pengendalian hama ini dapat membantu menjaga kesehatan tanaman dan mengurangi risiko infeksi tambahan.",
        "5. Penggunaan Fungisida: Penggunaan fungisida dapat menjadi pilihan terakhir jika infeksi Blight sudah parah. Konsultasikan dengan ahli pertanian lokal atau petani lainnya untuk rekomendasi fungisida yang tepat dan cara aplikasinya.",
        "6. Pengelolaan Tanah: Praktik-praktik seperti mengelola drainase tanah dengan baik dan menghindari kelembaban berlebihan di sekitar tanaman juga dapat membantu mengurangi risiko infeksi Blight.",
        "7. Pemantauan dan Tindakan Cepat: Penting untuk memantau tanaman secara teratur untuk deteksi dini gejala Blight. Jika ada tanda-tanda infeksi, tindakan cepat harus diambil untuk membatasi penyebarannya, termasuk pemangkasan daun yang terinfeksi dan pembersihan sisa-sisa tanaman setelah panen.",
        "<a href='https://plantix.net/id/library/plant-diseases/100161/southern-leaf-blight-of-maize/'>Klik untuk informasi selanjutnya..."
    ],
    'Common Rust (Karatan Umum)': [
        "Common Rust (Karatan Umum) adalah penyakit jamur yang biasanya ditemukan pada daun-daun tanaman jagung. Gejalanya termasuk munculnya bercak-bercak berwarna oranye atau coklat pada daun jagung. Penyakit ini dapat menyebabkan penurunan produksi jika tidak diatasi dengan tepat.",
        "Menangani Common Rust (Karatan Umum) pada tanaman jagung dapat dilakukan dengan beberapa langkah pencegahan dan pengendalian. Berikut adalah lima langkah efektif yang dapat diambil:",
        "1. Pilih Varietas Tahan Penyakit: Tanam varietas jagung yang memiliki ketahanan terhadap Common Rust. Banyak benih jagung modern telah dikembangkan untuk memiliki resistensi terhadap berbagai penyakit, termasuk Common Rust.",
        "2. Rotasi Tanaman: Lakukan rotasi tanaman dengan menanam tanaman selain jagung di lahan yang sama setiap tahun. Rotasi tanaman membantu mengurangi populasi patogen di tanah yang bisa menyebabkan infeksi pada musim berikutnya.",
        "3. Pemantauan Rutin: Pantau tanaman jagung secara rutin untuk mendeteksi gejala awal Common Rust. Identifikasi dan tangani infeksi sedini mungkin untuk mencegah penyebaran lebih lanjut.",
        "4. Penggunaan Fungisida: Aplikasikan fungisida yang efektif terhadap Common Rust sesuai dengan petunjuk yang tertera pada label produk. Fungisida dapat membantu mengontrol penyebaran penyakit jika diterapkan pada tahap awal infeksi atau sebagai tindakan pencegahan.",
        "5. Pengelolaan Tanaman dan Lingkungan: Pastikan tanaman mendapatkan nutrisi yang cukup dan air yang memadai, serta pertahankan jarak tanam yang cukup untuk memastikan sirkulasi udara yang baik. Lingkungan yang sehat dan sirkulasi udara yang baik dapat mengurangi kelembaban yang berlebihan dan menghambat perkembangan jamur.",
        "<a href='https://plantix.net/id/library/plant-diseases/100082/common-rust-of-maize/'>Klik untuk informasi selanjutnya..."
    ],
    'Gray Leaf Spot (Bercak Daun Abu-abu)': [
        "Gray Leaf Spot disebabkan oleh jamur yang menginfeksi daun-daun tanaman jagung. Gejalanya berupa bercak-bercak abu-abu atau coklat kecil yang muncul di daun. Jika tidak dikendalikan, penyakit ini dapat menyebabkan penurunan hasil panen yang signifikan.",
        "Mengatasi Gray Leaf Spot (Bercak Daun Abu-abu) pada tanaman jagung melibatkan beberapa langkah pengendalian yang efektif. Berikut adalah lima langkah utama untuk menangani penyakit ini:",
        "1. Rotasi Tanaman: Lakukan rotasi tanaman dengan menanam tanaman selain jagung di lahan yang sama pada musim berikutnya untuk memutus siklus hidup patogen penyebab Gray Leaf Spot dan mengurangi inokulum patogen di tanah.",
        "2. Penggunaan Varietas Tahan Penyakit: Pilih dan tanam varietas jagung yang memiliki resistensi terhadap Gray Leaf Spot, sehingga varietas tahan penyakit memiliki daya tahan lebih baik terhadap infeksi dan mengurangi keparahan penyakit serta kerugian hasil panen.",
        "3. Sanitasi Lahan: Bersihkan sisa-sisa tanaman yang terinfeksi setelah panen dan musnahkan dengan cara dibakar atau dikubur untuk mengurangi sumber inokulum patogen di lapangan dan mengurangi kemungkinan infeksi di musim tanam berikutnya.",
        "4. Pengelolaan Air yang Baik: Pastikan sistem irigasi yang baik dan hindari penyiraman berlebihan yang dapat meningkatkan kelembaban daun, sehingga mengurangi kelembaban yang mendukung perkembangan jamur penyebab Gray Leaf Spot.",
        "5. Aplikasi Fungisida: Gunakan fungisida yang efektif melawan patogen penyebab Gray Leaf Spot sesuai dengan rekomendasi dan petunjuk penggunaan untuk mengendalikan penyebaran infeksi pada tanaman yang sudah terinfeksi dan melindungi tanaman yang sehat.",
        "<a href='https://plantix.net/id/library/plant-diseases/100107/grey-leaf-spot-of-maize/'>Klik untuk informasi selanjutnya..."
    ],
    'Sehat': [
        "Tanaman jagung yang berada dalam kondisi sehat tidak menunjukkan gejala penyakit apapun. Tanaman ini tumbuh dengan baik dan memiliki warna daun yang hijau. Perawatan yang baik, termasuk pemupukan dan pengairan yang tepat, membantu menjaga kesehatan tanaman. Pengamatan teratur dan tindakan pencegahan, seperti rotasi tanaman, pemilihan varietas tahan penyakit, sanitasi lahan, dan pengelolaan air yang baik, adalah kunci untuk menjaga tanaman tetap sehat dan mengurangi risiko infeksi penyakit seperti Gray Leaf Spot."
    ]
}

# Load Model
def load_model():
    custom_objects = {"Adam": tf.keras.optimizers.Adam}
    model = tf.keras.models.load_model('corn_disease_classification.h5', compile=False)
    # Konfigurasi ulang optimizer
    optimizer = tf.keras.optimizers.Adam()
    model.compile(optimizer=optimizer, loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    return model

model = load_model()

# convert image to base64 format
def image_to_base64(image_path):
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    except FileNotFoundError:
        st.error(f"File not found: {image_path}")
        return ""

# Mendapatkan jalur direktori proyek
current_dir = os.path.dirname(os.path.abspath(__file__))
image_dir = os.path.join(current_dir, "images")

# Mendapatkan jalur gambar
logo_left = os.path.join(image_dir, "logo_left.png")
logo_right = os.path.join(image_dir, "logo_right.png")

# Konversi gambar ke base64
logo_left_base64 = image_to_base64(logo_left)
logo_right_base64 = image_to_base64(logo_right)

# Fungsi untuk mengubah gambar ke base64
def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return b64encode(image_file.read()).decode()

# Fungsi untuk menentukan gaya caption berdasarkan tema
def get_caption_style():
    theme = st.get_option("theme.base")
    if theme == "dark":
        return "color: white;"
    if theme == "light":
        return "color: black;"

caption_style = get_caption_style()

# Membuat HTML untuk ditampilkan
html_temp = f"""
    <style>
    .justified {{
        text-align: justify;
    }}
    .center {{
        text-align: center;
    }}
    .caption {{
        color: white; /* Ubah warna teks caption menjadi putih */
        font-size: 24px; /* Ubah ukuran font caption menjadi 20px */
    }}
    .container {{
        display: flex;
        justify-content: space-between; /* Membuat elemen berjajar secara horizontal */
        align-items: center; /* Pusatkan elemen secara vertikal */
        background-color:#228B22;
        padding: 5px;
        border-radius: 30px; /* Membuat sudut background */
    }}
    </style>
    <div class="container">
        <img src="data:image/png;base64,{logo_left_base64}" style="width:100px; height:100px;">
        <h2 style="color:white; font-size:40px;">CVTech</h2>
        <img src="data:image/png;base64,{logo_right_base64}" style="width:100px; height:100px;">
    </div>
"""

# Tampilkan HTML di Streamlit
st.markdown(html_temp, unsafe_allow_html=True)

# Sidebar
st.sidebar.title("CVTech Application")
app_mode = st.sidebar.selectbox("Pilihan", ["Tentang Aplikasi", "Tim Pengembang", "Sistem Prediksi"])

# Tentang Projek
if app_mode == "Tentang Aplikasi":
    st.markdown("""
    <h2 style="text-align: center; font-size: 32px;">Corn Vision Technology: Deteksi Dini, Panen Pasti!</h2>
    <div style="text-align: justify; font-size: 18px;">
    Pertanian merupakan tulang punggung bagi pemenuhan kebutuhan pangan global, namun petani sering kali dihadapkan pada tantangan yang kompleks. Tanaman jagung, salah satu tanaman pangan utama, tidak luput dari berbagai ancaman penyakit dan gangguan yang dapat mengancam hasil panen. Untuk mengatasi masalah ini, CVTech hadir sebagai solusi terdepan dengan menggunakan teknologi terkini dalam bidang Computer Vision.
    </div>
    """, unsafe_allow_html=True)

# Tim Pengembang
elif app_mode == "Tim Pengembang":
    st.markdown("<h1 style='text-align: center;'>Anggota Tim</h1>", unsafe_allow_html=True)
    
    # Fungsi untuk menampilkan profil anggota
    def show_profile(image_path, name, univ, role, github_link, linkedin_link, margin_top='10px'):
        st.markdown(f"""
        <div style="text-align: center; width: 200px; margin: 0 auto;">
            <img src='data:image/png;base64,{image_to_base64(image_path)}' width='128' style='display: block; margin: {margin_top} auto 10px;'>
            <div style='{caption_style}'>{name}</div>
            <div style='margin: 0 auto;'>
                <p style='margin-top: 15px;'><strong></strong> {univ}</p>
                <p><strong></strong> {role}</p>
                <p>
                <a href="{github_link}" target="_blank"><img src="https://upload.wikimedia.org/wikipedia/commons/9/91/Octicons-mark-github.svg" alt="GitHub" width="30" style="margin-right: 10px;"></a> 
                <a href="{linkedin_link}" target="_blank"><img src="https://upload.wikimedia.org/wikipedia/commons/c/ca/LinkedIn_logo_initials.png" alt="LinkedIn" width="30"></a>
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Membuat kolom untuk setiap baris
    col1, col2 = st.columns(2)
    with col1:
        show_profile('images/photo_anggota1.png', 'Anggih Prasetio', 'Universitas Pendidikan Indonesia', 'Data Scientist', 'https://github.com/anggihprasss', 'https://www.linkedin.com/in/anggih-prasetio-a32218223/', margin_top='20px')
    with col2:
        show_profile('images/photo_anggota2.png', 'Asyifa Fauziyah', 'Institut Teknik Garut', 'Data Engineer', 'https://github.com/Asyifauziyah990', 'https://www.linkedin.com/', margin_top='20px')
    
    col3, col4 = st.columns(2)
    with col3:
        show_profile('images/photo_anggota3.png', 'Muhammad Raihan', 'Institut Teknik Garut', 'Full Stack Developer', 'https://github.com/Reyourbae', 'https://www.linkedin.com/', margin_top='40px')
    with col4:
        show_profile('images/photo_anggota4.png', 'Nabila Fitriyani', 'Universitas Mayasari Bakti', 'Project Manager', 'https://github.com/nbilaft', 'https://www.linkedin.com/', margin_top='40px')

# Sistem Deteksi
elif app_mode == "Sistem Prediksi":
    st.markdown("<h1 style='text-align: center;'>Sistem Prediksi Penyakit Jagung</h1>", unsafe_allow_html=True)
    file = st.file_uploader("",type=["jpg", "jpeg", "png"])
    st.set_option('deprecation.showfileUploaderEncoding', False)

    def import_and_predict(image_data, model):
        size = (256, 256)    
        image = ImageOps.fit(image_data, size)
        image = np.asarray(image)
        img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)      
        img_reshape = img[np.newaxis,...]    
        prediction = model.predict(img_reshape)
        return prediction

    if file is None:
        st.text("Silahkan Unggah Gambar")
    else:
        image = Image.open(file)
        st.image(image, width=200)
        if st.button("Prediksi"):
            countdown = 3  # waktu hitung mundur dalam detik
            countdown_placeholder = st.empty()
            for i in range(countdown, 0, -1):
                countdown_placeholder.text(f'Memproses... {i} detik tersisa')
                time.sleep(3)
            countdown_placeholder.empty()
            predictions = import_and_predict(image, model)
            score = np.array(predictions[0])
            predicted_class = class_names[np.argmax(score)]
            confidence = np.max(score)  # Mendapatkan nilai keyakinan tertinggi

            st.title("Sistem memprediksi jagung dalam kondisi {}".format(predicted_class))
            st.write("Penjelasan:")
            explanation_html = "<div class='justified'>"
            for point in class_explanations[predicted_class]:
                explanation_html += "<p>{}</p>".format(point)
            explanation_html += "</div>"
            st.markdown(explanation_html, unsafe_allow_html=True)