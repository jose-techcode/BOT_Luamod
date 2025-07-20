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

# Log configuration with file

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s", # asctime = date, levelname = error level, message = error content
    filename="bot.log", # name of the file that stores the bot's terminal log
    filemode="a",  # 'a' to add to the end of the file
    encoding="utf-8" # universal code to accept all characters in bot.log
)
logging.info("Teste.")
logging.warning("Teste.")
logging.error("Teste.")

# Permissions of bot:

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=".", intents=intents)

# Uptime of bot

bot.start_time = time.time()

# Store log_channels in memory

FILE_LOG = 'log_channels.json'

def save_log_channels(data):
    with open(FILE_LOG, 'w') as j:
        json.dump(data, j, indent=4)

def load_log_channels():
    if os.path.exists(FILE_LOG):
        with open(FILE_LOG, 'r') as j:
            informations = json.load(j)
            return {int(k): v for k, v in informations.items()}
    return {}

# Load log_channels

bot.log_channels = load_log_channels()

# When the bot is active/online

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user.name} - {bot.user.id}")
    activity = discord.Game(name="Lua")
    await bot.change_presence(status=discord.Status.online, activity=activity)

# Global error handling

@bot.event
async def on_command_error(ctx, error):
    
    # Error handling to ignore non-existent commands


    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"Comando não encontrado: {ctx.message.content}")
        return

    # Error handling with command flood

    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"Aguarde {error.retry_after:.1f}s para usar esse comando novamente.")
        return
    
    # Error handling with user without permission

    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Tu não tem permissão para isso.")
        return
    
    # Error handling with bot without permission

    if isinstance(error, commands.BotMissingPermissions):
        await ctx.send("Eu não tenho permissão para isso.")
        return
    
    # Error handling with invalid arguments

    if isinstance(error, commands.BadArgument):
        await ctx.send("Argumento(s) inválido(s). Verifique o comando em ajuda.")
        return

    # Error handling without arguments

    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Sem argumento(s) obrigatório(s). Verifique o comando em ajuda.")
        return

    # Error handling with cogs

    logging.exception(f"Erro não tratado globalmente: {ctx.command}")
    raise error

# Load cogs

async def load_cogs():
    cogs = [
        "cogs.geral",
        "cogs.mod",
        "cogs.dev",
        "cogs.log",
        "cogs.chatbot"
    ]
    for cog in cogs:
        await bot.load_extension(cog)

# Execution of cogs:

async def start_bot():
    async with bot:
        await load_cogs()
        await bot.start(DISCORD_TOKEN)

# API of status amd API REST

async def start_api():

    application.state.bot = bot
    
    bot_task = asyncio.create_task(start_bot())
    
    api_task = asyncio.create_task(
        uvicorn.Server(
            uvicorn.Config(application, host="127.0.0.1", port=8000, log_level="info")
        ).serve()
    )

    await asyncio.gather(bot_task, api_task) 

# Execution of bot

if __name__ == "__main__":
    asyncio.run(start_api())