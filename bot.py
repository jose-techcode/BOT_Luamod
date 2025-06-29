import discord
from discord.ext import commands
import asyncio
import logging
import time
import json
import os
import uvicorn
from datetime import timedelta
from storage import DISCORD_TOKEN
from api import application

# Configuração simples de log com arquivo

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s", # asctime = data, levelname = nível do erro, message = conteúdo do erro
    filename="bot.log", # nome do arquivo que armazena o log de terminal do bot
    filemode="a",  # 'a' para adicionar ao final do arquivo
    encoding="utf-8" # código universal para aceitar todos os caracteres no bot.log
)
logging.info("Teste.")
logging.warning("Teste.")
logging.error("Teste.")

# Permissões do bot:

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=".", intents=intents)

# Uptime do bot

bot.start_time = time.time()

# Armazenar log_channels na memória

FILE_LOG = 'log_channels.json'

def salvar_log_channels(dados):
    with open(FILE_LOG, 'w') as j:
        json.dump(dados, j, indent=4)

def carregar_log_channels():
    if os.path.exists(FILE_LOG):
        with open(FILE_LOG, 'r') as j:
            informations = json.load(j)
            return {int(k): v for k, v in informations.items()}
    return {}

# Carregar log_channels

bot.log_channels = carregar_log_channels()

# Quando o bot estiver ativo/online

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user.name} - {bot.user.id}")
    activity = discord.Game(name="Lua")
    await bot.change_presence(status=discord.Status.online, activity=activity)

# Tratamento de erros globais

@bot.event
async def on_command_error(ctx, error):
    
    # Tratamento de erros para ignorar comandos não existentes
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"Comando não encontrado: {ctx.message.content}")
        return

    # Tratamento de erros com flood de comandos

    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"Aguarde {error.retry_after:.1f}s para usar esse comando novamente.")
        return
    
    # Tratamento de erros com usuário sem permissão

    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Tu não tem permissão para isso.")
        return
    
    # Tratamento de erros com bot sem permissão

    if isinstance(error, commands.BotMissingPermissions):
        await ctx.send("Eu não tenho permissão para isso.")
        return
    
    # Tratamento de erros com argumentos inválidos

    if isinstance(error, commands.BadArgument):
        await ctx.send("Argumento(s) inválido(s). Verifique o comando em ajuda.")
        return

    # Tratamento de erros sem argumentos

    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Sem argumento(s) obrigatório(s). Verifique o comando em ajuda.")
        return

    # Tratamento de erros com as cogs

    logging.exception(f"Erro não tratado globalmente: {ctx.command}")
    raise error

# Carregar cogs

async def load_cogs():
    cogs = [
        "cogs.geral",
        "cogs.admin",
        "cogs.dev",
        "cogs.log",
        "cogs.ia"
    ]
    for cog in cogs:
        await bot.load_extension(cog)

# Execução dos cogs:

async def start_bot():
    async with bot:
        await load_cogs()
        await bot.start(DISCORD_TOKEN)

# API de status e API REST

async def start_api():

    application.state.bot = bot
    
    bot_task = asyncio.create_task(start_bot())
    
    api_task = asyncio.create_task(
        uvicorn.Server(
            uvicorn.Config(application, host="127.0.0.1", port=8000, log_level="info")
        ).serve()
    )

    await asyncio.gather(bot_task, api_task) 

# Executar o bot

if __name__ == "__main__":
    asyncio.run(start_api())