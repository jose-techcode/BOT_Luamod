import discord
from discord.ext import commands
import asyncio
import logging
from datetime import timedelta
from storage import DEV_ID

# Cog structure (inheritance)

class Geral(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Command: ping
        
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    async def ping(self, ctx):
        try:
            latency = round(self.bot.latency * 1000)
            await ctx.send(f"A latência é: {latency}ms")
        except Exception as e:
            logging.exception(f"Erro no comando.")
            if ctx.author.id == DEV_ID:
                await ctx.send(f"Erro: {e}")
            else:
                await ctx.send("Algo deu errado...")
    
    # Command: ajuda
    
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    async def ajuda(self, ctx):
        embed = discord.Embed(
            title="Central de Comandos",
            description="Veja os comandos disponíveis organizados por categoria. Considere criar um canal e usar .setlog <channel> para ter acesso ao sistema de logs do bot.",
            color=discord.Color.blurple()
        )
        # I. Members
        embed.add_field(name="I. Gerais", value="""
`.ping` - Mostra a latência do bot.
`.ajuda` - Mostra a lista de comandos.
`.avatar <member>` - Mostra o avatar de um membro.
`.userinfo <member>` - Mostra as informações do usuário.
`.serverinfo` - Mostra informações do servidor.
`.botinfo` - Mostra informações do bot.                        
""", inline=False)

        # II. Moderators
        embed.add_field(name="II. Moderadores", value="""
`.warn <member> <reason>` - Avisa um usuário.
`.unwarn <member>` - Limpa os avisos de um usuário.
`.warnings <member>` - Vê a quantidade e o(s) motivo(s) dos avisos de um usuário.
`.warninglist` - Vê a quantidade e os usuários avisados.
`.clear <qtd>` - Apaga mensagens do chat.
`.purge <member> <qtd>` - Apaga mensagens de um membro.
`.slow <seconds>` - Ativa o modo lento no canal.
`.lock` - Tranca um canal.
`.unlock` - Destranca um canal.
`.lockdown` - Tranca todos os canais.
`.unlockdown` - Destranca todos os canais.
`.mute <member> <minutes>` - Silencia um membro por um tempo.
`.unmute <member>` - Remove o silêncio de um membro.
`.kick <member>` - Expulsa um membro do servidor.
`.ban <member>` - Bane um membro do servidor.
`.unban <ID>` - Remove o banimento de um usuário.
`.tempban <member> <qtd>` - Bane um membro do servidor por um tempo.
`.softban <member>` - Bane um membro do servidor por um segundo.
`.setlog <channel>` - Define um canal para receber logs de ações do servidor.
""", inline=False)

        # III. Developers — DEV_ID only
        if ctx.author.id == DEV_ID:
            embed.add_field(name="III. Desenvolvedores", value="""
`.restart` - Reinicia o bot.
`.toswitchoff` - Desliga o bot.
`.log` - Vê o histórico de logs do bot.
`.clearlog` - Limpa o histórico de logs do bot.
`.reloadcog <cog>` - Recarrega uma cog específica.
`.debug` - Exibe informações gerais e técnicas do bot.                           
""", inline=False)
            
        # IV. IA
        if ctx.author.id == DEV_ID:
            embed.add_field(name="IV. IA", value="""
`.on` - Liga o chat da IA.
`.off` - Desliga o chat da IA.
""", inline=False)

        embed.set_footer(text="Bot Luamod")
        await ctx.send(embed=embed)

    # Command: avatar

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    async def avatar(self, ctx, member: discord.Member = None):
        # member is the variable that refers to the member who triggered the command or was triggered by someone else.
        # avatar_url is the variable referring to the member's avatar.
        # embed, title, and color are used to display the avatar of the person who triggered or was triggered by the command.
        # embed.set_image is used to set the avatar image.
        # embed.set_footer places a note on the embed.
        # icon_url is used to trigger the embed for the person who triggered the command or for the person triggered by the command.
        try:
            member = member or ctx.author
            avatar_url = member.avatar.url if member.avatar else member.default_avatar.url
            embed = discord.Embed(
                title=f"Avatar de {member.name}",
                color=discord.Color.blue()
                )
            embed.set_image(url=avatar_url)
            embed.set_footer(text=f"Pedido por {ctx.author}",
                     icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
            await ctx.send(embed=embed)
        except Exception as e:
            logging.exception(f"Erro no comando.")
            if ctx.author.id == DEV_ID:
                await ctx.send(f"Erro: {e}")
            else:
                await ctx.send("Algo deu errado...")

    # Command: userinfo

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    async def userinfo(self, ctx, member: discord.Member = None):
        # roles is a variable referring to the member's roles on the server
        # all embed.add_fields are separate pieces of information about the member
        # member.display_avat.url is to display the member's image
        # member.name is the member's name
        # {member} is the member's tag
        # member.id is the member's ID
        # member.created.at.strftime is the user's account creation date
        # member.joined.at.strftime is the user's joined date
        # join(roles) is an integration with the roles variable
        member = member or ctx.author
        roles = [role.mention for role in member.roles if role != ctx.guild.default_role]
        try:
            embed = discord.Embed(
                title=f"Informações de usuário",
                color=discord.Color.blue()
            )
            embed.set_thumbnail(url=member.display_avatar.url) # member.display_avat.url
            embed.add_field(name="Nome", value=member.name, inline=True) # member.name
            embed.add_field(name="ID", value=member.id, inline=True) # member.id
            embed.add_field(name="Conta criada em", value=member.created_at.strftime("%d/%m/%Y %H:%M"), inline=False) # member.created.at.strftime
            embed.add_field(name="Entrou no servidor", value=member.joined_at.strftime("%d/%m/%Y %H:%M"), inline=False) # member.joined_at.strftime
            embed.add_field(name="Cargos", value=", ".join(roles) if roles else "Nenhum", inline=False) # join(roles)
            await ctx.send(embed=embed)
        except Exception as e:
            logging.exception(f"Erro no comando.")
            if ctx.author.id == DEV_ID:
                await ctx.send(f"Erro: {e}")
            else:
                await ctx.send("Algo deu errado...")

    # Command: serverinfo

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    async def serverinfo(self, ctx):
        # guild, embed, title, and color refer to the server where the bot was triggered
        # ctx.guild.icon.url is the server image
        # all embed.add_fields are separate server information
        # guild.id refers to the server ID
        # guild.onwer refers to the server owner
        # guild.member_count is the total number of members on the server
        # guild.created_at.strftime is used to express the date in year, month, day, hour, and minute
        # guild.text_channels is used to display the size of text channels on the server
        # guild.voice_channels is used to display the size of voice channels on the server
        try:
            guild = ctx.guild
            embed = discord.Embed(
                title=f"Informações do servidor: {guild.name}",
                color=discord.Color.blue()
                )
            embed.set_thumbnail(url=ctx.guild.icon.url if ctx.guild.icon else "") # ctx.guild.icon.url
            embed.add_field(name="ID", value=guild.id, inline=True) # guild.id
            embed.add_field(name="Dono", value=guild.owner, inline=True) # guild.owner
            embed.add_field(name="Membros", value=guild.member_count, inline=True) # guild.member_count
            embed.add_field(name="Criado em", value=guild.created_at.strftime(
            "%d/%m/%Y %H:%M"), inline=True) # guild.created_at.strftime
            embed.add_field(name="Canais de texto", value=len(
            guild.text_channels), inline=True) # guild.text_channels
            embed.add_field(name="Canais de voz", value=len(
            guild.voice_channels), inline=True) # guild.voice_channels
            await ctx.send(embed=embed)
        except Exception as e:
            logging.exception(f"Erro no comando.")
            if ctx.author.id == DEV_ID:
                await ctx.send(f"Erro: {e}")
            else:
                await ctx.send("Algo deu errado...")

    # Comando: botinfo

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    async def botinfo(self, ctx):
        # embed, title, description, and color are an introduction to the bot's information
        # all embed.add_fields are separate pieces of information about the bot
        # ctx.me.display_avatar.url is the bot's image
        # user.name refers to the bot's name
        # user.id refers to the bot's ID
        # {len(commands.guilds)} refers to all the bot's servers
        # {len(set(commands.get_all_member()))} refers to the total number of members the bot covers
        # {round(commands.latency * 1000)} refers to the bot's ping
        # embed.set_footer serves to return a "signature"
        try:
            embed = discord.Embed(
            title="Informações do bot Lua",
            color=discord.Color.blue()
            )
            embed.set_thumbnail(url=ctx.me.display_avatar.url) # ctx.me.display_avatar.url
            embed.add_field(name="Nome", value=self.bot.user.name, inline=True) # user.name
            embed.add_field(name="ID", value=self.bot.user.id, inline=True) # user.id
            embed.add_field(name="Servidores",
                    value=f"{len(self.bot.guilds)}", inline=True) # {len(commands.guilds)}
            embed.add_field(name="Usuários",
                    value=f"{len(set(self.bot.get_all_members()))}", inline=True) # {len(set(commands.get_all_member()))}
            embed.add_field(name="Latência",
                    value=f"{round(self.bot.latency * 1000)}ms", inline=True) # {round(commands.latency * 1000)}   
            embed.set_footer(text="Desenvolvido por Joseph.")
            await ctx.send(embed=embed)
        except Exception as e:
            logging.exception(f"Erro no comando.")
            if ctx.author.id == DEV_ID:
                await ctx.send(f"Erro: {e}")
            else:
                await ctx.send("Algo deu errado...")

# Cog registration

async def setup(bot):
    await bot.add_cog(Geral(bot))
