import discord
from discord.ext import commands
import asyncio
import logging
from datetime import timedelta
from storage import DEV_ID

# Estrutura cog (herança)

class Geral(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Comando: ping
        
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
    
    # Comando: ajuda
    
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    async def ajuda(self, ctx):
        embed = discord.Embed(
            title="Central de Comandos",
            description="Veja os comandos disponíveis organizados por categoria. Considere criar um canal e usar .setlog <channel> para ter acesso ao sistema de logs do bot.",
            color=discord.Color.blurple()
        )
        # I. Membros comuns
        embed.add_field(name="I. Gerais", value="""
`.ping` - Mostra a latência do bot.
`.ajuda` - Mostra a lista de comandos.
`.avatar <member>` - Mostra o avatar de um membro.
`.userinfo <member>` - Mostra as informações do usuário.
`.serverinfo` - Mostra informações do servidor.
`.botinfo` - Mostra informações do bot.                        
""", inline=False)

        # II. Moderadores
        embed.add_field(name="II. Moderadores", value="""
`.warn <member> <reason>` - Avisa um usuário.
`.unwarn <member>` - Retira todos os avisos do usuário.
`.warnings <member>` - Vê a quantidade e motivo dos avisos de um usuário.
`.warninglist` - Vê usuários avisados e quantidade de avisos.
`.clear <quantity>` - Apaga mensagens do chat.
`.slow <seconds>` - Ativa o modo lento no canal.
`.lock` - Tranca um canal.
`.unlock` - Destranca um canal trancado.
`.mute <member> <minutes>` - Silencia um membro temporariamente.
`.unmute <member>` - Remove o silêncio de um membro.
`.kick <member>` - Expulsa um membro do servidor.
`.ban <member>` - Bane um membro do servidor.
`.unban <ID>` - Remove o banimento de um usuário pelo ID.
`.setlog <channel>` - Define um canal para receber logs de ações do servidor.
""", inline=False)

        # III. Desenvolvedores — só para DEV_ID
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

    # Comando: avatar

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    async def avatar(self, ctx, member: discord.Member = None):
        # member é a variavel que trata do membro que acionou o comando ou que foi acionado por outra pessoa
        # avatar_url é a variável referente ao avatar do membro
        # embed, title e color servem para mostrar o avatar da pessoa que acionou ou foi acionada no comando
        # embed.set_image serve para definir a imagem do avatar
        # embed.set_footer coloca uma observação no embed
        # icon_url serve para acionar a embed para quem acionou o comando ou para quem foi acionado pelo comando
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

    # Comando: userinfo

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    async def userinfo(self, ctx, member: discord.Member = None):
        # roles é uma variável referente aos cargos que o membro tem no servidor
        # todos os embed.add_field são uma informação separada sobre o membro
        # member.display_avat.url é para mostrar a imagem do membro
        # member.name é o nome do membro
        # {member} é a tag do membro
        # member.id é o id do membro
        # member.created.at.strftime é a data de criação da conta do usuário
        # member.joined.at.strftime é a data em que o usuário entrou no servidor
        # join(roles) é uma integração com a variável roles
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

    # Comando: serverinfo

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    async def serverinfo(self, ctx):
        # guild, embed, title e color são referentes ao servidor em que o bot foi acionado
        # ctx.guild.icon.url é a imagem do servidor
        # todos os embed.add_field são uma informação separada do servidor
        # guild.id é referente ao id do servidor
        # guild.onwer é referente ao dono do servidor
        # guild.member_count é a quantidade total de membros no servidor
        # guild.created_at.strftime serve para expressar a data em ano, mês, dia, hora e minuto
        # guild.text_channels serve para mostrar o tamanho de canais de texto no servidor
        # guild.voice_channels serve para mostrar o tamanho de canais de voz no servidor
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
        # embed, title, description e color são uma introdução à informações do bot
        # todos os embed.add_field são uma informação separada sobre o bot
        # ctx.me.display_avatar.url é a imagem do bot
        # user.name é referente ao nome do bot
        # user.id é referente ao id do bot
        # {len(commands.guilds)} é referente a todos os servidores do bot
        # {len(set(commands.get_all_member()))} é referente ao número total de membros que o bot abrange
        # {round(commands.latency * 1000)} é referente ao ping do bot
        # embed.set_footer serve para retornar uma "assinatura"
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

# Registro de cog

async def setup(bot):
    await bot.add_cog(Geral(bot))
