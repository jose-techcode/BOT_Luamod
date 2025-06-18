import discord
from discord.ext import commands, tasks
import asyncio
from datetime import timedelta
import os
import sys
from storage import DEV_ID
from checks import is_dev

# --Comandos de dev: !reiniciar, !desligar, !verlogs, !limparlogs

# Estrutura cog (herança)

class Dev(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log_bot = "bot.log"
        self.limpar_log.start() # Inicia a limpeza quando o bot for ligado

    def cog_unload(self):
        self.limpar_log.cancel() # Para a task quando o bot for desligado
    
    # Comando: reiniciar

    @commands.command()
    @is_dev()
    async def reiniciar(self, ctx):
        # self.bot.close() fecha o bot primeiramente
        # os.execl(sus.executable, sys.executable, *sys.argv) é a parte que reinicia o bot
        try:
            await ctx.send("Reiniciando...")
            await self.bot.close()
            os.execl(sys.executable, sys.executable, *sys.argv)
        except Exception as e:
            await ctx.send(f"Erro ao reiniciar! Erro: {e}")

    # Comando: desligar

    @commands.command()
    @is_dev()
    async def desligar(self, ctx):
        # self.bot.close() fecha o bot
        try:
            await ctx.send("Desligando...")
            await self.bot.close()
        except Exception as e:
            await ctx.send(f"Erro ao desligar! Erro: {e}")

    # Comando: verlog

    @commands.command()
    @is_dev()
    async def verlog(self, ctx, linhas: int = 10):
        # conteudo é a variável que exibe as últimas linhas 
        try:
            with open("bot.log", "r", encoding="utf-8") as f:
                todas = f.readlines()
                ultimas = todas[-linhas:] if len(todas) >= linhas else todas

            conteudo = ''.join(ultimas)
            if len(conteudo) > 1900:
                conteudo = conteudo[-1900:]  # Evita ultrapassar limite do Discord

            await ctx.send(f"Últimas {linhas} linhas do log:\n```{conteudo}```")
        except Exception as e:
            await ctx.send(f"Erro ao ler o bot.log: {e}")

    # Comando: limparlog (manual)

    @commands.command()
    @is_dev()
    async def limparlog(self, ctx):
        # open serve para abrir o log do bot e o close em seguida para fechar
        try:
            open("bot.log", "w").close()
            await ctx.send("bot.log limpo com sucesso!")
        except Exception as e:
            await ctx.send(f"Erro ao limpar o bot.log! Erro: {e}")

    # Comando: limpar_log (automático)

    @tasks.loop(minutes=10)
    async def limpar_log(self):
        # open serve para abrir o log do bot e o close em seguida para fechar
        try:
            open("bot.log", "w").close()
            print("bot.log limpo com sucesso!")
        except Exception as e:
            print(f"Erro ao limpar o bot.log! Erro: {e}")

    # Comando: before_limpar_log (automático)
    
    @limpar_log.before_loop
    async def before_limpar_log(self):
        await self.bot.wait_until_ready() # Certifica de que a limpeza só funcione quando o bot ligar

async def setup(bot):
    await bot.add_cog(Dev(bot))