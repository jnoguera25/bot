import os
import discord
import asyncio
from openai import AsyncOpenAI

print("🚀 Iniciando bot de Discord...")

# === Cargar variables del entorno (Railway las lee automáticamente) ===
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# === Validación de seguridad ===
if not DISCORD_TOKEN:
    raise ValueError("❌ La variable DISCORD_TOKEN no está configurada en Railway.")
if not OPENAI_API_KEY:
    raise ValueError("❌ La variable OPENAI_API_KEY no está configurada en Railway.")

# === Inicializar cliente de OpenAI ===
oa_client = AsyncOpenAI(api_key=OPENAI_API_KEY)

# === Configurar cliente de Discord ===
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


# === Función para llamar a OpenAI ===
async def call_openai(message_text):
    try:
        completion = await asyncio.wait_for(
            oa_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "user", "content": message_text}
                ],
            ),
            timeout=25
        )
        return completion.choices[0].message.content
    except asyncio.TimeoutError:
        return "⚠️ El modelo tardó demasiado en responder. Intentá de nuevo."
    except Exception as e:
        print("❌ Error al llamar a OpenAI:", e)
        return "❌ Ocurrió un error procesando tu consulta."


# === Eventos de Discord ===
@client.event
async def on_ready():
    print(f"✅ Bot conectado como {client.user}")


@client.event
async def on_message(message):
    # Ignorar mensajes del propio bot
    if message.author == client.user:
        return

    # Ignorar mensajes vacíos o con solo espacios
    if not message.content.strip():
        return

    # Llamar a OpenAI directamente con el texto del mensaje
    user_text = message.content.strip()
    print(f"🧠 Usuario {message.author}: {user_text}")

    response = await call_openai(user_text)
    await message.channel.send(response)


# === Iniciar bot ===
client.run(DISCORD_TOKEN)
