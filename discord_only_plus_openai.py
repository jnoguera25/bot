import os
import discord
import asyncio
from openai import AsyncOpenAI

print("🚀 Iniciando bot de Distecna...")

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not DISCORD_TOKEN:
    raise ValueError("❌ Falta DISCORD_TOKEN en Railway.")
if not OPENAI_API_KEY:
    raise ValueError("❌ Falta OPENAI_API_KEY en Railway.")

oa_client = AsyncOpenAI(api_key=OPENAI_API_KEY)
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# === Palabras clave relacionadas con la empresa ===
KEYWORDS = ["distecna", "producto", "soporte", "fabricante", "sistema", "infraestructura", "servidor", "proyecto", "venta", "marketing", "empresa", "pedido", "stock", "tecnología", "marca", "negocio", "compra", "venta"]

async def call_openai(message_text):
    try:
        completion = await asyncio.wait_for(
            oa_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Sos un asistente oficial de la empresa Distecna en Buenos Aires, Argentina. "
                            "Tu función es responder preguntas sobre la empresa, sus productos, proyectos, marcas o soporte técnico. "
                            "Si la consulta no tiene relación con la empresa, respondé amablemente que solo estás autorizado a responder temas relacionados a la empresa."
                        ),
                    },
                    {"role": "user", "content": message_text},
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

@client.event
async def on_ready():
    print(f"✅ Bot conectado como {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    user_text = message.content.strip().lower()

    # --- Filtro local: solo responde si detecta alguna palabra clave ---
    if not any(keyword in user_text for keyword in KEYWORDS):
        await message.channel.send("Sólo estoy entrenado para responder consultas relacionadas con Distecna o sus productos y servicios.")
        return

    print(f"🧠 Usuario {message.author}: {user_text}")
    response = await call_openai(user_text)
    await message.channel.send(response)

client.run(DISCORD_TOKEN)
