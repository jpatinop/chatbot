import streamlit as st
import os
from groq import Groq
from PyPDF2 import PdfReader

# Configuración de la página
st.set_page_config(page_title="IA Business Assistant", page_icon="🤖")

# Conexión con los Secrets de Streamlit Cloud
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.title("🤖 Asistente IA Corporativo")
st.markdown("Suba su manual y chatee con la información.")

# --- BARRA LATERAL PARA EL PDF ---
with st.sidebar:
    st.header("Documentación")
    archivo_subido = st.file_uploader("Cargar PDF de conocimiento", type="pdf")

# --- PROCESAMIENTO DEL PDF ---
contexto_empresa = ""
if archivo_subido:
    reader = PdfReader(archivo_subido)
    for page in reader.pages:
        contexto_empresa += page.extract_text()
    st.sidebar.success("✅ PDF cargado con éxito")

# --- LÓGICA DEL CHAT MODERNO ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial con burbujas modernas
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Barra de chat inferior (La que antes daba error)
if prompt := st.chat_input("¿En qué puedo ayudarte hoy?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Respuesta de la IA
    with st.chat_message("assistant"):
        instrucciones = f"Eres un asistente experto. Usa este contexto: {contexto_empresa[:8000]}"
        
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": instrucciones},
                {"role": "user", "content": prompt}
            ]
        )
        respuesta = completion.choices[0].message.content
        st.markdown(respuesta)
        st.session_state.messages.append({"role": "assistant", "content": respuesta})
