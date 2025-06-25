import discord
from discord.ext import commands
import asyncio
from datetime import timedelta

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
        
        guild = message_before.guild
        channel_id = self.bot.log_channels.get(guild.id)
        
        if channel_id:
            log_channel = guild.get_channel(channel_id)
        else:
            log_channel = None
        
        if not log_channel:
            return
        
        author = message_before.author
        icon_url = author.avatar.url if author and author.avatar else None

        embed = discord.Embed(
            title="Mensagem Editada",
            description=f"Mensagem editada em {message_before.channel.mention}",
            color=discord.Color.yellow(),
            timestamp=message_after.edited_at or discord.utils.utcnow()
        )

        embed.set_author(name=str(message_before.author), icon_url=icon_url)
        embed.add_field(name="Antes", value=message_before.content or "*Mensagem vazia*", inline=False)
        embed.add_field(name="Depois", value=message_after.content or "*Mensagem vazia*", inline=False)
        embed.set_footer(text=f"ID do membro: {message_before.author.id}")

        await log_channel.send(embed=embed)

    # Message_delete

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        
        if not message.guild:
            return

        guild = message.guild
        channel_id = self.bot.log_channels.get(guild.id)
        
        if channel_id:
            log_channel = guild.get_channel(channel_id)
        else:
            log_channel = None
        
        if not log_channel:
            return
        
        author = message.author
        icon_url = author.avatar.url if author and author.avatar else None

        embed = discord.Embed(
            title="Mensagem Deletada",
            description=f"Mensagem deletada em {message.channel.mention}",
            color=discord.Color.orange(),
            timestamp=discord.utils.utcnow()
        )

        embed.set_author(name=str(message.author), icon_url=icon_url)
        embed.add_field(name="Conteúdo:", value=message.content or "*Mensagem vazia*", inline=False)
        embed.set_footer(text=f"ID do membro: {message.author.id}")
       
        await log_channel.send(embed=embed)

    # Bulk_message_delete

    @commands.Cog.listener()
    async def on_bulk_message_delete(self, messages):

        if not messages:
            return

        guild = messages[0].guild
        channel_id = self.bot.log_channels.get(guild.id)
        
        if channel_id:
            log_channel = guild.get_channel(channel_id)
        else:
            log_channel = None

        if not log_channel:
            return
        
        messages = sorted(messages, key=lambda m: m.created_at) # Ordem de horário de envio

        content_log = ""
        for msg in messages:
            author = getattr(msg, 'author', None)
            mention = author.mention if author else "Autor desconhecido"
            content = msg.content or "[Sem conteúdo]"
            timestamp = msg.created_at.strftime('%H:%M:%S')
            content_log += f"`{timestamp}` {mention}: {content}\n"
            
        if len(content_log) > 1900:
            content_log = content_log[:1900] + "\n... (log cortado)" # Limite de caracteres do discord: 2000

        reference_author = getattr(messages[0], 'author', None)
        reference_name = str(reference_author) if reference_author else "Autor desconhecido"
        icon_url = reference_author.avatar.url if reference_author and reference_author.avatar else None
        reference_id = reference_author.id if reference_author else "Desconhecido"
        
        embed = discord.Embed(
            title="Mensagens Deletadas",
            description=f"{len(messages)} Mensagens deletadas em {messages[0].channel.mention}",
            color=discord.Color.red(),
            timestamp=discord.utils.utcnow()
        )

        embed.set_author(name=reference_name, icon_url=icon_url)
        embed.add_field(name="Conteúdo", value=content_log or "*Mensagem vazia*", inline=False)
        embed.set_footer(text=f"ID de referência: {reference_id}")
       
        await log_channel.send(embed=embed)

    # 2. Membros

    # Member_join

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):

        guild = member.guild
        if not guild:
            return
        
        channel_id = self.bot.log_channels.get(guild.id)
            
        if channel_id:
            log_channel = guild.get_channel(channel_id)
        else:
            log_channel = None
        
        if not log_channel:
            return
        
        icon_url = member.avatar.url if member and member.avatar else None
        
        embed = discord.Embed(
            title="Membro Entrou",
            description=f"Membro: {member.mention}",
            color=discord.Color.blue(),
            timestamp=discord.utils.utcnow()
        )

        embed.set_author(name=str(member.mention), icon_url=icon_url)
        embed.set_footer(text=f"ID do membro: {member.id}")
       
        await log_channel.send(embed=embed)

    # Member_remove

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):

        guild = member.guild
        if not guild:
            return
        
        channel_id = self.bot.log_channels.get(guild.id)
            
        if channel_id:
            log_channel = guild.get_channel(channel_id)
        else:
            log_channel = None
        
        if not log_channel:
            return

        async for entry in member.guild.audit_logs(limit=1, action=discord.AuditLogAction.ban):
            if entry.target.id == member.id:
                continue  # Ignora

        icon_url = member.avatar.url if member and member.avatar else None

        embed = discord.Embed(
            title="Membro Saiu",
            description=f"Membro: {member.mention}",
            color=discord.Color.orange(),
            timestamp=discord.utils.utcnow()
        )

        embed.set_author(name=str(member.mention), icon_url=icon_url)
        embed.set_footer(text=f"ID do membro: {member.id}")
       
        await log_channel.send(embed=embed)

    # Member_ban
            
    @commands.Cog.listener()
    async def on_member_ban(self, guild: discord.Guild, user: discord.User):
        
        channel_id = self.bot.log_channels.get(guild.id)
            
        if channel_id:
            log_channel = guild.get_channel(channel_id)
        else:
            log_channel = None
        
        if not log_channel:
            return
        
        icon_url = user.avatar.url if user and user.avatar else None
        
        embed = discord.Embed(
            title="Membro Banido",
            description=f"Membro: {user.mention}",
            color=discord.Color.red(),
            timestamp=discord.utils.utcnow()
        )

        embed.set_author(name=str(user.mention), icon_url=icon_url)
        embed.set_footer(text=f"ID do membro: {user.id}")
       
        await log_channel.send(embed=embed)
            
    # Member_unban
           
    @commands.Cog.listener()
    async def on_member_unban(self, guild: discord.Guild, user: discord.User):
     
        channel_id = self.bot.log_channels.get(guild.id)
            
        if channel_id:
            log_channel = guild.get_channel(channel_id)
        else:
            log_channel = None
        
        if not log_channel:
            return
        
        icon_url = user.avatar.url if user and user.avatar else None
        
        embed = discord.Embed(
            title="Membro Desbanido",
            description=f"Membro: {user.mention}",
            color=discord.Color.green(),
            timestamp=discord.utils.utcnow()
        )

        embed.set_author(name=str(user.mention), icon_url=icon_url)
        embed.set_footer(text=f"ID do membro: {user.id}")
       
        await log_channel.send(embed=embed)

    # Member_update

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
                
        channel_id = self.bot.log_channels.get(after.guild.id)
            
        if channel_id:
            log_channel = after.guild.get_channel(channel_id)
        else:
            log_channel = None
        
        if not log_channel:
            return
        
        # Apelido

        if before.display_name != after.display_name:

            embed = discord.Embed(
                title="Membro (Apelido)",
                description=f"Membro: {before.mention}",
                color=discord.Color.yellow(),
                timestamp=discord.utils.utcnow()
            )
            
            embed.add_field(name="Antes", value=before.display_name, inline=False)
            embed.add_field(name="Depois", value=after.display_name, inline=False)
            embed.set_footer(text=f"ID do membro: {after.id}")
            
            await log_channel.send(embed=embed)

        # Cargo

        if before.roles != after.roles:
            
            added_roles = [role for role in after.roles if role not in before.roles]
            removed_roles = [role for role in before.roles if role not in after.roles]

            if added_roles:
                
                embed = discord.Embed(
                    title="Membro (Adição de Cargo)",
                    description=f"Membro: {before.mention}",
                    color=discord.Color.orange(),
                    timestamp=discord.utils.utcnow()
                )
                
                embed.add_field(name="Cargo", value=', '.join(role.mention for role in added_roles), inline=False)
                embed.set_footer(text=f"ID do membro: {after.id}")
                await log_channel.send(embed=embed)

            if removed_roles:
                
                embed = discord.Embed(
                    title="Membro (Remoção de Cargo)",
                    description=f"Membro: {before.mention}",
                    color=discord.Color.red(),
                    timestamp=discord.utils.utcnow()
                )
                
                embed.add_field(name="Cargo", value=', '.join(role.mention for role in removed_roles), inline=False)
                embed.set_footer(text=f"ID do membro: {after.id}")
                await log_channel.send(embed=embed)
            
    # 3. Cargos e permissões

    # User_update

    @commands.Cog.listener()
    async def on_user_update(self, before: discord.User, after: discord.User):
        
        for guild in self.bot.guilds:
            
            member = guild.get_member(after.id)
            if not member:
                continue # Ignora
                
            channel_id = self.bot.log_channels.get(guild.id)
            
            if channel_id:
                log_channel = guild.get_channel(channel_id)
            else:
                log_channel = None
            
            if not log_channel:
                continue

            # Nome (global)

            if before.name != after.name:

                embed = discord.Embed(
                    title="Membro (Nome)",
                    description=f"Membro: {before.mention}",
                    color=discord.Color.yellow(),
                    timestamp=discord.utils.utcnow()
                )
                
                embed.add_field(name="Antes", value=before.name, inline=False)
                embed.add_field(name="Depois", value=after.name, inline=False)
                embed.set_footer(text=f"ID do membro: {after.id}")
                
                await log_channel.send(embed=embed)

            # Avatar (global)

            if before.avatar != after.avatar:

                embed = discord.Embed(
                    title="Membro (Avatar)",
                    description=(
                        f"Membro: {before.mention}\n\n"
                        f"[Avatar Anterior]({before.avatar.url})\n"
                        f"[Avatar Atual]({after.avatar.url})"
                    ),
                    color=discord.Color.yellow(),
                    timestamp=discord.utils.utcnow()
                )
                
                embed.set_footer(text=f"ID do membro: {after.id}")
               
                await log_channel.send(embed=embed)

    # Role_create

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        
        guild = role.guild
        if not guild:
            return
        
        channel_id = self.bot.log_channels.get(guild.id)
        
        if channel_id:
            log_channel = guild.get_channel(channel_id)
        else:
            log_channel = None
        
        if not log_channel:
            return
        
        embed = discord.Embed(
            title="Cargo Criado",
            description=f"Cargo: {role.name}",
            color=discord.Color.green(),
            timestamp=discord.utils.utcnow()
        )

        embed.set_footer(text=f"ID do cargo: {role.id}")
       
        await log_channel.send(embed=embed)

    # Role_delete 

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):

        guild = role.guild
        if not guild:
            return
        
        channel_id = self.bot.log_channels.get(guild.id)
        
        if channel_id:
            log_channel = guild.get_channel(channel_id)
        else:
            log_channel = None
        
        if not log_channel:
            return
        
        embed = discord.Embed(
            title="Cargo Deletado",
            description=f"Cargo: {role.name}",
            color=discord.Color.red(),
            timestamp=discord.utils.utcnow()
        )

        embed.set_footer(text=f"ID do cargo: {role.id}")
       
        await log_channel.send(embed=embed)

    # Role_update

    @commands.Cog.listener()
    async def on_guild_role_update(self, before: discord.Role, after: discord.Role):
        
        guild = after.guild
        if not guild:
            return

        channel_id = self.bot.log_channels.get(guild.id)
        
        if channel_id:
            log_channel = guild.get_channel(channel_id)
        else:
            log_channel = None

        if not log_channel:
            return
            
        # Nome

        if before.name != after.name:
                
            embed = discord.Embed(
                title="Cargo Alterado (Nome)",
                description=f"Cargo: {before.name}",
                color=discord.Color.orange(),
                timestamp=discord.utils.utcnow()
            )
            
            embed.add_field(name="Antes", value=before.name, inline=False)
            embed.add_field(name="Depois", value=after.name, inline=False)
            embed.set_footer(text=f"ID do cargo: {after.id}")
            
            await log_channel.send(embed=embed)

        # Cor

        if before.color != after.color:
                
            embed = discord.Embed(
                title="Cargo Alterado (Cor)",
                description=f"Cargo: {before.name}",
                color=discord.Color.yellow(),
                timestamp=discord.utils.utcnow()
            )
                
            embed.add_field(name="Antes", value=str(before.color), inline=False)
            embed.add_field(name="Depois", value=str(after.color), inline=False)
            embed.set_footer(text=f"ID do cargo: {after.id}")
            
            await log_channel.send(embed=embed)
                
        # Permissões

        if before.permissions != after.permissions:
                
            embed = discord.Embed(
                title="Cargo Alterado (Permissões)",
                description=f"Cargo: {before.name}",
                color=discord.Color.red(),
                timestamp=discord.utils.utcnow()
            )
            
            embed.set_footer(text=f"ID do cargo: {after.id}")
            
            await log_channel.send(embed=embed)
    
    # 4. Canais

    # Channel_create 

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        
        guild = channel.guild
        if not guild:
            return
        
        channel_id = self.bot.log_channels.get(guild.id)
        
        if channel_id:
            log_channel = guild.get_channel(channel_id)
        else:
            log_channel = None
        
        if not log_channel:
            return
        
        embed = discord.Embed(
            title="Canal Criado",
            description=f"Canal: {channel.name}",
            color=discord.Color.green(),
            timestamp=discord.utils.utcnow()
        )

        embed.set_footer(text=f"ID do canal: {channel.id}")
       
        await log_channel.send(embed=embed)

    # Channel_delete

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):

        guild = channel.guild
        if not guild:
            return
        
        channel_id = self.bot.log_channels.get(guild.id)
        
        if channel_id:
            log_channel = guild.get_channel(channel_id)
        else:
            log_channel = None
        
        if not log_channel:
            return
        
        embed = discord.Embed(
            title="Canal Deletado",
            description=f"Canal: {channel.name}",
            color=discord.Color.red(),
            timestamp=discord.utils.utcnow()
        )

        embed.set_footer(text=f"ID do canal: {channel.id}")
       
        await log_channel.send(embed=embed)

    # Channel_update
    
    @commands.Cog.listener()
    async def on_guild_channel_update(self, before: discord.abc.GuildChannel, after: discord.abc.GuildChannel):
        
        guild = after.guild
        if not guild:
            return

        channel_id = self.bot.log_channels.get(guild.id)
        
        if channel_id:
            log_channel = guild.get_channel(channel_id)
        else:
            log_channel = None
        
        if not log_channel:
            return
        
        # Nome

        if before.name != after.name:

            embed = discord.Embed(
                title="Canal Alterado",
                description=f"Canal: {before.mention}",
                color=discord.Color.orange(),
                timestamp=discord.utils.utcnow()
            )
            
            embed.add_field(name="Antes", value=before.name, inline=False)
            embed.add_field(name="Depois", value=after.name, inline=False)
            embed.set_footer(text=f"ID do canal: {after.id}")
            
            await log_channel.send(embed=embed)

    # 5. Voz

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        
        guild = member.guild
        if not guild:
            return

        channel_id = self.bot.log_channels.get(guild.id)
        
        if channel_id:
            log_channel = guild.get_channel(channel_id)
        else:
            log_channel = None
        
        if not log_channel:
            return
        
        # Entrou em um canal de voz

        if before.channel is None and after.channel is not None:

            embed = discord.Embed(
                title="Membro Entrou (Canal de Voz)",
                description=f"{member.mention} Entrou no canal de voz {after.channel.mention}",
                color=discord.Color.green(),
                timestamp=discord.utils.utcnow()
            )

            embed.set_footer(text=f"ID do membro: {member.id}")
            
            await log_channel.send(embed=embed)

        # Saiu de um canal de voz

        elif before.channel is not None and after.channel is None:

            embed = discord.Embed(
                title="Membro Saiu (Canal de Voz)",
                description=f"{member.mention} Saiu do canal de voz {before.channel.mention}",
                color=discord.Color.orange(),
                timestamp=discord.utils.utcnow()
            )

            embed.set_footer(text=f"ID do membro: {member.id}")
            
            await log_channel.send(embed=embed)
            
        # Mudou de canal de voz
        
        elif before.channel != after.channel:

            embed = discord.Embed(
                title="Membro Mudou (Canal de Voz)",
                description=f"{member.mention} Mudou do canal de voz",
                color=discord.Color.yellow(),
                timestamp=discord.utils.utcnow()
            )
            
            embed.add_field(name="Antes", value=before.channel.mention, inline=False)
            embed.add_field(name="Depois", value=after.channel.mention, inline=False)
            embed.set_footer(text=f"ID do membro: {member.id}")
            
            await log_channel.send(embed=embed)

    # 6. Guild

    # Guild_update

    @commands.Cog.listener()
    async def on_guild_update(self, before: discord.Guild, after: discord.Guild):

        guild = after
        
        channel_id = self.bot.log_channels.get(guild.id)
        
        if channel_id:
            log_channel = guild.get_channel(channel_id)
        else:
            log_channel = None
        
        if not log_channel:
            return
        
        # Nome

        if before.name != after.name:
            
            embed = discord.Embed(
                title="Guild Alterada",
                description=f"Guild: {before.name}",
                color=discord.Color.yellow(),
                timestamp=discord.utils.utcnow()
            )
            
            embed.add_field(name="Antes", value=before.name, inline=False)
            embed.add_field(name="Depois", value=after.name, inline=False)
            embed.set_footer(text=f"ID da guild: {after.id}")
            
            await log_channel.send(embed=embed)

        # Ícone

        if before.icon != after.icon:
            
            embed = discord.Embed(
                title="Guild Alterada",
                description=f"Guild: {before.name}",
                color=discord.Color.yellow(),
                timestamp=discord.utils.utcnow()
            )
            
            embed.set_image(url=after.icon.url if after.icon else discord.Embed.Empty)
            embed.set_thumbnail(url=before.icon.url if before.icon else discord.Embed.Empty)
            embed.set_footer(text=f"ID da guild: {after.id}")
            
            await log_channel.send(embed=embed)

    # Guild_join

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        
        guild_id = 1380981509808459850
        channel_id = 1387483949323915364

        central_guild = self.bot.get_guild(guild_id)
        if not central_guild:
            return

        log_channel = central_guild.get_channel(channel_id)
        
        if not log_channel:
            return
        
        embed = discord.Embed(
            title="Bot Lua Entrou",
            description=f"Guild: {guild.name}",
            color=discord.Color.green(),
            timestamp=discord.utils.utcnow()
        )

        embed.set_footer(text=f"ID da guild: {guild.id}")

        await log_channel.send(embed=embed)
            
    # Guild_remove
    
    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        
        guild_id = 1380981509808459850
        channel_id = 1387483949323915364

        central_guild = self.bot.get_guild(guild_id)
        if not central_guild:
            return

        log_channel = central_guild.get_channel(channel_id)

        if not log_channel:
            return
        
        embed = discord.Embed(
            title="Bot Lua Saiu",
            description=f"Guild: {guild.name}",
            color=discord.Color.red(),
            timestamp=discord.utils.utcnow()
        )

        embed.set_footer(text=f"ID da guild: {guild.id}")

        await log_channel.send(embed=embed)

# Registro de cog

async def setup(bot):
    await bot.add_cog(Log(bot))