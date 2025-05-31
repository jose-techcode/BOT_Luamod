import discord
from discord.ext import commands
import asyncio
from datetime import timedelta
from dotenv import load_dotenv
import os


# Pegar e carregar variáveis do .env


load_dotenv()

token = os.getenv("DISCORD_TOKEN")


# Permissões do bot:


intents = discord.Intents.all()

bot = commands.Bot(command_prefix="!", intents=intents)


# Quando o bot estiver ativo/online:


@bot.event
async def on_ready():
    print(f"[LOG] Bot conectado como {bot.user.name} - {bot.user.id}")


# Ignorar comandos não existentes:


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        print(f"[ERRO] Comando não encontrado: {ctx.message.content}")
        return
    else:
        raise error  # Outros erros continuam aparecendo


# Carregar cogs
# cogs é uma lista que será carregada


async def load_cogs():
    cogs = [
        "cogs.geral",
        "cogs.admin"
    ]
    for cog in cogs:
        await bot.load_extension(cog)


# Execução dos cogs:
# main é uma função que vai executar as cogs


async def main():
    async with bot:
        await load_cogs()
        await bot.start(token)


# Executar o bot
# executar todo o código

asyncio.run(main())