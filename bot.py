import discord
from discord.ext import commands
import asyncio
import logging
from datetime import timedelta
from storage import DISCORD_TOKEN

# Configuração simples de log com arquivo

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="bot.log",
    filemode="a",  # 'a' para adicionar ao final do arquivo
    encoding="utf-8"
)
logging.info("Bot iniciado com sucesso.")
logging.warning("Algo inesperado aconteceu.")
logging.error("Erro crítico.")

# Permissões do bot:

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="<?", intents=intents)

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
        "cogs.admin",
        "cogs.dev",
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