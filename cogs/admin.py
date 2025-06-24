import discord
from discord.ext import commands
import asyncio
from datetime import timedelta
from storage import DEV_ID
import logging
import re
import json
import os

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

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def avisar(self, ctx, member: commands.MemberConverter, *, reason: str):
        try:
            
            warns = carregar_avisos()
            user_id = str(member.id)
            guild_id = str(ctx.guild.id)
            
            if guild_id not in warns:
                warns[guild_id] = {}
            
            if user_id not in warns[guild_id]:
                warns[guild_id][user_id] = []

            # Dicionário/Dict
            warns[guild_id][user_id].append({
                "reason": reason,
                "moderator_id": ctx.author.id
            })
            
            salvar_avisos(warns)
            await ctx.send(f"{ctx.author.mention} Avisou {member.mention}! Motivo: {reason}.")
        
        except Exception as e:
            logging.exception(f"Erro no comando.")
            if ctx.author.id == DEV_ID:
                await ctx.send(f"Erro: {e}")
            else:
                await ctx.send("Algo deu errado...")

    # Comando: desavisar

    @commands.cooldown(1, 5, commands.BucketType.user)
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
                await ctx.send(f"{ctx.author.mention} Desavisou {member.mention}!")
            
            else:
                await ctx.send(f"{member.mention} Não tem avisos registrados neste servidor!")
        
        except Exception as e:
            logging.exception(f"Erro no comando.")
            if ctx.author.id == DEV_ID:
                await ctx.send(f"Erro: {e}")
            else:
                await ctx.send("Algo deu errado...")


    # Comando: avisos

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def avisos(self, ctx, member: commands.MemberConverter = None):
        # self.bot.fetch_user serve para buscar o ID do usuário pela API do discord
        try:
            
            member = member or ctx.author
            user_id = str(member.id)
            guild_id = str(ctx.guild.id)
            
            warns = carregar_avisos()
            warns_guild = warns.get(guild_id, {})
            warns_usuario = warns_guild.get(user_id, [])
            
            if warns_usuario:
                reasons = ""
                for i, warn in enumerate(warns_usuario):
                    
                    if isinstance(warn, str):
                        reason = warn
                        moderator_mention = "Desconhecido"
                    
                    else:
                        reason = warn.get("reason", "Sem motivo")
                        moderator_id = warn.get("moderator_id")
                        moderator_mention = f"<@{moderator_id}>" if moderator_id else "Desconhecido"

                    reasons += f"{i+1}. {reason} — Avisado por: {moderator_mention}\n"
                    
                # Limitar tamanho do reasons para o embed
                
                max_len = 1000
                if len(reasons) > max_len:
                    reasons = reasons[:max_len] + "\n...(texto cortado)..."
                
                member = await self.bot.fetch_user(int(user_id))
                
                embed = discord.Embed(
                    title="Avisos",
                    description=f"{member.mention} - `{member.id}`\n\nPossui **{len(warns_usuario)} aviso(s)**.",
                    color=discord.Color.yellow()
                )
                
                embed.add_field(
                    name="Motivos:",
                    value=f"{reasons}",
                    inline=False
                )

                await ctx.send(embed=embed)

            else:
                await ctx.send(f"{member.mention} Não tem nenhum aviso registrado.")
        
        except Exception as e:
            logging.exception(f"Erro no comando.")
            if ctx.author.id == DEV_ID:
                await ctx.send(f"Erro: {e}")
            else:
                await ctx.send("Algo deu errado...")

    # Comando: listaavisos

    @commands.cooldown(1, 5, commands.BucketType.user)
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
            
            # Limitar tamanho do reasons para o embed
                
            max_len = 1000
            if len(warns_guild) > max_len:
                warns_guild = warns_guild[:max_len] + "\n...(texto cortado)..."

            embed = discord.Embed(
                title="Lista de Avisos",
                color=discord.Color.yellow()
            )
            
            warned = 0

            for user_id, lista in warns_guild.items():
                if not lista:
                    continue  # Ignora se a lista estiver vazia
                
                try:
                    member = await self.bot.fetch_user(int(user_id))
                    warned += 1
                    
                    embed.add_field(
                        name=f"{member} - {member.id} - {len(lista)} aviso(s)",
                        value="",
                        inline=False
                    )
                    warned += 1
                except:
                    continue
            
            if warned == 0:
                await ctx.send("Nenhum usuário tem avisos ativos neste servidor.")
            
            else:
                await ctx.send(embed=embed)
        
        except Exception as e:
            logging.exception(f"Erro no comando.")
            if ctx.author.id == DEV_ID:
                await ctx.send(f"Erro: {e}")
            else:
                await ctx.send("Algo deu errado...")

    # Comando: apagar

    @commands.cooldown(1, 5, commands.BucketType.user)
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

    @commands.cooldown(1, 5, commands.BucketType.user)
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

    @commands.cooldown(1, 5, commands.BucketType.user)
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

    @commands.cooldown(1, 5, commands.BucketType.user)
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

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def silenciar(self, ctx, member: discord.Member, time: int):
        # member.timeout define a variável do tempo em que o usuário será silenciado
        try:
            await member.timeout(timedelta(minutes=time),
            reason="Motivo não especificado")
            await ctx.send(f"{member.mention} foi silenciado por {time} minuto(s).")
        except Exception as e:
            logging.exception(f"Erro no comando.")
            if ctx.author.id == DEV_ID:
                await ctx.send(f"Erro: {e}")
            else:
                await ctx.send("Algo deu errado...")

    # Comando: dessilenciar (manual)

    @commands.cooldown(1, 5, commands.BucketType.user)
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

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def expulsar(self, ctx, member: discord.Member, *, reason="Não especificado"):
        # member.kick é um comando específico para expulsão
        try:
            await member.kick(reason=reason)
            await ctx.send(f"{member.mention} foi expulso do servidor! Motivo: {reason}")
        except Exception as e:
            logging.exception(f"Erro no comando.")
            if ctx.author.id == DEV_ID:
                await ctx.send(f"Erro: {e}")
            else:
                await ctx.send("Algo deu errado...")

    # Comando: banir

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def banir(self, ctx, member: discord.Member, *, reason="Não especificado"):
        # member.ban é um comando específico para banimento
        try:
            await member.ban(reason=reason)
            await ctx.send(f"{member.mention} foi banido do servidor! Motivo: {reason}")
        except Exception as e:
            logging.exception(f"Erro no comando.")
            if ctx.author.id == DEV_ID:
                await ctx.send(f"Erro: {e}")
            else:
                await ctx.send("Algo deu errado...")

    # Comando: desbanir

    @commands.cooldown(1, 5, commands.BucketType.user)
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