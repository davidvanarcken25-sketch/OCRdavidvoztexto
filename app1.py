import streamlit as st
import cv2
import numpy as np
import pytesseract
from PIL import Image
from googletrans import Translator
import pyttsx3
import tempfile
import os

# --- Configuración de la app ---
st.set_page_config(page_title="OCR Traductor con Voz", page_icon="🧠", layout="centered")
st.title("🧠 OCR + Traducción + Audio")
st.write("Toma una foto con texto, tradúcelo automáticamente y escúchalo en voz alta.")

# --- Sidebar ---
with st.sidebar:
    st.header("Opciones")
    filtro = st.radio("Filtro de imagen", ("Sin filtro", "Invertir colores"))
    idioma_salida = st.selectbox("Traducir a:", ("Español", "Inglés", "Francés", "Alemán", "Italiano"))

# --- Captura de imagen ---
img_file_buffer = st.camera_input("📸 Toma una foto con texto")

if img_file_buffer is not None:
    # Leer la imagen
    bytes_data = img_file_buffer.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

    # Filtro opcional
    if filtro == "Invertir colores":
        cv2_img = cv2.bitwise_not(cv2_img)

    # Convertir a RGB
    img_rgb = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)

    # Mostrar imagen procesada
    st.image(img_rgb, caption="Imagen procesada", use_container_width=True)

    # --- OCR ---
    st.subheader("📄 Texto detectado:")
    texto = pytesseract.image_to_string(img_rgb)
    st.write(texto if texto.strip() else "No se detectó texto en la imagen.")

    # --- Traducción ---
    if texto.strip():
        translator = Translator()

        # Selección del idioma de salida
        lang_codes = {
            "Español": "es",
            "Inglés": "en",
            "Francés": "fr",
            "Alemán": "
