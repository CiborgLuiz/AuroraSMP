import discord
import openai
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do .env
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")  # Token do bot do Discord
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # Chave da OpenAI

openai.api_key = OPENAI_API_KEY

# Configurar intents do bot
intents = discord.Intents.default()
intents.messages = True
client = discord.Client(intents=intents)

# História do servidor
HISTORIA_SERVIDOR = (
    "No passado, uma organização científica misteriosa chamada Aurora, responsável por criar as maiores atrocidades em prol da ciência, "
    "fez um experimento e criou uma criatura chamada Nightmare. Inicialmente contido, o Nightmare misteriosamente adquiriu um poder "
    "inimaginável, escapou e se tornou um devorador de galáxias. Sua aparência lembra o sculk do Minecraft, e ele pode mudar de forma. "
    "Cinco guerreiros mágicos - Wagner, TheClown, Jason Stolff e Franchesco - conseguiram selá-lo dentro da Aurora, uma organização "
    "tão grande que pode ser do tamanho de uma galáxia. No presente, o selo do Nightmare está enfraquecendo. Para combater essa ameaça, "
    "o Doutor Nefário, principal cientista da Aurora, decide sequestrar seres de diferentes universos e linhas do tempo para treiná-los e "
    "fortalecê-los, pois o Nightmare continua a crescer em poder a cada ano que passa."
)

@client.event
async def on_ready():
    print(f'✅ Bot conectado como {client.user}')

@client.event
async def on_message(message):
    if client.user.mentioned_in(message) and message.author != client.user:
        pergunta = message.content.replace(f"<@{client.user.id}}>", "").strip()
        
        if "história" in pergunta.lower() or "contexto" in pergunta.lower():
            resposta = HISTORIA_SERVIDOR
        else:
            try:
                resposta = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": pergunta}]
                )["choices"][0]["message"]["content"]
            except Exception as e:
                resposta = "Desculpe, houve um erro ao processar sua pergunta."
                print(e)
        
        await message.channel.send(resposta)

# Iniciar o bot
client.run(TOKEN)
