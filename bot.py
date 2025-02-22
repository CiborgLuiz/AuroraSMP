import discord
import openai
import asyncio
import os
from dotenv import load_dotenv
from discord.ext import commands

# 🔑 Configuração do bot e API OpenAI
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")  # Token do bot do Discord
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # Chave da OpenAI

openai.api_key = OPENAI_API_KEY
client_openai = openai.OpenAI()

# ⚙️ Configuração do bot
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
bot = commands.Bot(command_prefix="!", intents=intents)

# 📖 História do Servidor
HISTORIA_SERVIDOR = """
No passado, a organização científica multiversal Aurora criou uma criatura chamada Nightmare.
Ele saiu do controle e se tornou um devorador de galáxias. Cinco pessoas com poderes mágicos
(Wagner, TheClown, Jason Stolff e Franchesco) conseguiram selá-lo. No presente, o selo está
enfraquecendo, e o Doutor Nefário sequestra pessoas de diferentes universos para fortalecê-las
e prepará-las contra a ameaça iminente.
"""

# 🛠️ Função para perguntar ao ChatGPT
async def perguntar_ao_chatgpt(pergunta):
    try:
        resposta = client_openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um assistente especializado no servidor Aurora SMP BR."},
                {"role": "user", "content": pergunta}
            ]
        )
        return resposta.choices[0].message.content
    except Exception as e:
        print(f"Erro na API do ChatGPT: {e}")
        return "Desculpe, houve um erro ao processar sua pergunta."

# 🗣️ Evento: Quando o bot estiver pronto
@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user}")

# 💬 Evento: Quando uma mensagem for enviada
@bot.event
async def on_message(message):
    if message.author.bot:
        return  # Ignorar mensagens de outros bots

    if bot.user in message.mentions:
        pergunta = message.content.replace(f"<@{bot.user.id}>", "").strip()

        if "história" in pergunta.lower():
            resposta = HISTORIA_SERVIDOR
        else:
            resposta = await perguntar_ao_chatgpt(pergunta)

        await message.channel.send(resposta)

    await bot.process_commands(message)

# 🚀 Iniciar o bot
bot.run(TOKEN)
