from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

# Si no has configurado el .env, puedes poner la clave directo para probar:
# client = Groq(api_key="TU_KEY_DE_GROQ_AQUI")
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

completion = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": "Hola, ¿estás funcionando?"}]
)

print(completion.choices[0].message.content)
