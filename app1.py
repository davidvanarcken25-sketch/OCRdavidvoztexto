import streamlit as st
import cv2
import numpy as np
import pytesseract
from PIL import Image
from gtts import gTTS
from googletrans import Translator
import os
import time
import glob

# ================================
# CONFIGURACIÓN DE PÁGINA
# ================================
st.set_page_config(page_title="OCR Traductor y Narrador", page_icon="🧠", layout="centered")

st.markdown("""
    <style>
        .title {
            text-align: center;
            color: #0078FF;
            font-size: 40px;
            font-weight: bold;
        }
        .subtitle {
            text-align: center;
            font-size: 18px;
            color: #555;
        }
        .result-box {
            background-color: #EAF4FF;
            padding: 15px;
            border-radius: 10px;
            border-left: 6px solid #0078FF;
            margin-top: 15px;
        }
    </style>
""", unsafe_allow_html=True)

# ================================
# ENCABEZADO
# ================================
st.markdown("<div class='title'>📷 OCR Traductor & Narrador</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Toma una foto con texto, tradúcelo y escúchalo en voz alta.</div>", unsafe_allow_html=True)
st.divider()

# ================================
# CAPTURA DE IMAGEN
# ================================
img_file_buffer = st.camera_input("📸 Toma una foto con texto")

with st.sidebar:
    st.header("Opciones")
    filtro = st.radio("Aplicar Filtro:", ('Con Filtro', 'Sin Filtro'))
    idioma_salida = st.selectbox("Traducir a:", ("Español", "Inglés", "Francés", "Alemán", "Italiano"))

# ================================
# PROCESAMIENTO
# ================================
if img_file_buffer is not None:
    bytes_data = img_file_buffer.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

    if filtro == 'Con Filtro':
        cv2_img = cv2.bitwise_not(cv2_img)

    img_rgb = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
    text = pytesseract.image_to_string(img_rgb)

    st.markdown("### 🧾 Texto Detectado:")
    st.markdown(f"<div class='result-box'>{text}</div>", unsafe_allow_html=True)

    # ================================
    # TRADUCCIÓN
    # ================================
    translator = Translator()
    if idioma_salida == "Español":
        output_lang = "es"
    elif idioma_salida == "Inglés":
        output_lang = "en"
    elif idioma_salida == "Francés":
        output_lang = "fr"
    elif idioma_salida == "Alemán":
        output_lang = "de"
    elif idioma_salida == "Italiano":
        output_lang = "it"

    traduccion = translator.translate(text, dest=output_lang)
    st.markdown("### 🌍 Texto Traducido:")
    st.markdown(f"<div class='result-box'>{traduccion.text}</div>", unsafe_allow_html=True)

    # ================================
    # AUDIO
    # ================================
    os.makedirs("temp", exist_ok=True)
    tts = gTTS(traduccion.text, lang=output_lang)
    audio_path = "temp/audio_traducido.mp3"
    tts.save(audio_path)

    st.markdown("### 🔊 Escucha el resultado:")
    st.audio(audio_path, format="audio/mp3")

    # Animación al finalizar
    st.snow()

    # ================================
    # LIMPIEZA
    # ================================
    def remove_files(n):
        mp3_files = glob.glob("temp/*mp3")
        now = time.time()
        n_days = n * 86400
        for f in mp3_files:
            if os.stat(f).st_mtime < now - n_days:
                os.remove(f)

    remove_files(2)

    


