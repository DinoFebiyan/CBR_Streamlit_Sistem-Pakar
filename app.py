import streamlit as st
import pandas as pd
from function import hitung_cosine

st.set_page_config(
    page_title="Orange Checker",
    page_icon="🍊",
    layout="centered"
)

st.markdown("""
    <style>
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

df_gejala = pd.read_csv('dataGejala.csv', header=None)[0].tolist()
df_penyakit = pd.read_csv('dataPenyakit.csv', header=None)[0].tolist()
df_vektor = pd.read_csv('vektorPenyakit.csv', header=None).astype(float).values.tolist()

st.html("""
    <h1 style="text-align: center; color: #FF7A00; margin-bottom: 0.5rem;">
        🍊 Orange Checker
    </h1>
""")

col_kiri, col_kanan = st.columns([1.7, 1])

with col_kiri:
    st.subheader("Sistem Pakar Diagnosa Penyakit Tanaman Jeruk")
    st.write(
        "Pilih gejala yang anda lihat pada tanaman jeruk anda, kemudian klik tombol "
        "'Proses Diagnosa' untuk mendapatkan hasil diagnosa penyakit yang mungkin terjadi."
    )

with col_kanan:
    st.image("jeruk.png", use_container_width=True)

st.divider()
st.markdown("#### Pilih Gejala")
kasusBaru = []

for gejala in df_gejala:
    pilih = st.checkbox(gejala)
    kasusBaru.append(1 if pilih else 0)

if st.button("Proses Diagnosa", type="primary"):

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

    st.markdown("#### Hasil Diagnosa")
    if nilaiTerbesar == 0:
        st.warning("Tidak ada penyakit yang terdiagnosa. Silakan pilih gejala!")
    else:
        st.success(namaPenyakitTerbesar)
        st.write(f"Nilai Kemiripan : {nilaiTerbesar:.4f}")
        st.markdown("#### Kecenderungan Kemiripan Penyakit Lainnya")
        for i in range(len(df_penyakit)):
            if hasil_akhir[i] > 0:
                st.write(f"{df_penyakit[i]} : {hasil_akhir[i]:.4f}")

st.divider()
st.html("""
    <div style="text-align: center; font-size: 0.85rem; padding: 5px 0; color: #4B5563;">
        ©<strong>OrangeChecker</strong> <br> Sistem Pakar Diagnosa Penyakit Tanaman Jeruk<br>
        Dikembangkan oleh: <br> <strong>Dino Febiyan (362458302043)</strong> | 3D-Teknologi Rekayasa Perangkat Lunak | SPK<br>
        <strong><a href="https://ojs.trigunadharma.ac.id/index.php/jsi/article/download/8463/3141" target="_blank" style="color: #FF7A00; text-decoration: none;">Artikel Penelitian</a></strong>
    </div>
""")