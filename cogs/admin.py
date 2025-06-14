import discord
from discord.ext import commands
import asyncio
from datetime import timedelta
import re
import json
import os

# --Comandos de moderação: !avisar, !desavisar, !veravisos, !listaavisos, !apagar, !lento, !trancar, !destrancar, !silenciar, !dessilenciar, !expulsar, !banir, !desbanir

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
    re.compile(r"https?://\S+"),
    re.compile(r"\[([^\]]+)\]\((https?://[^\s\)]+)\)"),
    re.compile(r"(https?:\/\/)?(www\.)?(discord\.gg|discord\.com\/invite)\/[a-zA-Z0-9]+"),
    re.compile(r"https?://(bit\.ly|tinyurl\.com|t\.co|is\.gd|goo\.gl)/\S+"),
    re.compile(r"\b(?:www\.)?[a-zA-Z0-9\-]+\.[a-z]{2,}(?:\/\S*)?\b")
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

    # Comando: !avisar

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def avisar(self, ctx, member: discord.Member, *, motivo: str):
        try:
            avisos = carregar_avisos()
            user_id = str(member.id)
            if user_id not in avisos:
                avisos[user_id] = []
            avisos[user_id].append(motivo)
            salvar_avisos(avisos)
            await ctx.send(f"{member.mention} foi avisado por: {motivo}")
        except Exception as e:
            await ctx.send(f"Erro ao avisar o usuário! Erro: {e}")

    # Comando: !desavisar

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def desavisar(self, ctx, member: discord.Member):
        try:
            avisos = carregar_avisos()
            user_id = str(member.id)
            if user_id in avisos:
                del avisos[user_id]
            else:
                await ctx.send(f"{member.mention} não tem avisos registrados!")
                return
            salvar_avisos(avisos)
            await ctx.send(f"{member.mention} foi desavisado!")
        except Exception as e:
            await ctx.send(f"Erro ao desavisar o usuário! Erro: {e}")

    # Comando: !veravisos

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def veravisos(self, ctx, member: discord.Member = None):
        # self.bot.fetch_user serve para buscar o ID do usuário pela API do discord
        # motivos é uma variável que enumera os motivos dos avisos em determinado usuário
        try:
            membro = member or ctx.author
            user_id = str(membro.id)
            avisos = carregar_avisos().get(user_id, [])
            if avisos:
                mensagem = "**Avisos:**\n\n"
                motivos = "\n".join(f"{i+1}. {m}" for i, m in enumerate(avisos))
                membro = await self.bot.fetch_user(int(user_id))
                mensagem += f"{membro.mention} - {membro} - {membro.id} - {len(avisos)} aviso(s):```{motivos}```"
                await ctx.send(mensagem[:2000]) # Limite de caracteres
            else:
                await ctx.send(f"{membro.mention} não tem nenhum aviso registrado.")
        except Exception as e:
            await ctx.send(f"Erro ao ver os avisos! Erro: {e}")

    # Comando: !listaavisos

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def listaavisos(self, ctx):
        # self.bot.fetch_user serve para buscar o ID de um usuário pela API do discord
        # for serve para "organizar" a lista de avisadas
        try:
            avisos = carregar_avisos()
            if not avisos:
                await ctx.send("Nenhum usuário foi avisado ainda")
                return
            mensagem = "**Lista de usuários avisados:**\n\n"
            for user_id, qtd in avisos.items():
                membro = await self.bot.fetch_user(int(user_id))
                mensagem += f"```{membro.name} - {membro} — {membro.id} - aviso(s): {len(qtd)}```"
            await ctx.send(mensagem[:2000]) # Limite de caracteres
        except Exception as e:
            await ctx.send(f"Erro ao ver a lista de avisos! Erro: {e}")

    # Comando: !apagar

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
            await ctx.send(f"Não foi possível apagar as mensagens! Erro: {e}")

    # Comando: !lento

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def lento(self, ctx, tempo: int):
        # ctx.channel.edit serve editar as configurações do canal
        # slowmode_delay é para especificar o tipo de edição que será realizado no servidor
        try:
            await ctx.channel.edit(slowmode_delay=tempo)
            await ctx.send(f"O modo lento foi definido para {tempo} segundos")
        except Exception as e:
            await ctx.send(f"Não foi possível definir um tempo de lentidão no canal! Erro: {e}")

    # Comando: !trancar

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
            await ctx.send(f"Não foi possível trancar o canal! Erro: {e}")

    # Comando: !destrancar

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
            await ctx.send(f"Não foi possível destrancar o canal! Erro: {e}")

    # Comando: !silenciar (dessilenciar automático)

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def silenciar(self, ctx, member: discord.Member, tempo: int):
        # member.timeout define a variável do tempo em que o usuário será silenciado
        try:
            await member.timeout(timedelta(minutes=tempo),
            reason="Motivo não especificado")
            await ctx.send(f"{member.mention} foi silenciado por {tempo} minuto(s).")
        except Exception as e:
            await ctx.send(f"Não foi possível silenciar o usuário! Erro: {e}")

    # Comando: !dessilenciar (manual)

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def dessilenciar(self, ctx, member: discord.Member):
        # member.timeout é o tipo de comando para silenciar ou dessilenciar o usuário
        try:
            await member.timeout(None, reason="Dessilenciado manualmente com sucesso!")
            await ctx.send(f"{member.mention} foi dessilenciado manualmente ou automaticamente!")
        except Exception as e:
            await ctx.send(f"Não foi possível dessilenciar o membro! Erro: {e}")

    # Comando: !expulsar

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def expulsar(self, ctx, member: discord.Member, *, motivo="Não especificado"):
        # member.kick é um comando específico para expulsão
        try:
            await member.kick(reason=motivo)
            await ctx.send(f"{member.mention} foi expulso do servidor! Motivo: {motivo}")
        except Exception as e:
            await ctx.send(f"Não foi possível expulsar determinado membro! Erro: {e}")

    # Comando: !banir

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def banir(self, ctx, member: discord.Member, *, motivo="Não especificado"):
        # member.ban é um comando específico para banimento
        try:
            await member.ban(reason=motivo)
            await ctx.send(f"{member.mention} foi banido do servidor! Motivo: {motivo}")
        except Exception as e:
            await ctx.send(f"Não foi possível banir determinado membro! Erro: {e}")

    # Comando: !desbanir

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
            await ctx.send(f"Não foi possível desbanir o usuário com ID {user_id}. Erro: {e}")

# Registro de cog

async def setup(bot):
    await bot.add_cog(Admin(bot))