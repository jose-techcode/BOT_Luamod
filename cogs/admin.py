import discord
from discord.ext import commands
import asyncio
from datetime import timedelta
from storage import DEV_ID
import logging
import re
import json
import os

# --Comandos de moderação: avisar, desavisar, avisos, avisados, apagar, lentear, trancar, destrancar, silenciar, dessilenciar, expulsar, banir, desbanir

# JSON

ARQUIVO_JSON = "warns.json"

def carregar_avisos():
        if not os.path.exists(ARQUIVO_JSON):
            return {}
        with open(ARQUIVO_JSON, "r") as j:
            return json.load(j)
    
def salvar_avisos(dados):
        with open(ARQUIVO_JSON, "w") as j:
            json.dump(dados, j, indent=4)

# Estrutura cog (herança)

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.regex_links = [
    re.compile(r"https?://\S+"), # Regex de link genérico
    re.compile(r"\[([^\]]+)\]\((https?://[^\s\)]+)\)"), # Regex de link mais específico
    re.compile(r"(https?:\/\/)?(www\.)?(discord\.gg|discord\.com\/invite)\/[a-zA-Z0-9]+"), # Regex de link de discord
    re.compile(r"https?://(bit\.ly|tinyurl\.com|t\.co|is\.gd|goo\.gl)/\S+"), # Regex de links variados
    re.compile(r"\b(?:www\.)?[a-zA-Z0-9\-]+\.[a-z]{2,}(?:\/\S*)?\b") # Regex de falso positivo
]

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return # Ignora mensagens do bot
        # Verifica link
        for regex in self.regex_links:
            if regex.search(message.content):
                await message.delete()
                break

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if after.author == self.bot.user:
            return  # Ignora edições feitas pelo bot
        for regex in self.regex_links:
            if regex.search(after.content):
                await after.delete()
                break

    # Comando: avisar

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def avisar(self, ctx, member: commands.MemberConverter, *, motivo: str):
        try:
            
            warns = carregar_avisos()
            user_id = str(member.id)
            guild_id = str(ctx.guild.id)
            
            if guild_id not in warns:
                warns[guild_id] = {}
            
            if user_id not in warns[guild_id]:
                warns[guild_id][user_id] = []

            warns[guild_id][user_id].append(motivo)
            salvar_avisos(warns)
            await ctx.send(f"{member.mention} foi avisado por: {motivo}")
        
        except Exception as e:
            logging.exception(f"Erro no comando.")
            if ctx.author.id == DEV_ID:
                await ctx.send(f"Erro: {e}")
            else:
                await ctx.send("Algo deu errado...")

    # Comando: desavisar

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def desavisar(self, ctx, member: commands.MemberConverter):
        try:
            
            warns = carregar_avisos()
            user_id = str(member.id)
            guild_id = str(ctx.guild.id)
            
            if guild_id in warns and user_id in warns[guild_id]:
                del warns[guild_id][user_id]
                
                if not warns[guild_id]:
                    del warns[guild_id]
                    
                salvar_avisos(warns)
                await ctx.send(f"{member.mention} foi desavisado completamente!")
            
            else:
                await ctx.send(f"{member.mention} não tem avisos registrados neste servidor!")
        
        except Exception as e:
            logging.exception(f"Erro no comando.")
            if ctx.author.id == DEV_ID:
                await ctx.send(f"Erro: {e}")
            else:
                await ctx.send("Algo deu errado...")


    # Comando: avisos

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def avisos(self, ctx, member: commands.MemberConverter = None):
        # self.bot.fetch_user serve para buscar o ID do usuário pela API do discord
        # motivos é uma variável que enumera os motivos dos avisos em determinado usuário
        try:
            
            member = member or ctx.author
            user_id = str(member.id)
            guild_id = str(ctx.guild.id)
            
            warns = carregar_avisos()
            warns_guild = warns.get(guild_id, {})
            warns_usuario = warns_guild.get(user_id, [])
            
            if warns_usuario:
                message = "**Avisos:**\n\n"
                reasons = "\n".join(f"{i+1}. {m}" for i, m in enumerate(warns_usuario))
                member = await self.bot.fetch_user(int(user_id))
                message += f"{member.mention} - {member} - {member.id} - {len(warns_usuario)} aviso(s):```{reasons}```"
                await ctx.send(message[:2000]) # Limite de caracteres
            
            else:
                await ctx.send(f"{member.mention} não tem nenhum aviso registrado.")
        
        except Exception as e:
            logging.exception(f"Erro no comando.")
            if ctx.author.id == DEV_ID:
                await ctx.send(f"Erro: {e}")
            else:
                await ctx.send("Algo deu errado...")

    # Comando: listaavisos

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def listaavisos(self, ctx):
        try:
            
            guild_id = str(ctx.guild.id)
            warns = carregar_avisos()
            warns_guild = warns.get(guild_id, {})
            
            if not warns_guild:
                await ctx.send("Nenhum usuário foi avisado neste servidor.")
                return
            
            mensagem = "**Lista de usuários avisados neste servidor:**\n\n"
            
            for user_id, lista in warns_guild.items():
                if not lista:
                    continue  # Ignora se a lista estiver vazia
                
                membro = await self.bot.fetch_user(int(user_id))
                mensagem += f"```{membro.name} - {membro} — {membro.id} - aviso(s): {len(lista)}```\n"
            
            if mensagem.strip() == "**Lista de usuários avisados neste servidor:**":
                await ctx.send("Nenhum usuário tem avisos ativos neste servidor.")
            
            else:
                await ctx.send(mensagem[:2000])
        
        except Exception as e:
            logging.exception(f"Erro no comando.")
            if ctx.author.id == DEV_ID:
                await ctx.send(f"Erro: {e}")
            else:
                await ctx.send("Algo deu errado...")

    # Comando: apagar

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def apagar(self, ctx, quantidade_mensagens: int):
        # ctx.channel.purge serve para poder apagar a quantidade de mensagens definidas no canal
        # limit serve para definir um limite de mensagens apagadas
        # delete_after=5 é a quantidade de segundos que o bot levará para apagar as mensagens
        try:
            await ctx.channel.purge(limit=quantidade_mensagens)
            await ctx.send(f"Foram apagadas {quantidade_mensagens} mensagens.", delete_after=5)
        except Exception as e:
            logging.exception(f"Erro no comando.")
            if ctx.author.id == DEV_ID:
                await ctx.send(f"Erro: {e}")
            else:
                await ctx.send("Algo deu errado...")

    # Comando: lentear

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def lentear(self, ctx, tempo: int):
        # ctx.channel.edit serve editar as configurações do canal
        # slowmode_delay é para especificar o tipo de edição que será realizado no servidor
        try:
            await ctx.channel.edit(slowmode_delay=tempo)
            await ctx.send(f"O modo lento foi definido para {tempo} segundos")
        except Exception as e:
            logging.exception(f"Erro no comando.")
            if ctx.author.id == DEV_ID:
                await ctx.send(f"Erro: {e}")
            else:
                await ctx.send("Algo deu errado...")

    # Comando: trancar

    @commands.command()
    @commands.has_permissions(manage_channels = True)
    async def trancar(self, ctx):
        # overwirte é a variável que permite sobrescrever as permissões do canal de um servidor
        # overwirte.send_messages é referente a poder ou a não poder mandar mensagens em determinado canal
        # ctx.channel.set_permissions é para definir as permissões do canal
        try:
            overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
            overwrite.send_messages = False
            await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
            await ctx.send("Canal trancado!")
        except Exception as e:
            logging.exception(f"Erro no comando.")
            if ctx.author.id == DEV_ID:
                await ctx.send(f"Erro: {e}")
            else:
                await ctx.send("Algo deu errado...")

    # Comando: destrancar

    @commands.command()
    @commands.has_permissions(manage_channels = True)
    async def destrancar(self, ctx):
        # owerwirte é a variável que permite sobrescrever as permissões do canal de um servidor
        # overwirte.send_messages é referente a poder ou a não poder mandar mensagens em um canal
        # ctx.channel.set_permissions é para definir as permissões do canal
        try:
            overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
            overwrite.send_messages = True
            await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
            await ctx.send("Canal destrancado!")
        except Exception as e:
            logging.exception(f"Erro no comando.")
            if ctx.author.id == DEV_ID:
                await ctx.send(f"Erro: {e}")
            else:
                await ctx.send("Algo deu errado...")

    # Comando: silenciar (dessilenciar automático)

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def silenciar(self, ctx, member: discord.Member, tempo: int):
        # member.timeout define a variável do tempo em que o usuário será silenciado
        try:
            await member.timeout(timedelta(minutes=tempo),
            reason="Motivo não especificado")
            await ctx.send(f"{member.mention} foi silenciado por {tempo} minuto(s).")
        except Exception as e:
            logging.exception(f"Erro no comando.")
            if ctx.author.id == DEV_ID:
                await ctx.send(f"Erro: {e}")
            else:
                await ctx.send("Algo deu errado...")

    # Comando: dessilenciar (manual)

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def dessilenciar(self, ctx, member: discord.Member):
        # member.timeout é o tipo de comando para silenciar ou dessilenciar o usuário
        try:
            await member.timeout(None, reason="Dessilenciado manualmente com sucesso!")
            await ctx.send(f"{member.mention} foi dessilenciado manualmente ou automaticamente!")
        except Exception as e:
            logging.exception(f"Erro no comando.")
            if ctx.author.id == DEV_ID:
                await ctx.send(f"Erro: {e}")
            else:
                await ctx.send("Algo deu errado...")

    # Comando: expulsar

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def expulsar(self, ctx, member: discord.Member, *, motivo="Não especificado"):
        # member.kick é um comando específico para expulsão
        try:
            await member.kick(reason=motivo)
            await ctx.send(f"{member.mention} foi expulso do servidor! Motivo: {motivo}")
        except Exception as e:
            logging.exception(f"Erro no comando.")
            if ctx.author.id == DEV_ID:
                await ctx.send(f"Erro: {e}")
            else:
                await ctx.send("Algo deu errado...")

    # Comando: banir

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def banir(self, ctx, member: discord.Member, *, motivo="Não especificado"):
        # member.ban é um comando específico para banimento
        try:
            await member.ban(reason=motivo)
            await ctx.send(f"{member.mention} foi banido do servidor! Motivo: {motivo}")
        except Exception as e:
            logging.exception(f"Erro no comando.")
            if ctx.author.id == DEV_ID:
                await ctx.send(f"Erro: {e}")
            else:
                await ctx.send("Algo deu errado...")

    # Comando: desbanir

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def desbanir(self, ctx, user_id: int):
        # user serve para definir que o banimento deve ser realizado por id de usuário
        # ctx.guild.unban(user) serve para desbanir determinado usuário por id
        try:
            user = await self.bot.fetch_user(user_id)
            await ctx.guild.unban(user)
            await ctx.send(f"O usuário {user.mention} foi desbanido com sucesso!")
        except Exception as e:
            logging.exception(f"Erro no comando.")
            if ctx.author.id == DEV_ID:
                await ctx.send(f"Erro: {e}")
            else:
                await ctx.send("Algo deu errado...")


# Registro de cog

async def setup(bot):
    await bot.add_cog(Admin(bot))