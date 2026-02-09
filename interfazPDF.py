import streamlit as st
import os
from groq import Groq
from dotenv import load_dotenv
from PyPDF2 import PdfReader # La librería que instalamos

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# --- FUNCIÓN PARA EXTRAER TEXTO DE UN PDF ---
def extraer_texto_pdf(nombre_archivo):
    texto_acumulado = ""
    try:
        reader = PdfReader(nombre_archivo)
        for page in reader.pages:
            texto_acumulado += page.extract_text()
        return texto_acumulado
    except Exception as e:
        return f"Error leyendo PDF: {e}"

# --- INTERFAZ ---
st.title("🤖 IA Lector de Catálogos (PDF)")

# Buscamos si hay un PDF en la carpeta
pdf_files = [f for f in os.listdir('.') if f.endswith('.pdf')]

if pdf_files:
    archivo_actual = pdf_files[0] # Tomamos el primer PDF que encuentre
    st.write(f"✅ Leyendo conocimiento de: **{archivo_actual}**")
    contexto_empresa = extraer_texto_pdf(archivo_actual)
else:
    st.warning("⚠️ No encontré ningún archivo PDF en la carpeta.")
    contexto_empresa = ""

# --- LÓGICA DE CHAT ---
if "historial" not in st.session_state:
    st.session_state.historial = []

with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Haz una pregunta sobre el PDF:")
    submit_button = st.form_submit_button(label="Consultar")

if submit_button and user_input and contexto_empresa:
    instrucciones = f"""
    Eres un asistente experto. Usa la información del PDF para responder.
    INFORMACIÓN DEL PDF:
    {contexto_empresa[:5000]} # Limitamos a 5000 caracteres para no saturar
    """

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": instrucciones},
            {"role": "user", "content": user_input}
        ]
    )
    
    respuesta = completion.choices[0].message.content
    st.session_state.historial.append((user_input, respuesta))

for pregunta, respuesta in reversed(st.session_state.historial):
    st.info(f"**Pregunta:** {pregunta}")
    st.success(f"**Respuesta:** {respuesta}")
