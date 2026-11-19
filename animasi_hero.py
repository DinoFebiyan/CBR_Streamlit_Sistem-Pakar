import streamlit as st
import streamlit.components.v1 as components
import glob
import base64
import os
import re
import json

def _natural_sort_key(s):
    """Mengurutkan string angka secara alami (misal: frame-1, frame-2, ..., frame-118)."""
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]

@st.cache_data(show_spinner=False)
def load_and_encode_frames(folder_path="frames"):
    """
    Membaca seluruh frame gambar dari folder lokal secara otomatis,
    diurutkan secara teratur (natural sorting), dan di-encode ke Base64 Data URL.
    """
    valid_exts = ("*.jpg", "*.jpeg", "*.webp", "*.png")
    image_paths = []
    
    if os.path.exists(folder_path):
        for ext in valid_exts:
            image_paths.extend(glob.glob(os.path.join(folder_path, ext)))
            image_paths.extend(glob.glob(os.path.join(folder_path, ext.upper())))

    image_paths = sorted(list(set(image_paths)), key=_natural_sort_key)

    encoded_frames = []
    for p in image_paths:
        ext = os.path.splitext(p)[1].lower().replace('.', '')
        mime = "jpeg" if ext in ("jpg", "jpeg") else ext
        try:
            with open(p, "rb") as f:
                b64 = base64.b64encode(f.read()).decode("utf-8")
                encoded_frames.append(f"data:image/{mime};base64,{b64}")
        except Exception as e:
            print(f"Gagal membaca frame {p}: {e}")

    return encoded_frames

def inject_theme_css():
    """
    Menyuntikkan CSS tema modern:
    - Seluruh kartu checkbox interaktif 100% responsif terhadap klik
    - Palet warna Oranye & Putih Bersih yang nyaman di mata
    - Card diagnosa putih bersih berborder oranye segar dengan teks oranye tua pekat
    - Ruang lebar (max-width: 1280px) agar animasi jeruk bebas melebar tanpa terpotong
    """
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Outfit:wght@600;700;800;900&display=swap');

    /* Global Typography & Background */
    html, body, [class*="css"], .stApp {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
        background-color: #FAFAFA !important;
        color: #0F172A !important;
    }

    /* Container Max Width Diperlebar agar Animasi Jeruk Bebas Melebar */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 6rem !important;
        max-width: 1280px !important;
        margin: 0 auto !important;
    }

    /* Headings */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Outfit', 'Plus Jakarta Sans', sans-serif !important;
        letter-spacing: -0.02em !important;
    }

    /* Judul 'Pilih Gejala' & 'Detail Similarity' */
    .stApp h2, .stApp h3, h2#pilih-gejala {
        color: #0F172A !important;
        font-weight: 800 !important;
        font-size: 1.85rem !important;
        margin-top: 36px !important;
        margin-bottom: 18px !important;
        display: flex !important;
        align-items: center !important;
        gap: 12px !important;
        border-left: 5px solid #FF6F00 !important;
        padding-left: 14px !important;
        max-width: 960px !important;
        margin-left: auto !important;
        margin-right: auto !important;
    }

    /* ==============================================================
       KARTU CHECKBOX GEJALA - 100% RESPONSIF & MUDAH DIKLIK
       ============================================================== */
    div[data-testid="stCheckbox"] {
        background-color: #FFFFFF !important;
        border: 1.5px solid #E2E8F0 !important;
        border-radius: 12px !important;
        padding: 14px 20px !important;
        margin-bottom: 10px !important;
        transition: all 0.2s ease-in-out !important;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.03) !important;
        max-width: 960px !important;
        margin-left: auto !important;
        margin-right: auto !important;
        cursor: pointer !important;
        pointer-events: auto !important;
    }

    div[data-testid="stCheckbox"]:hover {
        background-color: #FFF9F2 !important;
        border-color: #FFB74D !important;
        transform: translateX(4px);
        box-shadow: 0 6px 18px rgba(255, 111, 0, 0.1) !important;
    }

    /* Pastikan seluruh area label menangkap klik */
    div[data-testid="stCheckbox"] label {
        cursor: pointer !important;
        width: 100% !important;
        display: flex !important;
        align-items: center !important;
        pointer-events: auto !important;
    }

    /* Teks Checkbox Sangat Jelas (Dark Charcoal #0F172A) */
    div[data-testid="stCheckbox"] label p {
        color: #0F172A !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        line-height: 1.5 !important;
        margin: 0 !important;
        cursor: pointer !important;
    }

    /* Checkbox active state */
    div[data-testid="stCheckbox"] input[type="checkbox"]:checked + div {
        background-color: #FF6F00 !important;
        border-color: #FF6F00 !important;
    }

    /* Tombol "Proses Diagnosa" */
    div.stButton {
        display: flex !important;
        justify-content: center !important;
        max-width: 960px !important;
        margin: 28px auto !important;
    }

    div.stButton > button {
        background: linear-gradient(135deg, #FF6F00 0%, #FF8F00 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 16px 48px !important;
        font-size: 1.15rem !important;
        font-weight: 800 !important;
        letter-spacing: 0.02em !important;
        box-shadow: 0 8px 24px rgba(255, 111, 0, 0.38) !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
        cursor: pointer !important;
        width: 100% !important;
        max-width: 340px !important;
    }

    div.stButton > button:hover {
        background: linear-gradient(135deg, #E65100 0%, #FF6F00 100%) !important;
        box-shadow: 0 12px 30px rgba(255, 111, 0, 0.5) !important;
        transform: translateY(-2px) !important;
        color: #FFFFFF !important;
    }

    div.stButton > button:active {
        transform: translateY(0) !important;
        box-shadow: 0 4px 12px rgba(255, 111, 0, 0.25) !important;
    }

    /* ==============================================================
       BLOK NAMA PENYAKIT (st.success) - GARIS WARNA ORANYE & TEKS BESAR
       Nama penyakit di dalam blok garis warna orange, teks dibuat agak besar
       ============================================================== */
    div[data-testid="stAlert"] {
        background: #FFFFFF !important;
        background-color: #FFFFFF !important;
        border: 2.5px solid #FF6F00 !important;
        border-radius: 16px !important;
        box-shadow: 0 8px 25px rgba(255, 111, 0, 0.12) !important;
        max-width: 960px !important;
        margin: 12px auto 20px auto !important;
        padding: 20px 28px !important;
    }

    /* Bersihkan border, shadow, dan background dari elemen anak di dalam alert */
    div[data-testid="stAlert"] > div,
    div[data-testid="stNotificationContentSuccess"],
    div[data-testid="stAlertContent"],
    .stAlert > div {
        background: transparent !important;
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
        margin: 0 !important;
    }

    /* Ubah Icon Checklist Streamlit Menjadi Oranye Segar */
    div[data-testid="stAlert"] svg {
        fill: #FF6F00 !important;
        color: #FF6F00 !important;
        width: 30px !important;
        height: 30px !important;
    }

    /* Teks Nama Penyakit di Dalam Blok Garis Oranye - Dibuat Agak Besar */
    div[data-testid="stAlert"] p,
    div[data-testid="stAlert"] span,
    div[data-testid="stAlertContent"] p {
        color: #D84315 !important;
        font-family: 'Outfit', 'Plus Jakarta Sans', sans-serif !important;
        font-size: 1.7rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.01em !important;
        line-height: 1.35 !important;
        background: transparent !important;
        text-shadow: none !important;
        margin: 0 !important;
    }

    /* Detail Similarity Text & Nilai Similarity Utama */
    div[data-testid="stMarkdownContainer"] p {
        color: #1E293B !important;
        font-size: 1.05rem !important;
        font-weight: 600 !important;
        line-height: 1.6 !important;
        max-width: 960px !important;
        margin-left: auto !important;
        margin-right: auto !important;
    }
    </style>
    """, unsafe_allow_html=True)

def render_hero_sequence_section(frames_data):
    """
    Merender Hero Section yang bersih:
    - Tanpa badge kondisi buah & tanpa teks instruksi scroll (sesuai instruksi)
    - Scroll-lock murni berbasis event.preventDefault() (tanpa merusak overflow DOM / checkbox)
    - Saat frame habis, langsung scroll ke konten tanpa me-reset ke awal
    - Posisi awal jeruk di pojok bawah layar dan melebar bebas tanpa terpotong
    """
    total_frames = len(frames_data)
    frames_json = json.dumps(frames_data)

    component_html = f"""
    <!DOCTYPE html>
    <html lang="id">
    <head>
      <meta charset="UTF-8">
      <link rel="preconnect" href="https://fonts.googleapis.com">
      <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
      <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@700;800;900&family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap" rel="stylesheet">
      <style>
        * {{
          box-sizing: border-box;
          margin: 0;
          padding: 0;
          user-select: none;
        }}
        body, html {{
          width: 100%;
          height: 100%;
          overflow: hidden;
          background-color: #FAFAFA;
          font-family: 'Plus Jakarta Sans', sans-serif;
        }}
        .hero-container {{
          position: relative;
          width: 100%;
          height: 100%;
          min-height: 650px;
          background: #FAFAFA;
          display: flex;
          flex-direction: column;
          align-items: center;
          overflow: hidden;
        }}
        /* Canvas Penuh Lebar agar Jeruk Bebas Melebar */
        #hero-canvas {{
          position: absolute;
          top: 0;
          left: 0;
          width: 100%;
          height: 100%;
          z-index: 1;
          cursor: ns-resize;
        }}
        /* Tipografi Bagian Atas: HANYA TULISAN BESAR JERUK ANDA? (GAP RAPAT) */
        .top-title-overlay {{
          position: absolute;
          top: 22px;
          left: 0;
          width: 100%;
          text-align: center;
          z-index: 10;
          pointer-events: none;
          padding: 0 20px;
        }}
        .title-first {{
          font-family: 'Outfit', sans-serif;
          font-size: clamp(3rem, 6.5vw, 4.8rem);
          font-weight: 900;
          color: #0F172A;
          line-height: 1.05;
          letter-spacing: -0.03em;
          text-shadow: 0 2px 20px rgba(0, 0, 0, 0.04);
        }}

        /* Tipografi Melayang Tepat Di Atas Frame Jeruk: MEMBUSUK! (DIPERBESAR MAKSIMAL) */
        .floating-rot-wrapper {{
          position: absolute;
          top: 50%;
          left: 50%;
          transform: translate(-50%, -50%);
          z-index: 25;
          pointer-events: none;
          text-align: center;
          width: 100%;
          max-width: 850px;
          padding: 0 16px;
        }}
        .title-second {{
          display: inline-block;
          font-family: 'Outfit', sans-serif;
          font-size: clamp(4.6rem, 11.5vw, 8.5rem);
          font-weight: 900;
          color: #D84315;
          line-height: 0.95;
          letter-spacing: -0.04em;
          opacity: 0;
          transform: translateY(35px) scale(0.85);
          filter: blur(14px);
          transition: opacity 0.35s ease, transform 0.42s cubic-bezier(0.175, 0.885, 0.32, 1.275), filter 0.35s ease;
          text-shadow: 0 14px 44px rgba(216, 67, 21, 0.5), 0 3px 12px rgba(0, 0, 0, 0.12);
        }}
        .title-second.active {{
          opacity: 1;
          transform: translateY(0) scale(1);
          filter: blur(0);
          animation: floatHover 3.2s ease-in-out infinite alternate;
        }}
        @keyframes floatHover {{
          0% {{
            transform: translateY(0px) scale(1);
          }}
          100% {{
            transform: translateY(-14px) scale(1.02);
          }}
        }}
      </style>
    </head>
    <body>
      <div class="hero-container" id="hero-container">
        <canvas id="hero-canvas"></canvas>

        <!-- Bagian Atas: HANYA Teks Besar "Jeruk Anda?" -->
        <div class="top-title-overlay">
          <div class="title-first">Jeruk Anda?</div>
        </div>

        <!-- Melayang Tepat Di Atas Frame Jeruk: "Membusuk!" -->
        <div class="floating-rot-wrapper">
          <div class="title-second" id="text-rot">Membusuk!</div>
        </div>
      </div>

      <script>
        const FRAMES = {frames_json};
        const TOTAL_FRAMES = FRAMES.length;
        const canvas = document.getElementById('hero-canvas');
        const ctx = canvas.getContext('2d');
        const textRot = document.getElementById('text-rot');

        const pDoc = window.parent.document;
        const pWin = window.parent;

        // Preload Frame Images
        let images = [];
        let loadedFrames = 0;

        FRAMES.forEach((src, idx) => {{
          const img = new Image();
          img.src = src;
          img.onload = () => {{
            loadedFrames++;
            if (loadedFrames === 1) {{
              drawFrame(0);
            }}
          }};
          images.push(img);
        }});

        function getBestFrame(idx) {{
          if (images[idx] && images[idx].complete) return images[idx];
          for (let d = 1; d < TOTAL_FRAMES; d++) {{
            if (idx - d >= 0 && images[idx - d] && images[idx - d].complete) return images[idx - d];
            if (idx + d < TOTAL_FRAMES && images[idx + d] && images[idx + d].complete) return images[idx + d];
          }}
          return images[0];
        }}

        function drawFrame(index) {{
          const img = getBestFrame(index);
          if (!img) return;

          const dpr = window.devicePixelRatio || 1;
          const rect = canvas.getBoundingClientRect();

          if (canvas.width !== Math.round(rect.width * dpr) || canvas.height !== Math.round(rect.height * dpr)) {{
            canvas.width = Math.round(rect.width * dpr);
            canvas.height = Math.round(rect.height * dpr);
          }}

          ctx.save();
          ctx.scale(dpr, dpr);
          ctx.imageSmoothingEnabled = true;
          ctx.imageSmoothingQuality = 'high';

          // Clear dengan latar bersih
          ctx.fillStyle = '#FAFAFA';
          ctx.fillRect(0, 0, rect.width, rect.height);

          // Penskalaan Proporsional agar lebar tidak terpotong saat membelah
          const preferredHeight = Math.min(rect.height * 0.62, 410);
          const scaleByHeight = preferredHeight / 693;
          const maxAllowedWidth = rect.width * 0.95;
          const scaleByWidth = maxAllowedWidth / img.width;
          const scale = Math.min(scaleByHeight, scaleByWidth);

          const drawW = img.width * scale;
          const drawH = img.height * scale;
          
          // Posisi X di tengah persis
          const drawX = (rect.width - drawW) / 2;
          
          // Posisi Y: Rapat dan dekat di bawah tulisan "Jeruk Anda?" (tanpa gap kosong yang jauh)
          const drawY = 118;

          ctx.drawImage(img, drawX, drawY, drawW, drawH);
          ctx.restore();
        }}

        // Deteksi Posisi Scroll Streamlit
        function getScrollPosition() {{
          let top = 0;
          const candidates = [
            pDoc.querySelector('[data-testid="stAppViewContainer"]'),
            pDoc.querySelector('section.main'),
            pDoc.querySelector('[data-testid="stMain"]'),
            pDoc.documentElement,
            pDoc.body
          ];
          for (let el of candidates) {{
            if (el && el.scrollTop > top) {{
              top = el.scrollTop;
            }}
          }}
          if (pWin.scrollY > top) top = pWin.scrollY;
          if (pWin.pageYOffset > top) top = pWin.pageYOffset;
          return top;
        }}

        // Inisialisasi:
        // Jika user berada di bawah (sedang memilih gejala / diagnosa), frame tetap di posisi 1.0 (habis)
        const initialTop = getScrollPosition();
        let targetProgress = initialTop > 80 ? 1.0 : 0.0;
        let currentProgress = targetProgress;

        function updateUI(progress) {{
          if (progress >= 0.42) {{
            textRot.classList.add('active');
          }} else {{
            textRot.classList.remove('active');
          }}
        }}

        // Render Loop 60 FPS
        function renderLoop() {{
          currentProgress += (targetProgress - currentProgress) * 0.22;

          // Clamp frameIdx agar ketika habis tetap berada di frame terakhir (TIDAK KEMBALI KE AWAL)
          const frameIdx = Math.min(TOTAL_FRAMES - 1, Math.max(0, Math.round(currentProgress * (TOTAL_FRAMES - 1))));
          drawFrame(frameIdx);
          updateUI(currentProgress);

          requestAnimationFrame(renderLoop);
        }}
        requestAnimationFrame(renderLoop);

        // ==============================================================
        // LOGIKA SCROLL MURNI BEBAS-GLITCH (TIDAK MERUSAK CHECKBOX / OVERFLOW)
        // 1. Saat frame masih berjalan (targetProgress < 1.0): tahan scroll layar dengan e.preventDefault()
        // 2. Saat frame sudah habis (targetProgress = 1.0): lepaskan e.preventDefault(), halaman langsung scroll ke bawah
        // 3. Frame TIDAK KEMBALI KE AWAL saat habis
        // ==============================================================
        function handleWheelScroll(e) {{
          const currentTop = getScrollPosition();
          const rect = canvas.getBoundingClientRect();
          const isHeroInView = rect.top <= 40 && rect.bottom >= 120;

          // KONDISI 1: User di atas hero dan frame belum habis
          if (isHeroInView && currentTop <= 20 && targetProgress < 1.0) {{
            if (e.deltaY > 0) {{
              // Scroll ke bawah: putar frame maju
              e.preventDefault();
              targetProgress = Math.min(1.0, targetProgress + e.deltaY * 0.0018);
            }} else if (e.deltaY < 0 && targetProgress > 0.0) {{
              // Scroll ke atas: putar frame mundur
              e.preventDefault();
              targetProgress = Math.max(0.0, targetProgress + e.deltaY * 0.0018);
            }}
          }}
          // KONDISI 2: Frame SUDAH HABIS (targetProgress >= 1.0)
          else if (targetProgress >= 1.0) {{
            // Jika user scroll ke atas sampai mentok ke puncak halaman (top <= 5), barulah frame bisa diputar mundur
            if (currentTop <= 5 && e.deltaY < 0) {{
              e.preventDefault();
              targetProgress = Math.max(0.0, targetProgress + e.deltaY * 0.0018);
            }}
            // Jika scroll ke bawah, BIARKAN HALAMAN BERGULIR BEBAS KE CHECKBOX & FORM DIAGNOSA
          }}
        }}

        // Touch handling untuk layar sentuh
        let touchStartY = 0;
        function handleTouchStart(e) {{
          if (e.touches && e.touches.length > 0) {{
            touchStartY = e.touches[0].clientY;
          }}
        }}

        function handleTouchMove(e) {{
          if (!e.touches || e.touches.length === 0) return;
          const currentY = e.touches[0].clientY;
          const deltaY = touchStartY - currentY;
          touchStartY = currentY;

          const currentTop = getScrollPosition();
          const rect = canvas.getBoundingClientRect();
          const isHeroInView = rect.top <= 40 && rect.bottom >= 120;

          if (isHeroInView && currentTop <= 20 && targetProgress < 1.0) {{
            if (deltaY > 0) {{
              e.preventDefault();
              targetProgress = Math.min(1.0, targetProgress + deltaY * 0.0035);
            }} else if (deltaY < 0 && targetProgress > 0.0) {{
              e.preventDefault();
              targetProgress = Math.max(0.0, targetProgress + deltaY * 0.0035);
            }}
          }} else if (targetProgress >= 1.0) {{
            if (currentTop <= 5 && deltaY < 0) {{
              e.preventDefault();
              targetProgress = Math.max(0.0, targetProgress + deltaY * 0.0035);
            }}
          }}
        }}

        // Pasang event listeners pada komponen hero dan window
        const heroEl = document.getElementById('hero-container');
        heroEl.addEventListener('wheel', handleWheelScroll, {{ passive: false }});
        pWin.addEventListener('wheel', handleWheelScroll, {{ passive: false }});
        pDoc.addEventListener('wheel', handleWheelScroll, {{ passive: false }});

        heroEl.addEventListener('touchstart', handleTouchStart, {{ passive: true }});
        pWin.addEventListener('touchstart', handleTouchStart, {{ passive: true }});
        pDoc.addEventListener('touchstart', handleTouchStart, {{ passive: true }});

        heroEl.addEventListener('touchmove', handleTouchMove, {{ passive: false }});
        pWin.addEventListener('touchmove', handleTouchMove, {{ passive: false }});
        pDoc.addEventListener('touchmove', handleTouchMove, {{ passive: false }});

        window.addEventListener('resize', () => {{
          const frameIdx = Math.min(TOTAL_FRAMES - 1, Math.max(0, Math.round(currentProgress * (TOTAL_FRAMES - 1))));
          drawFrame(frameIdx);
        }});
      </script>
    </body>
    </html>
    """
    components.html(component_html, height=650, scrolling=False)

def render_big_orange_callout_section():
    """
    Merender Section Teks Besar dengan Background Oranye Hangat (Bergaya Apple):
    - Background oranye segar yang memukau
    - Judul besar 'Cek penyakit jeruk Anda sebelum telat!' berwarna putih murni tebal
    - Jarak atas lega (margin-top: 80px) agar memberi ruang saat jeruk terbelah
    """
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #FF6F00 0%, #E65100 100%);
        border-radius: 28px;
        padding: 58px 44px;
        margin: 80px auto 44px auto;
        max-width: 960px;
        text-align: center;
        box-shadow: 0 20px 50px rgba(255, 111, 0, 0.28);
        color: #FFFFFF;
    ">
        <div style="
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(8px);
            border: 1px solid rgba(255, 255, 255, 0.35);
            padding: 7px 22px;
            border-radius: 40px;
            color: #FFFFFF;
            font-size: 0.95rem;
            font-weight: 800;
            letter-spacing: 0.14em;
            text-transform: uppercase;
            margin-bottom: 16px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
        ">
            🍊 ORANGECHECKER
        </div>
        <h1 style="
            margin: 0 0 16px 0;
            color: #FFFFFF !important;
            font-family: 'Outfit', sans-serif;
            font-size: clamp(2.3rem, 4.6vw, 3.6rem);
            font-weight: 900;
            line-height: 1.15;
            letter-spacing: -0.02em;
            text-shadow: 0 4px 18px rgba(0, 0, 0, 0.15);
        ">
            Cek penyakit jeruk Anda<br>sebelum telat!
        </h1>
        <p style="
            margin: 0 auto;
            max-width: 760px;
            color: #FFF8E1;
            font-size: 1.12rem;
            line-height: 1.7;
            font-weight: 500;
        ">
            Jangan biarkan infeksi patogen merusak seluruh kebun Anda. 
            Sistem <b>Case-Based Reasoning (Cosine Similarity)</b> siap mencocokkan gejala klinis tanaman jeruk secara cepat, akurat, dan terpercaya.
        </p>
    </div>
    """, unsafe_allow_html=True)

def tampilkan_footer():
    """
    Merender footer elegan di bagian paling bawah halaman:
    Identitas Sistem Pakar CBR Tanaman Jeruk & Mahasiswa (Dino Febiyan).
    """
    st.markdown("""
    <div style="
        margin-top: 80px;
        padding: 40px 20px 30px 20px;
        text-align: center;
        border-top: 1.5px solid #F1F5F9;
        background: #FAFAFA;
        color: #64748B;
        font-family: 'Plus Jakarta Sans', sans-serif;
    ">
        <div style="
            display: inline-flex;
            align-items: center;
            gap: 10px;
            background: #FFFFFF;
            border: 1.5px solid #FFE0B2;
            padding: 10px 24px;
            border-radius: 50px;
            box-shadow: 0 4px 16px rgba(255, 111, 0, 0.08);
            margin-bottom: 14px;
        ">
            <span style="font-size: 1.25rem;">🍊</span>
            <span style="font-weight: 800; color: #E65100; font-size: 1rem; letter-spacing: -0.01em;">OrangeChecker</span>
            <span style="color: #CBD5E1;">•</span>
            <span style="font-weight: 600; color: #334155; font-size: 0.95rem;">Sistem Pakar CBR Tanaman Jeruk</span>
        </div>
        <p style="
            margin: 6px 0 0 0;
            font-size: 0.88rem;
            color: #64748B;
            font-weight: 600;
        ">
<div style="
    background-color: #FFFFFF;
    border: 2px solid #FF9800;
    border-radius: 16px;
    padding: 18px 24px;
    margin: 32px auto 12px auto;
    max-width: 960px;
    box-shadow: 0 8px 24px rgba(255, 111, 0, 0.1);
    text-align: center;
    font-family: sans-serif;
">
    <p style="margin: 0 0 6px 0; color: #D84315; font-size: 1.05rem;">
        Dikembangkan oleh: <b>Dino Febiyan</b> &mdash; NIM <b>362458302043</b>
    </p>
    <p style="margin: 0 0 12px 0; color: #5D4037; font-size: 0.95rem;">
        Kelas <b>3D</b> &bull; Prodi <b>Teknologi Rekayasa Perangkat Lunak (TRPL)</b> &bull; Mata Kuliah <b>Sistem Pendukung Keputusan</b>
    </p>
    <div style="border-top: 1px dashed #FFCC80; padding-top: 10px; font-size: 0.88rem; color: #6D4C41;">
        Referensi Artikel: 
        <a href="https://ojs.trigunadharma.ac.id/index.php/jsi/article/download/8463/3141" 
           target="_blank" 
           style="color: #EF6C00; font-weight: 700; text-decoration: none;">
           Sistem Pakar Mendiagnosa Penyakit Pada Tanaman Jeruk Sunkist Dengan Metode Case Based Reasoning (CBR) &#8599;
        </a>
    </div>
        </p>
    </div>
    """, unsafe_allow_html=True)

def tampilkan_hero_animasi():
    """
    Fungsi utama yang dipanggil pada app.py.
    Menjalankan styling tema, memuat Hero Section sequence tajam bergaya Apple,
    dan menampilkan Section Teks Besar dengan Background Oranye.
    """
    try:
        st.set_page_config(
            page_title="OrangeChecker",
            page_icon="🍊",
            layout="wide",
            initial_sidebar_state="collapsed"
        )
    except Exception:
        pass

    # 1. Suntikkan styling tema dengan kontras warna tinggi & checkbox responsif
    inject_theme_css()

    # 2. Muat frame gambar dan render Hero Section Tajam di Pojok Bawah Layar Saat Dibuka
    frames = load_and_encode_frames("frames")
    if frames:
        render_hero_sequence_section(frames)
    else:
        st.warning("Folder 'frames' tidak ditemukan atau tidak berisi gambar")

    # 3. Tampilkan Section Teks Besar dengan Background Warna Oranye
    render_big_orange_callout_section()
