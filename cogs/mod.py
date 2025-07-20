import discord
from discord.ext import commands
import asyncio
import logging
import re
import json
import os
from datetime import timedelta
from storage import DEV_ID
from bot import save_log_channels

# JSON

FILE_JSON = "warns.json"

def load_warns():
        if not os.path.exists(FILE_JSON):
            return {}
        with open(FILE_JSON, "r") as j:
            return json.load(j)
    
def save_warns(informations):
        with open(FILE_JSON, "w") as j:
            json.dump(informations, j, indent=4)

# Cog structure (inheritance)

class Mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.regex_links = [
    re.compile(r"https?://\S+"), # Generic link regex
    re.compile(r"\[([^\]]+)\]\((https?://[^\s\)]+)\)"), # More specific link regex
    re.compile(r"(https?:\/\/)?(www\.)?(discord\.gg|discord\.com\/invite)\/[a-zA-Z0-9]+"), # Discord link regex
    re.compile(r"https?://(bit\.ly|tinyurl\.com|t\.co|is\.gd|goo\.gl)/\S+"), # Varied link regex
    re.compile(r"\b(?:www\.)?[a-zA-Z0-9\-]+\.[a-z]{2,}(?:\/\S*)?\b") # False positive regex
]

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return # Ignore bot messages
        # Check link
        for regex in self.regex_links:
            if regex.search(message.content):
                await message.delete()
                break

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if after.author == self.bot.user:
            return  # Ignore edits made by the bot
        for regex in self.regex_links:
            if regex.search(after.content):
                await after.delete()
                break

    # Command: warn

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def warn(self, ctx, member: commands.MemberConverter, *, reason: str):
        
        if ctx.author.id == member.id:
            await ctx.send("Ação reflexiva não permitida!")
            return
        
        try:
            
            warns = load_warns()
            user_id = str(member.id)
            guild_id = str(ctx.guild.id)
            
            if guild_id not in warns:
                warns[guild_id] = {}
            
            if user_id not in warns[guild_id]:
                warns[guild_id][user_id] = []

            # Dict

            warns[guild_id][user_id].append({
                "reason": reason,
                "moderator_id": ctx.author.id
            })
            
            save_warns(warns)
            await ctx.send(f"{ctx.author.mention} Avisou {member.mention}! Motivo: {reason}.")
        
        except Exception as e:
            logging.exception(f"Erro no comando.")
            if ctx.author.id == DEV_ID:
                await ctx.send(f"Erro: {e}")
            else:
                await ctx.send("Algo deu errado...")

    # Command: unwarn

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def unwarn(self, ctx, member: commands.MemberConverter):
        
        if ctx.author.id == member.id:
            await ctx.send("Ação reflexiva não permitida!")
            return

        try:
            
            warns = load_warns()
            user_id = str(member.id)
            guild_id = str(ctx.guild.id)
            
            if guild_id in warns and user_id in warns[guild_id]:
                del warns[guild_id][user_id]
                
                if not warns[guild_id]:
                    del warns[guild_id]
                    
                save_warns(warns)
                await ctx.send(f"{ctx.author.mention} Desavisou {member.mention}!")
            
            else:
                await ctx.send(f"{member.mention} Não tem avisos registrados neste servidor!")
        
        except Exception as e:
            logging.exception(f"Erro no comando.")
            if ctx.author.id == DEV_ID:
                await ctx.send(f"Erro: {e}")
            else:
                await ctx.send("Algo deu errado...")


    # Command: warnings

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def warnings(self, ctx, member: commands.MemberConverter = None):
        # self.bot.fetch_user is used to fetch the user ID via the discord API

        try:
            
            member = member or ctx.author
            user_id = str(member.id)
            guild_id = str(ctx.guild.id)
            
            warns = load_warns()
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

    # Command: warninglist

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def warninglist(self, ctx):
        
        try:
            
            guild_id = str(ctx.guild.id)
            warns = load_warns()
            warns_guild = warns.get(guild_id, {})
            
            if not warns_guild:
                await ctx.send("Nenhum usuário foi avisado neste servidor.")
                return
            
            # Limit reasons size for embed
                
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
                    continue  # Ignore if the list is empty
                
                try:
                    member = await self.bot.fetch_user(int(user_id))
                    
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

    # Commmand: clear

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, quantity_messages: int):
        # ctx.channel.purge is used to delete the number of messages defined in the command
        # limit is used to set a limit on the number of messages deleted
        # delete_after=5 is the number of seconds it will take for the bot to delete the messages
        try:
            await ctx.channel.purge(limit=quantity_messages)
            await ctx.send(f"Foram apagadas {quantity_messages} mensagens.", delete_after=5)
        except Exception as e:
            logging.exception(f"Erro no comando.")
            if ctx.author.id == DEV_ID:
                await ctx.send(f"Erro: {e}")
            else:
                await ctx.send("Algo deu errado...")

    # Command: purge

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, member: discord.Member, quantity_messages: int):
        # ctx.channel.purge is used to delete the number of messages from a user in the channel, as defined in the command.
        # limit is used to set a limit on the number of messages deleted.
        # delete_after=5 is the number of seconds it will take for the bot to delete the messages.
        try:
            deleted = await ctx.channel.purge(
                limit=999, # 999 messages
                check=lambda msg: msg.author == member,
                before=ctx.message  # Ignore the command itself
            )
            
            deleted = deleted[:quantity_messages]

            await ctx.send(f"Foram apagadas {len(deleted)} mensagens de {member.mention}.", delete_after=5)
        except Exception as e:
            logging.exception(f"Erro no comando.")
            if ctx.author.id == DEV_ID:
                await ctx.send(f"Erro: {e}")
            else:
                await ctx.send("Algo deu errado...")

    # Command: slow

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def slow(self, ctx, time: int):
        # ctx.channel.edit is used to edit channel settings
        # slowmode_delay is used to specify the type of editing that will be performed on the server
        try:
            await ctx.channel.edit(slowmode_delay=time)
            await ctx.send(f"O modo lento foi definido para {time} segundos")
        except Exception as e:
            logging.exception(f"Erro no comando.")
            if ctx.author.id == DEV_ID:
                await ctx.send(f"Erro: {e}")
            else:
                await ctx.send("Algo deu errado...")

    # Commmand: lock

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def lock(self, ctx):
        # overwirte is the variable that allows you to override a server's channel permissions.
        # overwirte.send_messages refers to whether or not you can send messages on a given channel.
        # ctx.channel.set_permissions is for setting channel permissions.
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

    # Comando: unlock

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx):
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

    # Command: lockdown

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def lockdown(self, ctx):
        # overwrite is the variable that allows you to override a server's channel permissions.
        # overwrite.send_messages refers to whether or not messages can be sent on a given channel.
        # ctx.channel.set_permissions is for setting channel permissions.
        try:
            locked_channels = 0

            for channel in ctx.guild.text_channels:
                overwrite = channel.overwrites_for(ctx.guild.default_role)
                if overwrite.send_messages is not False:
                    overwrite.send_messages = False
                    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
                    locked_channels += 1

            await ctx.send(f"Lockdown ativado!")
        except Exception as e:
            logging.exception(f"Erro no comando.")
            if ctx.author.id == DEV_ID:
                await ctx.send(f"Erro: {e}")
            else:
                await ctx.send("Algo deu errado...")

    # Command: unlockdown

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unlockdown(self, ctx):
        # overwrite is the variable that allows you to override a server's channel permissions.
        # overwrite.send_messages refers to whether or not messages can be sent on a given channel.
        # ctx.channel.set_permissions is for setting channel permissions.
        try:
            locked_channels = 0

            for channel in ctx.guild.text_channels:
                overwrite = channel.overwrites_for(ctx.guild.default_role)
                if overwrite.send_messages is not True:
                    overwrite.send_messages = True
                    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
                    locked_channels += 1

            await ctx.send(f"Lockdown desativado!")
        except Exception as e:
            logging.exception(f"Erro no comando.")
            if ctx.author.id == DEV_ID:
                await ctx.send(f"Erro: {e}")
            else:
                await ctx.send("Algo deu errado...")

    # Command: mute

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member, time: int):
        # member.timeout sets the time variable in which the user will be muted
        if ctx.author.id == member.id:
            await ctx.send("Ação reflexiva não permitida!")
            return
        try:
            await member.timeout(timedelta(minutes=time),
            reason="Motivo não especificado")
            await ctx.send(f"O membro {member.mention} foi silenciado por {time} minuto(s).")
        except Exception as e:
            logging.exception(f"Erro no comando.")
            if ctx.author.id == DEV_ID:
                await ctx.send(f"Erro: {e}")
            else:
                await ctx.send("Algo deu errado...")

    # Command: unmute

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member):
        # member.timeout is the type of command to mute or unmute the user
        try:
            await member.timeout(None, reason="Dessilenciado manualmente com sucesso!")
            await ctx.send(f"O membro {member.mention} foi dessilenciado manualmente ou automaticamente!")
        except Exception as e:
            logging.exception(f"Erro no comando.")
            if ctx.author.id == DEV_ID:
                await ctx.send(f"Erro: {e}")
            else:
                await ctx.send("Algo deu errado...")

    # Command: kick

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason="Não especificado"):
        # member.kick is a specific command for kicking
        if ctx.author.id == member.id:
            await ctx.send("Ação reflexiva não permitida!")
            return
        try:
            await member.kick(reason=reason)
            await ctx.send(f"O membro {member.mention} foi expulso do servidor! Motivo: {reason}")
        except Exception as e:
            logging.exception(f"Erro no comando.")
            if ctx.author.id == DEV_ID:
                await ctx.send(f"Erro: {e}")
            else:
                await ctx.send("Algo deu errado...")

    # Command: ban

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason="Não especificado"):
        # member.ban is a specific command for banning
        if ctx.author.id == member.id:
            await ctx.send("Ação reflexiva não permitida!")
            return
        try:
            await member.ban(reason=reason)
            await ctx.send(f"O membro {member.mention} foi banido do servidor! Motivo: {reason}.")
        except Exception as e:
            logging.exception(f"Erro no comando.")
            if ctx.author.id == DEV_ID:
                await ctx.send(f"Erro: {e}")
            else:
                await ctx.send("Algo deu errado...")

    # Command: unban

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user_id: int):
        # user is used to define whether the ban should be carried out by user ID
        # ctx.guild.unban(user) is used to unban a specific user by ID
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

    # Command: tempban

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def tempban(self, ctx, member: discord.Member, duration: int, *, reason="Não especificado"):
        if ctx.author.id == member.id:
            await ctx.send("Ação reflexiva não permitida!")
            return
        try:
            await member.ban(reason=reason)
            await ctx.send(f"{member.mention} Foi banido por {duration} minuto(s). Motivo: {reason}.")

            # Time

            await asyncio.sleep(duration * 60)

            # Automatic Unban

            await ctx.guild.unban(discord.Object(id=member.id))
            await ctx.send(f"{member.mention} Foi desbanido automaticamente após {duration} minuto(s)!")
        except Exception as e:
            logging.exception(f"Erro no comando.")
            if ctx.author.id == DEV_ID:
                await ctx.send(f"Erro: {e}")
            else:
                await ctx.send("Algo deu errado...")

    # Command: softban

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def softban(self, ctx, member: discord.Member, reason="Não especificado"):
        if ctx.author.id == member.id:
            await ctx.send("Ação reflexiva não permitida!")
            return
        try:
            await member.ban(reason=reason)
            await ctx.send(f"{member.mention} Foi banido para limpeza de mensagens. Motivo: {reason}.")

            # Time

            await asyncio.sleep(1)

            # Automatic Unban

            await ctx.guild.unban(discord.Object(id=member.id))
            await ctx.send(f"{member.mention} Foi desbanido automaticamente após 1 segundo!")
        except Exception as e:
            logging.exception(f"Erro no comando.")
            if ctx.author.id == DEV_ID:
                await ctx.send(f"Erro: {e}")
            else:
                await ctx.send("Algo deu errado...")

    # Command: setlog

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    @commands.has_permissions(manage_channels = True)
    async def setlog(self, ctx, channel: discord.TextChannel):
        try:
            self.bot.log_channels[ctx.guild.id] = channel.id
            save_log_channels(self.bot.log_channels)
            await ctx.send(f"Canal de logs configurado: {channel.mention}.")
        except Exception as e:
            logging.exception(f"Erro no comando.")
            if ctx.author.id == DEV_ID:
                await ctx.send(f"Erro: {e}")
            else:
                await ctx.send("Algo deu errado...")

# Cog registration

async def setup(bot):
    await bot.add_cog(Mod(bot))