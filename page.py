import streamlit as st
from function import hitung_cosine

def tambah_gejala_page():

    df_penyakit = []
    with open("dataPenyakit.csv", "r") as dataPenyakit:
        for baris in dataPenyakit:
            bersih = baris.replace("\n", "")
            if bersih != "":
                df_penyakit = df_penyakit + [bersih]
    st.title("Tambah Gejala Baru")
    
    with st.form("form_tambah_gejala"):
        nama_gejala = st.text_input("Nama Gejala")
        penyakit_terkait = st.selectbox("Pilih Penyakit Terkait", df_penyakit)
        bobot = st.slider("Bobot", 0.1, 1.0, 0.5, 0.01)
        
        submitted = st.form_submit_button("Simpan")
        if submitted:
            if nama_gejala == "":
                st.error("Nama gejala tidak boleh kosong")
            else:
                with open("dataGejala.csv", "a") as csvDataGejala:
                    print(nama_gejala, file=csvDataGejala)
                
                vektor_matrix = []
                with open("vektorPenyakit.csv", "r") as csvVektor:
                    for baris in csvVektor:
                        if "," in baris:
                            vektor_matrix = vektor_matrix + [baris.replace("\n", "").split(',')]
                
                for i in range(len(df_penyakit)):
                    dataBaru = str(bobot) if df_penyakit[i] == penyakit_terkait else "0"
                    vektor_matrix[i] = vektor_matrix[i] + [dataBaru]
                
                with open("vektorPenyakit.csv", "w") as csvVektor:
                    for baris in vektor_matrix:
                            teks = ""
                            for i in range(len(baris)):
                                teks += str(baris[i])
                                if i < len(baris) - 1:
                                    teks += ","
                            print(teks, file=csvVektor)            
                st.success("Gejala berhasil ditambahkan!")

    if st.button("Kembali"):
        st.session_state.page = "main"
        st.rerun()

def main_page():
    df_gejala = []
    with open("dataGejala.csv", "r") as f:
        for baris in f:
            bersih = baris.replace("\n", "").replace('"', '')
            if bersih != "":
                df_gejala = df_gejala + [bersih]

    df_penyakit = []
    with open("dataPenyakit.csv", "r") as f:
        for baris in f:
            bersih = baris.replace("\n", "")
            if bersih != "":
                df_penyakit = df_penyakit + [bersih]

    df_vektor = []
    with open("vektorPenyakit.csv", "r") as f:
        for baris in f:
            if "," in baris:
                angka = [float(x) for x in baris.replace("\n", "").split(",")]
                df_vektor = df_vektor + [angka]
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
        st.image("jeruk.png")

    st.divider()
    st.markdown("#### Pilih Gejala")
    kasusBaru = []

    for gejala in df_gejala:
        pilih = st.checkbox(gejala)
        kasusBaru = kasusBaru + [1] if pilih else kasusBaru + [0]

    if st.button("Proses Diagnosa", type="primary"):

        hasil_akhir = []

        for i in range(len(df_penyakit)):
            nilai = hitung_cosine(df_vektor[i], kasusBaru)
            hasil_akhir = hasil_akhir + [nilai]

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

    st.write("Tidak menemukan gejala yang anda alami?")
    if st.button("Tambah Gejala Baru"):
        st.session_state.page = "tambah_gejala"
        st.rerun()

    st.divider()
    st.html("""
        <div style="text-align: center; font-size: 0.85rem; padding: 5px 0; color: #4B5563;">
            ©<strong>OrangeChecker</strong> <br> Sistem Pakar Diagnosa Penyakit Tanaman Jeruk<br>
            Dikembangkan oleh: <br> <strong>Dino Febiyan (362458302043)</strong> | 3D-Teknologi Rekayasa Perangkat Lunak | SPK<br>
            <strong><a href="https://ojs.trigunadharma.ac.id/index.php/jsi/article/download/8463/3141" target="_blank" style="color: #FF7A00; text-decoration: none;">Artikel Penelitian</a></strong>
        </div>
    """)