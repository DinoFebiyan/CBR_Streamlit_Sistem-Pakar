import streamlit as st
import math

st.title("Sistem Pakar CBR Jeruk")
st.subheader("Dino Febiyan - 362458302043(3DRPL)")

# Data Gejala
dataGejala = [
    'Adanya bercak kecil jernih pada daun dan helaian daun',
    'Pada daun terdapat semacam gabus berwarna kuning/coklat',
    'Pertumbuhan batang tampak menjadi kerdil',
    'Perubahan bentuk ukuran jeruk (deformasi) pada titik tumbuh',
    'Pada buah jeruk juga terdapat bercak',
    'Buah tampak kering',
    'Mengeluarkan substansi pertahanan berupa kelenjar atau gum',
    'Kulit batang menjadi kering',
    'Kulit tanaman mengelupas',
    'Ranting yang terserang mengeluarkan blendok berwarna kuning keemasan',
    'Celah kulit terlihat adanya masa spora jamur berwarna putih atau hitam',
    'Adanya lapisan tepung putih pada bagian atas daun',
    'Daun mengering akan tetapi tidak gugur',
    'Buah muda yang terserang mudah gugur',
    'Helaian daun menggulung',
    'Terdapat koloni kutu berwarna hitam, coklat atau hijau kekuningan',
    'Terdapat embun madu yang melapisi permukaan daun',
    'Memungkinkan jamur tumbuh (embun jelaga)',
    'Bintik hitam muncul di akar dan daun',
    'Bintik-bintik gelap kecil muncul di daun',
    'Batang muda terdapat bintik kecil',
    'Daun jatuh / rontok',
    'Beberapa buah membusuk'
]

# Data Penyakit
dataPenyakit = [
    'Penyakit Kudis Jeruk atau Kering Kulit',
    'Lumut Batang (Blendok)',
    'Jamur Buah (Embun Tepung)',
    'Kutu Hitam',
    'Jamur Daun'
]

# Basis Kasus
vektorPenyakit = [
    [0.4,0.6,0.3,0.4,0.3,0.5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0.7,0.6,0.5,0.8,0.5,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0.6,0.5,0.5,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.6,0.7,0.8,0.7,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.4,0.5,0.5,0.4,0.3]
]

st.subheader("Pilih Gejala")

kasusBaru = []

for gejala in dataGejala:
    pilih = st.checkbox(gejala)
    kasusBaru.append(1 if pilih else 0)

def hitung_xy(vektor, kasusBaru):
    total = 0
    for i in range(len(kasusBaru)):
        total += vektor[i] * kasusBaru[i]
    return total

def hitung_bawah(data):
    total = 0
    for nilai in data:
        total += nilai * nilai
    hasil = math.sqrt(total)
    return hasil

def hitung_cosine(vektor, kasusBaru):
    xy = hitung_xy(vektor, kasusBaru)
    x = hitung_bawah(vektor)
    y = hitung_bawah(kasusBaru)

    if y == 0:
        return 0

    hasil_cosine = xy / (x * y)
    return hasil_cosine

if st.button("Proses Diagnosa"):

    hasil_akhir = []

    for i in range(len(dataPenyakit)):
        nilai = hitung_cosine(vektorPenyakit[i], kasusBaru)
        hasil_akhir.append(nilai)

    nilaiTerbesar = hasil_akhir[0]
    namaPenyakitTerbesar = dataPenyakit[0]
    for i in range(len(dataPenyakit)):
        if hasil_akhir[i] > nilaiTerbesar:
            nilaiTerbesar = hasil_akhir[i]
            namaPenyakitTerbesar = dataPenyakit[i]

    st.success(f"Penyakit Terdiagnosa : {namaPenyakitTerbesar}")
    st.write(f"Nilai Cosine Similarity : {nilaiTerbesar:.4f}")

    st.subheader("Detail Similarity")
    for i in range(len(dataPenyakit)):
        st.write(f"{dataPenyakit[i]} : {hasil_akhir[i]:.4f}")