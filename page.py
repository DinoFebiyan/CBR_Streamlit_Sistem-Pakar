import streamlit as st
from function import hitung_cosine

KUNCI_PAKAR = "pakar123"

def tambah_gejala_page():
    if "akses_pakar" not in st.session_state:
        st.session_state.akses_pakar = False

    if st.session_state.akses_pakar == False:
        st.title("🔒 Akses Basis Pengetahuan")
        st.info("Fitur ini dikunci khusus untuk pakar agar validitas bobot penilaian penyakit tetap terjaga.")
        
        input_kunci = st.text_input("Masukkan Kunci Pakar", type="password", key="input_kunci_pakar")
        if st.button("Buka Kunci", type="primary", key="btn_buka_kunci"):
            if input_kunci == KUNCI_PAKAR:
                st.session_state.akses_pakar = True
                st.rerun()
            else:
                st.error("Kunci salah!")
        if st.button("Kembali", key="btn_kembali_terkunci"):
            st.session_state.page = "main"
            st.rerun()
        return

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
        
        submitted = st.form_submit_button("Simpan", type="primary")
        if submitted:
            if nama_gejala == "":
                st.error("Nama gejala tidak boleh kosong")
            else:
                gejala_simpan = '"' + nama_gejala + '"' if "," in nama_gejala else nama_gejala
                with open("dataGejala.csv", "a") as csvDataGejala:
                    print(gejala_simpan, file=csvDataGejala)
                
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

    if st.button("Kunci & Kembali", key="btn_kunci_kembali"):
        st.session_state.akses_pakar = False
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

    st.write("Anda pakar yang menemukan gejala baru?")
    if st.button("Tambah Gejala", key="btn_tambah_gejala"):
        st.session_state.page = "tambah_gejala"
        st.rerun()

    if st.button("Proses Diagnosa", type="primary", key="btn_proses_diagnosa"):

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

    st.write("Anda ingin menambahkan penyakit baru?")
    if st.button("Tambah Penyakit Baru", key="btn_tambah_penyakit"):
        st.session_state.page = "tambah_penyakit"
        st.rerun()

    st.divider()
    st.html("""
        <div style="text-align: center; font-size: 0.85rem; padding: 5px 0; color: #4B5563;">
            ©<strong>OrangeChecker</strong> <br> Sistem Pakar Diagnosa Penyakit Tanaman Jeruk<br>
            Dikembangkan oleh: <br> <strong>Dino Febiyan (362458302043)</strong> | 3D-Teknologi Rekayasa Perangkat Lunak | SPK<br>
            <strong><a href="https://ojs.trigunadharma.ac.id/index.php/jsi/article/download/8463/3141" target="_blank" style="color: #FF7A00; text-decoration: none;">Artikel Penelitian</a></strong>
        </div>
    """)

def tambah_penyakit_page():
    if "akses_pakar" not in st.session_state:
        st.session_state.akses_pakar = False

    if st.session_state.akses_pakar == False:
        st.title("🔒 Akses Basis Pengetahuan")
        st.info("Fitur ini dikunci khusus untuk pakar agar validitas bobot penilaian penyakit tetap terjaga.")
        
        input_kunci = st.text_input("Masukkan Kunci Pakar", type="password", key="input_kunci_penyakit")
        if st.button("Buka Kunci", type="primary", key="btn_buka_kunci_penyakit"):
            if input_kunci == KUNCI_PAKAR:
                st.session_state.akses_pakar = True
                st.rerun()
            else:
                st.error("Kunci salah!")
        if st.button("Kembali", key="btn_kembali_terkunci_penyakit"):
            st.session_state.page = "main"
            st.rerun()
        return

    df_gejala = []
    with open("dataGejala.csv", "r") as dataGejala:
        for baris in dataGejala:
            bersih = baris.replace("\n", "").replace('"', '')
            if bersih != "":
                df_gejala = df_gejala + [bersih]

    st.title("Tambah Penyakit Baru")

    with st.form("form_tambah_penyakit"):
        nama_penyakit = st.text_input("Nama Penyakit")
        st.write("Tentukan bobot setiap gejala (biarkan 0 jika gejala tidak terkait):")

        daftar_bobot = []
        for i in range(len(df_gejala)):
            bobot = st.slider(df_gejala[i], 0.0, 1.0, 0.0, 0.01)
            daftar_bobot = daftar_bobot + [bobot]

        submitted = st.form_submit_button("Simpan Penyakit", type="primary")
        if submitted:
            ada_bobot = False
            for i in daftar_bobot:
                if i > 0:
                    ada_bobot = True
            if nama_penyakit == "":
                st.error("Nama penyakit tidak boleh kosong!")
            elif ada_bobot == False:
                st.error("Minimal satu gejala harus memiliki bobot lebih dari 0!")
            else:
                if "," in nama_penyakit:
                    penyakit_simpan = '"' + nama_penyakit + '"'
                else:
                    penyakit_simpan = nama_penyakit

                with open("dataPenyakit.csv", "a") as csvDataPenyakit:
                    print(penyakit_simpan, file=csvDataPenyakit)

                teks_vektor = ""
                for i in range(len(daftar_bobot)):
                    nilai = "0" if daftar_bobot[i] == 0 else str(daftar_bobot[i])
                    teks_vektor += nilai
                    if i < len(daftar_bobot) - 1:
                        teks_vektor += ","

                with open("vektorPenyakit.csv", "a") as csvVektor:
                    print(teks_vektor, file=csvVektor)

                st.success("Penyakit baru berhasil ditambahkan!")

    if st.button("Kunci & Kembali", key="btn_kunci_kembali_penyakit"):
        st.session_state.akses_pakar = False
        st.session_state.page = "main"
        st.rerun()