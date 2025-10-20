import os
import discord
from openai import AsyncOpenAI

print("🚀 Iniciando bot de Discord...")

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

print(f"🔍 Token leído (primeros 10 chars): {DISCORD_TOKEN[:10] if DISCORD_TOKEN else 'None'}")

if not DISCORD_TOKEN:
    raise ValueError("❌ La variable DISCORD_TOKEN no está configurada en Railway.")
if not OPENAI_API_KEY:
    raise ValueError("❌ La variable OPENAI_API_KEY no está configurada en Railway.")
