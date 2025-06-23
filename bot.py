import discord
from discord.ext import commands
import asyncio
import logging
import time
from datetime import timedelta
from storage import DISCORD_TOKEN

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
bot = commands.Bot(command_prefix="?", intents=intents)
bot.start_time = time.time()

# Quando o bot estiver ativo/online:

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
        "cogs.log"
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