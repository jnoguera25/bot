from dotenv import load_dotenv
from openai import AsyncOpenAI
import discord
import os
import asyncio

# --- Cargar variables del entorno (.env) ---
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DISCORD_TOKEN = os.getenv("TOKEN")

# --- Inicializar cliente OpenAI ---
oa_client = AsyncOpenAI(api_key=OPENAI_API_KEY)

# --- Configurar cliente de Discord ---
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


# --- Función que llama a la API de OpenAI con timeout y manejo de errores ---
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
            timeout=25  # tiempo máximo de espera en segundos
        )

        # Acceso correcto al contenido
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
    print(f"✅ Logged in as {client.user}")


@client.event
async def on_message(message):
    # Ignorar mensajes del propio bot
    if message.author == client.user:
        return

    # Comando personalizado
    if message.content.startswith("$question"):
        question = message.content.split("$question", 1)[1].strip()
        print(f"🧠 Pregunta: {question}")

        # Llamar a OpenAI
        response = await call_openai(question)

        # Enviar respuesta a Discord
        await message.channel.send(response)


# --- Ejecutar bot ---
if __name__ == "__main__":
    if not OPENAI_API_KEY:
        print("⚠️ No se encontró la variable OPENAI_API_KEY en tu archivo .env")
    elif not DISCORD_TOKEN:
        print("⚠️ No se encontró la variable TOKEN en tu archivo .env")
    else:
        client.run(DISCORD_TOKEN)
