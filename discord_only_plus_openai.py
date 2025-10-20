import os
import discord
import asyncio
from openai import AsyncOpenAI

# --- Cargar variables de entorno (solo desde Railway) ---
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
TOKEN = os.environ.get("DISCORD_TOKEN")

# --- Validación de seguridad ---
if not OPENAI_API_KEY:
    raise ValueError("❌ OPENAI_API_KEY no está configurada en Railway.")
if not TOKEN:
    raise ValueError("❌ DISCORD_TOKEN no está configurada en Railway.")

# --- Inicializar cliente OpenAI ---
oa_client = AsyncOpenAI(api_key=OPENAI_API_KEY)

# --- Configurar cliente de Discord ---
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# --- Función para llamar a OpenAI con manejo de errores y timeout ---
async def call_openai(question):
    try:
        completion = await asyncio.wait_for(
            oa_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": f"Responde como un especialista en tecnología IT lo siguiente: {question}",
                    },
                ],
            ),
            timeout=25
        )
        response = completion.choices[0].message.content
        print("Respuesta:", response)
        return response

    except asyncio.TimeoutError:
        print("⏳ Timeout: la API tardó demasiado.")
        return "⚠️ El modelo tardó demasiado en responder. Probá reformular la pregunta."

    except Exception as e:
        print(f"❌ Error al llamar a OpenAI: {e}")
        return "❌ Ocurrió un error al procesar tu consulta. Intentá nuevamente más tarde."

# --- Eventos de Discord ---
@client.event
async def on_ready():
    print(f"✅ Bot conectado como {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("$question"):
        question = message.content.split("$question", 1)[1].strip()
        print(f"🧠 Pregunta recibida: {question}")

        response = await call_openai(question)
        await message.channel.send(response)

# --- Ejecutar bot ---
if __name__ == "__main__":
    print("🚀 Iniciando bot de Discord...")
    print(f"🔍 Token leído (primeros 10 chars): {DISCORD_TOKEN[:10] if DISCORD_TOKEN else 'None'}")
    client.run(TOKEN)
