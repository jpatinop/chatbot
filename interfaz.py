import streamlit as st
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# --- FUNCIÓN PARA LEER EL ARCHIVO ---
def cargar_contexto():
    try:
        with open("conocimiento.txt", "r", encoding="utf-8") as file:
            return file.read()
    except Exception as e:
        return "No hay información adicional disponible."

# --- INTERFAZ ---
st.title("🤖 Asistente de Ventas IA")
contexto_empresa = cargar_contexto()

if "historial" not in st.session_state:
    st.session_state.historial = []

with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Pregunta sobre nuestros servicios:")
    submit_button = st.form_submit_button(label="Consultar")

if submit_button and user_input:
    # El "Prompt" con Contexto (RAG básico)
    instrucciones = f"""
    Eres un asistente de ventas de la inmobiliaria Tech-Home. 
    Usa estrictamente la siguiente información para responder al cliente:
    ---
    {contexto_empresa}
    ---
    Si el cliente pregunta algo que NO está en la información anterior, 
    responde amablemente que deben contactar a un asesor humano al 555-1234.
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

# Mostrar historial
for pregunta, respuesta in reversed(st.session_state.historial):
    st.info(f"**Cliente:** {pregunta}")
    st.success(f"**Asistente:** {respuesta}")
