import os
import discord
import asyncio
from openai import AsyncOpenAI

print("🚀 Iniciando bot de Discord...")

# === Cargar variables del entorno (Railway las lee automáticamente) ===
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


# print(f"🔍 Primeros 10 caracteres del token: {DISCORD_TOKEN[:10] if DISCORD_TOKEN else 'No encontrado'}")


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

async def call_openai(question):
    try:
        completion = await asyncio.wait_for(
            oa_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "user", "content": f"Responde como un especialista en tecnología IT lo siguiente: {question}"}
                ],
            ),
            timeout=25
        )
        return completion.choices[0].message.content
    except Exception as e:
        print("❌ Error al llamar a OpenAI:", e)
        return "Hubo un error procesando tu consulta."

@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("$question"):
        question = message.content[len("$question "):].strip()
        print(f"🧠 Pregunta: {question}")
        response = await call_openai(question)
        await message.channel.send(response)

# === Iniciar bot ===
client.run(DISCORD_TOKEN)
