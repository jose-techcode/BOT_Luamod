import discord
from discord.ext import commands
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
    
    # Comando: !reiniciar

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

    # Comando: !desligar

    @commands.command()
    @is_dev()
    async def desligar(self, ctx):
        # self.bot.close() fecha o bot
        try:
            await ctx.send("Desligando...")
            await self.bot.close()
        except Exception as e:
            await ctx.send(f"Erro ao desligar! Erro: {e}")

    # Comando: !verlogs

    @commands.command()
    @is_dev()
    async def verlogs(self, ctx, linhas: int = 10):
        # conteudo é a variável que exibe as últimas linhas 
        try:
            with open("bot.log", "r", encoding="utf-8") as f:
                todas = f.readlines()
                ultimas = todas[-linhas:] if len(todas) >= linhas else todas

            conteudo = ''.join(ultimas)
            if len(conteudo) > 1900:
                conteudo = conteudo[-1900:]  # evita ultrapassar limite do Discord

            await ctx.send(f"Últimas {linhas} linhas do log:\n```{conteudo}```")
        except Exception as e:
            await ctx.send(f"Erro ao ler o log: {e}")

    # Comando: !limparlogs

    @commands.command()
    @is_dev()
    async def limparlogs(self, ctx):
        # open serve para abrir o log do bot e o close em seguida para fechar
        try:
            open("bot.log", "w").close()
            await ctx.send("Arquivo de log limpo com sucesso.")
        except Exception as e:
            await ctx.send(f"Erro ao limpar log: {e}")

async def setup(bot):
    await bot.add_cog(Dev(bot))