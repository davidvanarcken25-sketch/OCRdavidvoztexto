import streamlit as st
import speech_recognition as sr
from gtts import gTTS
from io import BytesIO

st.title("🎙️ Voz a Texto y Texto a Voz")

# ------------------------
# Sección 1: Voz → Texto
# ------------------------
st.header("🎧 Grabar voz y convertir a texto")

if st.button("🎤 Grabar voz"):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Escuchando... habla ahora 🎙️")
        audio = recognizer.listen(source)
        try:
            texto = recognizer.recognize_google(audio, language="es-ES")
            st.success(f"Texto reconocido: {texto}")
            # Reproduce automáticamente el texto reconocido
            tts = gTTS(text=texto, lang="es")
            audio_buffer = BytesIO()
            tts.write_to_fp(audio_buffer)
            audio_buffer.seek(0)
            st.audio(audio_buffer, format="audio/mp3")
        except:
            st.error("No se pudo reconocer la voz. Intenta nuevamente.")

# ------------------------
# Sección 2: Texto → Voz
# ------------------------
st.header("✍️ Escribe tu narración")

texto_manual = st.text_area("Escribe algo para escucharlo en voz alta:", "")

if st.button("🔊 Escuchar texto escrito"):
    if texto_manual.strip() != "":
        tts = gTTS(text=texto_manual, lang="es")
        audio_buffer = BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        st.audio(audio_buffer, format="audio/mp3")
    else:
        st.warning("Por favor escribe algo primero.")
