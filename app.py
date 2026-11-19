import streamlit as st
import math
import pandas as pd
from animasi_hero import tampilkan_hero_animasi

# Panggil fungsi antarmuka animasi Hero & Tema Oranye-Putih di bagian paling atas
tampilkan_hero_animasi()

df_gejala = pd.read_csv('dataGejala.csv', header=None)[0].tolist()
df_penyakit = pd.read_csv('dataPenyakit.csv', header=None)[0].tolist()
df_vektor = pd.read_csv('vektorPenyakit.csv', header=None).astype(float).values.tolist()

st.subheader("Pilih Gejala")

kasusBaru = []

for gejala in df_gejala:
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

    for i in range(len(df_penyakit)):
        nilai = hitung_cosine(df_vektor[i], kasusBaru)
        hasil_akhir.append(nilai)

    nilaiTerbesar = hasil_akhir[0]
    namaPenyakitTerbesar = df_penyakit[0]
    for i in range(len(df_penyakit)):
        if hasil_akhir[i] > nilaiTerbesar:
            nilaiTerbesar = hasil_akhir[i]
            namaPenyakitTerbesar = df_penyakit[i]

    st.success(f"Penyakit Terdiagnosa : {namaPenyakitTerbesar}")
    st.write(f"Nilai Cosine Similarity : {nilaiTerbesar:.4f}")

    st.subheader("Detail Similarity")
    for i in range(len(df_penyakit)):
        st.write(f"{df_penyakit[i]} : {hasil_akhir[i]:.4f}")
