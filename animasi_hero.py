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

    /* Kartu Checkbox Gejala Putih Bersih dengan Teks Gelap Kontras */
    div[data-testid="stCheckbox"] {
        background-color: #FFFFFF !important;
        border: 1.5px solid #E2E8F0 !important;
        border-radius: 12px !important;
        padding: 12px 18px !important;
        margin-bottom: 10px !important;
        transition: all 0.22s ease-in-out !important;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.03) !important;
        max-width: 960px !important;
        margin-left: auto !important;
        margin-right: auto !important;
    }

    div[data-testid="stCheckbox"]:hover {
        background-color: #FFF9F2 !important;
        border-color: #FFB74D !important;
        transform: translateX(5px) !important;
        box-shadow: 0 6px 18px rgba(255, 111, 0, 0.1) !important;
    }

    /* Teks Checkbox Sangat Jelas (Dark Charcoal #0F172A) */
    div[data-testid="stCheckbox"] label p {
        color: #0F172A !important;
        font-size: 0.98rem !important;
        font-weight: 600 !important;
        line-height: 1.5 !important;
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
       KOTAK HASIL DIAGNOSA (st.success) - TEMA ORANYE PUTIH BERSIH
       Memperbaiki warna gelap / hijau yang membuat sakit mata
       ============================================================== */
    div[data-testid="stAlert"],
    div[data-testid="stAlert"] > div,
    div[data-testid="stNotificationContentSuccess"],
    div[data-testid="stAlertContent"],
    .stAlert,
    .stAlert > div {
        background: #FFFFFF !important;
        background-color: #FFFFFF !important;
        border: 2.5px solid #FF9800 !important;
        border-radius: 18px !important;
        box-shadow: 0 10px 30px rgba(255, 111, 0, 0.12) !important;
        max-width: 960px !important;
        margin: 24px auto !important;
        padding: 18px 24px !important;
    }

    /* Ubah Icon Checklist Streamlit Menjadi Oranye Segar */
    div[data-testid="stAlert"] svg {
        fill: #FF6F00 !important;
        color: #FF6F00 !important;
    }

    /* Teks Hasil Diagnosa - Oranye Tua Pekat & Sangat Jelas di Atas Latar Putih */
    div[data-testid="stAlert"] p,
    div[data-testid="stAlert"] span,
    div[data-testid="stAlertContent"] p {
        color: #D84315 !important;
        font-size: 1.3rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.01em !important;
        line-height: 1.5 !important;
        background: transparent !important;
        text-shadow: none !important;
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
    Merender Hero Section dengan fitur Scroll-Lock cerdas (Apple Style):
    - Saat frame sedang berjalan (masih di tengah): scroll layar MATI agar frame berputar penuh di tempat
    - Saat frame sudah habis (jeruk terbelah sempurna): scroll layar NYALA dan TIDAK kembali ke awal lagi
    - Jeruk diposisikan di pojok bawah layar saat awal dibuka dan melebar bebas tanpa terpotong
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
          min-height: 860px;
          background: #FAFAFA;
          display: flex;
          flex-direction: column;
          justify-content: space-between;
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
        /* Tipografi Mengambang di Bagian Atas Layar */
        .typography-overlay {{
          position: relative;
          z-index: 10;
          padding: 32px 24px 0 24px;
          text-align: center;
          pointer-events: none;
          max-width: 780px;
        }}
        .badge-pill {{
          display: inline-flex;
          align-items: center;
          gap: 8px;
          background: #FFF3E0;
          border: 1px solid #FFE0B2;
          color: #E65100;
          font-size: 0.82rem;
          font-weight: 700;
          padding: 6px 16px;
          border-radius: 30px;
          margin-bottom: 12px;
          letter-spacing: 0.03em;
          box-shadow: 0 2px 8px rgba(230, 81, 0, 0.08);
        }}
        .title-first {{
          font-family: 'Outfit', sans-serif;
          font-size: clamp(2.8rem, 5.5vw, 4.4rem);
          font-weight: 900;
          color: #0F172A;
          line-height: 1.05;
          letter-spacing: -0.03em;
        }}
        .title-second {{
          font-family: 'Outfit', sans-serif;
          font-size: clamp(3rem, 6vw, 4.8rem);
          font-weight: 900;
          color: #D84315;
          line-height: 1.05;
          letter-spacing: -0.03em;
          margin-top: 2px;
          margin-bottom: 12px;
          opacity: 0;
          transform: translateY(20px) scale(0.96);
          filter: blur(8px);
          transition: opacity 0.32s ease, transform 0.35s cubic-bezier(0.175, 0.885, 0.32, 1.275), filter 0.32s ease;
          text-shadow: 0 4px 20px rgba(216, 67, 21, 0.28);
        }}
        .title-second.active {{
          opacity: 1;
          transform: translateY(0) scale(1);
          filter: blur(0);
        }}
        .fruit-status {{
          display: inline-flex;
          align-items: center;
          gap: 8px;
          padding: 7px 16px;
          background: rgba(255, 255, 255, 0.95);
          backdrop-filter: blur(10px);
          border-radius: 12px;
          border: 1px solid #E2E8F0;
          font-size: 0.86rem;
          font-weight: 700;
          color: #334155;
          box-shadow: 0 4px 14px rgba(0,0,0,0.05);
          transition: all 0.3s ease;
        }}
        .status-dot {{
          width: 9px;
          height: 9px;
          border-radius: 50%;
          background-color: #10B981;
          transition: background-color 0.3s ease;
        }}
        /* Petunjuk Scroll Minimalis */
        .scroll-cue {{
          position: relative;
          z-index: 10;
          display: flex;
          flex-direction: column;
          align-items: center;
          gap: 6px;
          color: #64748B;
          font-size: 0.78rem;
          font-weight: 700;
          letter-spacing: 0.05em;
          text-transform: uppercase;
          pointer-events: none;
          opacity: 1;
          transition: opacity 0.35s ease;
          margin-bottom: 24px;
        }}
        .mouse-icon {{
          width: 22px;
          height: 34px;
          border: 2px solid #CBD5E1;
          border-radius: 12px;
          position: relative;
          display: flex;
          justify-content: center;
        }}
        .wheel-dot {{
          width: 4px;
          height: 8px;
          background-color: #FF6F00;
          border-radius: 2px;
          position: absolute;
          top: 6px;
          animation: wheelScroll 1.6s infinite ease-in-out;
        }}
        @keyframes wheelScroll {{
          0% {{ transform: translateY(0); opacity: 1; }}
          100% {{ transform: translateY(14px); opacity: 0; }}
        }}
      </style>
    </head>
    <body>
      <div class="hero-container" id="hero-container">
        <!-- Canvas Gambar Jeruk Penuh Lebar -->
        <canvas id="hero-canvas"></canvas>

        <div class="typography-overlay">
          <div class="badge-pill">🍊 Sistem Pakar CBR Tanaman Jeruk • Dino Febiyan (3DRPL)</div>
          <div class="title-first">Jeruk Anda?</div>
          <div class="title-second" id="text-rot">Membusuk!</div>
          <div class="fruit-status" id="fruit-status">
            <span class="status-dot" id="status-dot"></span>
            <span id="status-text">Kondisi Buah: Segar & Sehat (100%)</span>
          </div>
        </div>

        <div class="scroll-cue" id="scroll-cue">
          <div class="mouse-icon">
            <div class="wheel-dot"></div>
          </div>
          <span>Scroll untuk memutar frame</span>
        </div>
      </div>

      <script>
        const FRAMES = {frames_json};
        const TOTAL_FRAMES = FRAMES.length;
        const canvas = document.getElementById('hero-canvas');
        const ctx = canvas.getContext('2d');
        const textRot = document.getElementById('text-rot');
        const statusDot = document.getElementById('status-dot');
        const statusText = document.getElementById('status-text');
        const scrollCue = document.getElementById('scroll-cue');

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

          // Penskalaan Proporsional agar lebar tidak terpotong
          const preferredHeight = Math.min(rect.height * 0.58, 410);
          const scaleByHeight = preferredHeight / 693;
          const maxAllowedWidth = rect.width * 0.95;
          const scaleByWidth = maxAllowedWidth / img.width;
          const scale = Math.min(scaleByHeight, scaleByWidth);

          const drawW = img.width * scale;
          const drawH = img.height * scale;
          
          // Posisi X di tengah persis
          const drawX = (rect.width - drawW) / 2;
          
          // Posisi Y di pojok bawah layar saat awal dibuka (scroll = 0)
          const drawY = rect.height - drawH - 30;

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

        // Fungsi Kunci & Buka Scroll Layar Utama Streamlit
        function lockPageScroll() {{
          const containers = [
            pDoc.querySelector('[data-testid="stAppViewContainer"]'),
            pDoc.querySelector('section.main'),
            pDoc.body,
            pDoc.documentElement
          ];
          containers.forEach(el => {{
            if (el) el.style.overflow = 'hidden';
          }});
        }}

        function unlockPageScroll() {{
          const containers = [
            pDoc.querySelector('[data-testid="stAppViewContainer"]'),
            pDoc.querySelector('section.main'),
            pDoc.body,
            pDoc.documentElement
          ];
          containers.forEach(el => {{
            if (el) el.style.overflow = '';
          }});
        }}

        // Inisialisasi State:
        // Jika user sedang berada di bawah (misal saat centang checkbox / diagnosa), jangan kunci scroll
        const initialTop = getScrollPosition();
        let targetProgress = initialTop > 60 ? 1.0 : 0.0;
        let currentProgress = targetProgress;

        if (initialTop <= 60) {{
          lockPageScroll(); // Matikan scroll layar awal saat frame masih di hero
        }} else {{
          unlockPageScroll();
        }}

        function updateUI(progress) {{
          if (progress > 0.04) {{
            scrollCue.style.opacity = '0';
          }} else {{
            scrollCue.style.opacity = '1';
          }}

          // Teks 'Membusuk!' aktif saat mencapai fase pembusukan
          if (progress >= 0.42) {{
            textRot.classList.add('active');
            statusDot.style.backgroundColor = '#D84315';
            statusText.innerText = 'Kondisi Buah: Infeksi Akut & Membusuk';
            statusDot.parentElement.style.borderColor = '#FFAB91';
          }} else if (progress >= 0.20) {{
            textRot.classList.remove('active');
            statusDot.style.backgroundColor = '#F59E0B';
            statusText.innerText = 'Kondisi Buah: Terindikasi Gejala Penyakit';
            statusDot.parentElement.style.borderColor = '#FFE082';
          }} else {{
            textRot.classList.remove('active');
            statusDot.style.backgroundColor = '#10B981';
            statusText.innerText = 'Kondisi Buah: Segar & Sehat (100%)';
            statusDot.parentElement.style.borderColor = '#E2E8F0';
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
        // LOGIKA SCROLL-LOCK CERDAS (APPLE STYLE):
        // 1. Saat frame masih berjalan: scroll layar MATI, scroll mouse memutar frame
        // 2. Saat frame sudah habis: scroll layar NYALA, langsung scroll halaman ke bawah
        // 3. Frame TIDAK KEMBALI KE AWAL lagi saat habis
        // ==============================================================
        function handleWheelScroll(e) {{
          const currentTop = getScrollPosition();

          // KONDISI 1: Berada di atas dan frame belum habis (0.0 <= targetProgress < 1.0)
          if (currentTop <= 15 && targetProgress < 1.0) {{
            if (e.deltaY > 0) {{
              // Scroll ke bawah: putar frame maju
              e.preventDefault();
              targetProgress = Math.min(1.0, targetProgress + e.deltaY * 0.0016);
              
              if (targetProgress >= 0.99) {{
                targetProgress = 1.0;
                unlockPageScroll(); // Frame HABIS: NYALAKAN SCROLL LAYAR!
              }} else {{
                lockPageScroll(); // Frame BELUM HABIS: MATIKAN SCROLL LAYAR!
              }}
            }} else if (e.deltaY < 0 && targetProgress > 0.0) {{
              // Scroll ke atas: putar frame mundur
              e.preventDefault();
              targetProgress = Math.max(0.0, targetProgress + e.deltaY * 0.0016);
              lockPageScroll();
            }}
          }}
          // KONDISI 2: Frame SUDAH HABIS (targetProgress >= 1.0)
          else if (targetProgress >= 1.0) {{
            unlockPageScroll(); // Pastikan scroll layar selalu nyala
            
            // Jika user scroll ke atas sampai mentok ke puncak halaman (top <= 5), barulah frame bisa diputar mundur
            if (currentTop <= 5 && e.deltaY < 0) {{
              e.preventDefault();
              targetProgress = Math.max(0.0, targetProgress + e.deltaY * 0.0016);
              lockPageScroll();
            }}
            // Jika scroll ke bawah, BIARKAN HALAMAN BERGULIR SECARA ALAMI (TIDAK e.preventDefault)
          }}
        }}

        // Touch handling untuk layar sentuh / mobile
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

          if (currentTop <= 15 && targetProgress < 1.0) {{
            if (deltaY > 0) {{
              e.preventDefault();
              targetProgress = Math.min(1.0, targetProgress + deltaY * 0.0035);
              if (targetProgress >= 0.99) {{
                targetProgress = 1.0;
                unlockPageScroll();
              }} else {{
                lockPageScroll();
              }}
            }} else if (deltaY < 0 && targetProgress > 0.0) {{
              e.preventDefault();
              targetProgress = Math.max(0.0, targetProgress + deltaY * 0.0035);
              lockPageScroll();
            }}
          }} else if (targetProgress >= 1.0) {{
            unlockPageScroll();
            if (currentTop <= 5 && deltaY < 0) {{
              e.preventDefault();
              targetProgress = Math.max(0.0, targetProgress + deltaY * 0.0035);
              lockPageScroll();
            }}
          }}
        }}

        // Pasang event listeners pada komponen hero dan window utama
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
    components.html(component_html, height=860, scrolling=False)

def render_big_orange_callout_section():
    """
    Merender Section Teks Besar dengan Background Oranye Hangat (Bergaya Apple):
    - Background oranye segar yang memukau
    - Judul besar 'Cek penyakit jeruk Anda sebelum telat!' berwarna putih murni tebal
    - Beri jarak atas lega (margin-top: 80px) agar memberi ruang saat jeruk terbelah
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
            display: inline-block;
            color: #FFE082;
            font-size: 0.92rem;
            font-weight: 800;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            margin-bottom: 12px;
        ">
            DIAGNOSA DINI CASE-BASED REASONING
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

def tampilkan_hero_animasi():
    """
    Fungsi utama yang dipanggil pada app.py.
    Menjalankan styling tema, memuat Hero Section sequence tajam bergaya Apple,
    dan menampilkan Section Teks Besar dengan Background Oranye.
    """
    try:
        st.set_page_config(
            page_title="Sistem Pakar CBR Jeruk",
            page_icon="🍊",
            layout="wide",
            initial_sidebar_state="collapsed"
        )
    except Exception:
        pass

    # 1. Suntikkan styling tema dengan kontras warna tinggi & ruang lebar
    inject_theme_css()

    # 2. Muat frame gambar dan render Hero Section dengan Scroll-Lock cerdas
    frames = load_and_encode_frames("frames")
    if frames:
        render_hero_sequence_section(frames)
    else:
        st.warning("Folder 'frames' tidak ditemukan atau tidak berisi gambar. Pastikan folder 'frames' tersedia di direktori proyek.")

    # 3. Tampilkan Section Teks Besar dengan Background Warna Oranye
    render_big_orange_callout_section()
