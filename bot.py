import discord
import openai
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")  # Token do bot do Discord
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # Chave da API do ChatGPT

openai.api_key = OPENAI_API_KEY

# Configurar intents do bot
intents = discord.Intents.default()
intents.messages = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Bot conectado como {client.user}')

@client.event
async def on_message(message):
    if client.user.mentioned_in(message) and message.author != client.user:
        pergunta = message.content.replace(f"<@{client.user.id}>", "").strip()
        if pergunta:
            resposta = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": pergunta}]
            )
            await message.channel.send(resposta["choices"][0]["message"]["content"])
        else:
            await message.channel.send("Olá! Como posso ajudar?")

# Iniciar o bot
client.run(TOKEN)
