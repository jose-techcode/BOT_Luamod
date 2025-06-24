import discord
from discord.ext import commands, tasks
import asyncio
from datetime import timedelta
import threading
import psutil
import platform
import discord
import datetime
import logging
import os
import sys
import time
from storage import DEV_ID
from checks import is_dev

# Estrutura cog (herança)

class Dev(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.restarting = False
        self.restart_loop.start()
        self.log_bot = "bot.log"
        self.clean_log.start() # Inicia a limpeza quando o bot for ligado

    def cog_unload(self):
        self.clean_log.cancel() # Para a task quando o bot for desligado
    
    # Comando: restart

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    @is_dev()
    async def restart(self, ctx):
        # self.bot.close() fecha o bot primeiramente
        # os.execl(sus.executable, sys.executable, *sys.argv) é a parte que reinicia o bot
        try:
            await ctx.send("Reiniciando...")
            await self.bot.close()
            os.execl(sys.executable, sys.executable, *sys.argv)
        except Exception as e:
            logging.exception(f"Erro no comando.")
            if ctx.author.id == DEV_ID:
                await ctx.send(f"Erro: {e}")
            else:
                await ctx.send("Algo deu errado...")

    # Comando: toswitchoff

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    @is_dev()
    async def toswitchoff(self, ctx):
        # self.bot.close() fecha o bot
        try:
            await ctx.send("Desligando...")
            await self.bot.close()
        except Exception as e:
            logging.exception(f"Erro no comando.")
            if ctx.author.id == DEV_ID:
                await ctx.send(f"Erro: {e}")
            else:
                await ctx.send("Algo deu errado...")

    # Comando: log

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    @is_dev()
    async def log(self, ctx, lines: int = 10):
        # content é a variável que exibe as últimas linhas 
        try:
            with open("bot.log", "r", encoding="utf-8") as f:
                all = f.readlines()
                lasts = all[-lines:] if len(all) >= lines else all

            content = ''.join(lasts)
            if len(content) > 1900:
                content = content[-1900:]  # Evita ultrapassar limite do Discord

            await ctx.send(f"Últimas {lines} linhas do log:\n```{content}```")
        except Exception as e:
            logging.exception(f"Erro no comando.")
            if ctx.author.id == DEV_ID:
                await ctx.send(f"Erro: {e}")
            else:
                await ctx.send("Algo deu errado...")

    # Comando: clearlog

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    @is_dev()
    async def clearlog(self, ctx):
        # open serve para abrir o log do bot e o close em seguida para fechar
        try:
            open("bot.log", "w").close()
            await ctx.send("bot.log limpo com sucesso!")
        except Exception as e:
            logging.exception(f"Erro no comando.")
            if ctx.author.id == DEV_ID:
                await ctx.send(f"Erro: {e}")
            else:
                await ctx.send("Algo deu errado...")

    # Comando: reloadcog

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    @is_dev()
    async def reloadcog(self, ctx, name: str):
        # self.bot.reload_extension serve para recarregar a cog selecionada
        try:
            await self.bot.reload_extension(f"cogs.{name}")
            await ctx.send(f"Cog `cogs.{name}` recarregada com sucesso!")
        except Exception as e:
            logging.exception(f"Erro no comando.")
            if ctx.author.id == DEV_ID:
                await ctx.send(f"Erro: {e}")
            else:
                await ctx.send("Algo deu errado...")

    # Comando: debug

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    @is_dev()
    async def debug(self, ctx):
        try:
            guilds = len(self.bot.guilds)
            users = len(set(self.bot.get_all_members()))
            
            uptime_seconds = int(time.time() - self.bot.start_time) # CONSERTO
            uptime_str = str(datetime.timedelta(seconds=uptime_seconds)) # CONSERTO
            status = "Online" if self.bot.is_ready() else "Desconectado"

            python_version = platform.python_version()

            discord_version = discord.__version__

            system = platform.system()

            architecture = platform.machine()

            process = psutil.Process()
            
            cpu = process.cpu_percent(interval=0.5)  # Porcentagem (0.5s de medição)
            
            memory = process.memory_info().rss / 1024**2  # MB

            threads_actives = len(threading.enumerate())

            tasks_actives = len(asyncio.all_tasks())

            latency = round(self.bot.latency * 1000)
            
            cogs = list(self.bot.cogs.keys())
            
            commands = len(self.bot.commands)
 
            await ctx.send(
            f"Nome: {self.bot.user.name}\n"
            f"ID: {self.bot.user.id}\n"
            f"Quantidade de guilds: {guilds}\n"
            f"Quantidade de usuários únicos: {users}\n"
            f"Tempo de atividade: {uptime_str}\n"
            f"Status de conexão: {status}\n"
            f"Versão da linguagem de programação python: {python_version}\n"
            f"Versão da biblioteca discord: {discord_version}\n"
            f"Sistema operacional: {system}\n"
            f"Arquitetura: {architecture}\n"
            f"CPU: {cpu: .1f}%\n"
            f"Memória: {memory:.2f}MB\n"
            f"Threads ativas: {threads_actives}\n"
            f"Atividades ativas: {tasks_actives}\n"
            f"Latência: {latency}ms\n"
            f"Quantidade de cogs carregadas: {len(cogs)}\n"
            f"Cogs carregadas: {cogs}\n"
            f"Quantidade de comandos registrados: {commands}"
            )
        except Exception as e:
            logging.exception(f"Erro no comando.")
            if ctx.author.id == DEV_ID:
                await ctx.send(f"Erro: {e}")
            else:
                await ctx.send("Algo deu errado...")

    # Comando: restart (automático)

    @tasks.loop(hours=2)
    async def restart_loop(self):
        print("Reiniciando!")
        await self.bot.close()
        os.execl(sys.executable, sys.executable, *sys.argv)

    @restart_loop.before_loop
    async def before_reiniciar(self):
        await self.bot.wait_until_ready() # Certifica de que a reiniciação só funcione quando o bot estiver ligado
        print("Reiniciação em 2 horas!")
        await asyncio.sleep(60 * 120)

    # Comando: clean_log (automático)

    @tasks.loop(hours=1)
    async def clean_log(self):
        # open serve para abrir o log do bot e o close em seguida para fechar
        open("bot.log", "w").close()
        print("bot.log limpo com sucesso!")
    
    @clean_log.before_loop
    async def before_clean_log(self):
        await self.bot.wait_until_ready() # Certifica de que a limpeza só funcione quando o bot ligar

async def setup(bot):
    await bot.add_cog(Dev(bot))