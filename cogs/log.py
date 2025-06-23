import discord
from discord.ext import commands
import asyncio
from datetime import timedelta
import typing

# Estrutura cog (herança)

class Log(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # 1. Mensagens

    # Message_edit

    @commands.Cog.listener()
    async def on_message_edit(self, message_before, message_after):
        if not message_before.guild:
            return
        
        if message_before.content == message_after.content:
            return  # ignora edição nula
        
        log_channel = discord.utils.get(message_before.guild.text_channels, name='log')
        
        if not log_channel:
            return
        
        time = message_before.created_at.strftime('%d/%m/%Y %H:%M:%S')

        await log_channel.send(
        f"Mensagem editada em {message_before.channel.mention}\n"
        f"Autor: {message_before.author.mention}\n"
        f"Horário: {time}\n"
        f"Antes: {message_before.content}\n"
        f"Depois: {message_after.content}"
        )

    # Message_delete 

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if not message.guild:
            return

        log_channel = discord.utils.get(message.guild.text_channels, name='log')
        
        if not log_channel:
            return
        
        author = message.author.mention if message.author else "Autor desconhecido"
        content = message.content or "*Sem conteúdo textual (pode ter sido um anexo, embed ou imagem)*"
        time = message.created_at.strftime('%d/%m/%Y %H:%M:%S') 
 
        await log_channel.send(
        f"Mensagem deletada em {message.channel.mention}\n"
        f"Autor: {author}\n"
        f"Conteúdo: {content}\n"
        f"Horário: {time}"
        )

    # Bulk_message_delete

    @commands.Cog.listener()
    async def on_bulk_message_delete(self, messages):

        guild = messages[0].guild
        log_channel = discord.utils.get(guild.text_channels, name='log')

        if not log_channel:
            return
        
        messages = sorted(messages, key=lambda m: m.created_at) # Ordem de horário de envio

        content_log = ""
        for msg in messages:
            author = msg.author if msg.author else "Autor desconhecido"
            content = msg.content or "[Sem conteúdo]"
            content_log += f"`{msg.created_at.strftime('%H:%M:%S')}` {author.mention}: {content}\n"
            
        if len(content_log) > 1900:
            content_log = content_log[:1900] + "\n... (log cortado)" # Limite de caracteres do discord: 2000

        await log_channel.send(
        f"{len(messages)} Mensagens deletadas em massa em {messages[0].channel.mention}:\n{content_log}"
        )

    # 2. Membros

    # Member_join

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        
        log_channel = discord.utils.get(member.guild.text_channels, name='log')
        
        if not log_channel:
            return

        await log_channel.send(
        f"{member.mention} Entrou no servidor!\n"
        f"ID: `{member.id}`"
        )

    # Member_remove

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        
        log_channel = discord.utils.get(member.guild.text_channels, name='log')
        
        if not log_channel:
            return

        async for entry in member.guild.audit_logs(limit=1, action=discord.AuditLogAction.ban):
            if entry.target.id == member.id:
                continue  # Ignora
            
        await log_channel.send(
        f"{member.mention} Saiu ou foi expulso do servidor!\n"
        f"ID: `{member.id}`"
        )

    # Member_ban
            
    @commands.Cog.listener()
    async def on_member_ban(self, guild: discord.Guild, user: discord.User):
        
        log_channel = discord.utils.get(guild.text_channels, name='log')
        
        if not log_channel:
            return
        
        await log_channel.send(
        f"{user.mention} Foi banido do servidor!\n"
        f"ID: `{user.id}`"
        )
            
    # Member_unban
           
    @commands.Cog.listener()
    async def on_member_unban(self, guild: discord.Guild, user: discord.User):
        
        log_channel = discord.utils.get(guild.text_channels, name='log')
        
        if not log_channel:
            return
            
        await log_channel.send(
        f"{user.mention} Foi desbanido do servidor!\n"
        f"ID: `{user.id}`"
        )

    # Member_update

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        
        log_channel = discord.utils.get(after.guild.text_channels, name='log')
        
        if not log_channel:
            return
        
        # Apelido

        if before.display_name != after.display_name:
            await log_channel.send(
            f"{before.mention} Mudou o nickname!\n"
            f"De: `{before.display_name}`\n"
            f"Para: `{after.display_name}`"
            f"ID: `{after.id}`"
            )

        # Cargo

        if before.roles != after.roles:
            added_roles = [role for role in after.roles if role not in before.roles]
            removed_roles = [role for role in before.roles if role not in after.roles]
            
            changes = ""
            if added_roles:
                changes += f"Cargos adicionados: {', '.join(role.mention for role in added_roles)}\n"
            if removed_roles:
                changes += f"Cargos removidos: {', '.join(role.mention for role in removed_roles)}\n"

            if changes:
                await log_channel.send(
                f"{before.mention} Teve alterações no cargo!\n{changes}"
                f"ID: `{after.id}`"
                )
            
    # 3. Cargos e permissões

    # User_update

    @commands.Cog.listener()
    async def on_user_update(self, before: discord.User, after: discord.User):
        for guild in self.bot.guilds:
            
            member = guild.get_member(after.id)
            if not member:
                continue # Ignora
            
            log_channel = discord.utils.get(guild.text_channels, name='log')
            
            if not log_channel:
                continue

            # Nome (global)

            if before.name != after.name:
                await log_channel.send(
                f"O membro `{before}` Alterou o nome de `{before.name}` para `{after.name}`!\n"
                f"ID: `{after.id}`"
                )

            # Avatar (global)

            if before.avatar != after.avatar:
                await log_channel.send(
                f"O membro `{before}` alterou o avatar!\n"
                f"ID: `{after.id}`"
                )

    # Role_create

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        
        log_channel = discord.utils.get(role.guild.text_channels, name='log')
        
        if not log_channel:
            return
        
        await log_channel.send(
        f"O cargo `{role.name}` foi criado!\n"
        f"ID: `{role.id}`"
        )

    # Role_delete 

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        
        log_channel = discord.utils.get(role.guild.text_channels, name='log')
        
        if not log_channel:
            return
        
        await log_channel.send(
        f"O cargo `{role.name}` foi deletado!\n"
        f"ID: `{role.id}`"
        )

    # Role_update

    @commands.Cog.listener()
    async def on_guild_role_update(self, before: discord.Role, after: discord.Role):
        if before.name != after.name:
            
            log_channel = discord.utils.get(before.guild.text_channels, name='log')
            
            if not log_channel:
                return
            
            changes = []
            
            # Nome

            if before.name != after.name:
                changes.append(f"De nome `{before.name}` para `{after.name}`")

            # Cor

            if before.color != after.color:
                changes.append(f"De cor `{before.color}` para `{after.color}`")
                
            # Permissões

            if before.permissions != after.permissions:
                changes.append(f"Permissões foram alteradas!")
                
            if changes:
                await log_channel.send(
                f"O cargo `{before.name}` foi atualizado:\n" + 
                "\n".join(changes) +
                f"\nID: `{after.id}`"
                )
    
    # 4. Canais

    # Channel_create 

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        
        log_channel = discord.utils.get(channel.guild.text_channels, name='log')
        
        if not log_channel:
            return
        
        await log_channel.send(
        f"O canal `{channel.name}` foi criado!\n"
        f"ID: `{channel.id}`"
        )

    # Channel_delete

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        
        log_channel = discord.utils.get(channel.guild.text_channels, name='log')
        
        if not log_channel:
            return

        await log_channel.send(
        f"O canal `{channel.name}` foi deletado!\n"
        f"ID: `{channel.id}`"
        )

    # Channel_update
    
    @commands.Cog.listener()
    async def on_guild_channel_update(self, before: discord.abc.GuildChannel, after: discord.abc.GuildChannel):
        
        log_channel = discord.utils.get(before.guild.text_channels, name='log')
        
        if not log_channel:
            return
            
        await log_channel.send(
        f"O nome do canal `{before.name}` foi atualizado para `{after.name}`!\n"
        f"ID: `{after.id}`"
        )

    # 5. Voz

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        log_channel = discord.utils.get(member.guild.text_channels, name='log')
        
        if not log_channel:
            return
        
        # Entrou em um canal

        if before.channel is None and after.channel is not None:
            await log_channel.send(
            f"{member.mention} entrou no canal de voz `{after.channel.name}`"
            )

        # Saiu de um canal

        elif before.channel is not None and after.channel is None:
            await log_channel.send(
            f"{member.mention} saiu do canal de voz `{before.channel.name}`"
        )
            
        # Mudou de canal
        
        elif before.channel != after.channel:
            await log_channel.send(
            f"{member.mention} mudou do canal de voz `{before.channel.name}` para `{after.channel.name}`"
            )

    # 6. Guild

    # Guild_update

    @commands.Cog.listener()
    async def on_guild_update(self, before: discord.Guild, after: discord.Guild):
        
        log_channel = discord.utils.get(after.text_channels, name='log')
        
        if not log_channel:
            return
        
        await log_channel.send(
        f"O nome do servidor foi alterado!\n"
        f"De: `{before.name}`\n"
        f"Para: `{after.name}`\n"
        f"ID: `{after.id}`"
        )

    # Guild_join

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        
        log_channel = self.bot.get_channel(1386112547148529695) # ID de um canal de logs do servidor central
        
        if not log_channel:
            return
        
        await log_channel.send(
        f"O bot {self.bot.user.name} entrou no servidor!\n"
        f"Nome: {guild.name}\n"
        f"ID: {guild.id}"
        )
            
    # Guild_remove
    
    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        
        log_channel = self.bot.get_channel(1386112547148529695) # ID de um canal de logs do servidor central
        
        if log_channel:
            
            await log_channel.send(
            f"O bot {self.bot.user.name} foi removido!\n"
            f"Nome: {guild.name}\n"
            f"ID: {guild.id}"
            )

# Registro de cog

async def setup(bot):
    await bot.add_cog(Log(bot))