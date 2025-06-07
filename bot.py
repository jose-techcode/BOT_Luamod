import discord
from discord.ext import commands
import asyncio
from datetime import timedelta
from storage import DISCORD_TOKEN

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

async def load_cogs():
    cogs = [
        "cogs.geral",
        "cogs.admin"
    ]
    for cog in cogs:
        await bot.load_extension(cog)

# Execução dos cogs:

async def main():
    async with bot:
        await load_cogs()
        await bot.start(DISCORD_TOKEN)

# Executar o bot

asyncio.run(main())