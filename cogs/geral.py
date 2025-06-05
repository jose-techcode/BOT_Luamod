import discord
from discord.ext import commands
import asyncio
from datetime import timedelta

# --Comandos gerais: !help, !lua, !ping, !avatar


# Estrutura cog (herança)


class Geral(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    # Comando: !help (pré_definido)


    # Comando: !lua


    @commands.command()
    async def lua(self, ctx):
        
        # ctx.send para mandar para o canal em que o comando foi acionado
        # except trata erros em relação a não conseguir se apresentar no canal acionado
        
        try:
            await ctx.send("Olá, me chamo Lua! Sou um bot inspirado na linguagem de programação Lua! Mas meus comandos são escritos em Python!")
            await ctx.send("https://pt.wikipedia.org/wiki/Lua_%28linguagem_de_programa%C3%A7%C3%A3o%29")
        
        except Exception as e:
            await ctx.send(f"Erro: {e}")


    # Comando: !ping
        

    @commands.command()
    async def ping(self, ctx):
        
        # ctx.send serve para mandar a mensagem abaixo quando o comando for acionado
        # ctx.author.mention é o nome membro que acionou o comando
        # except é para avisar sobre erros na execução do comando

        try:
            latency = round(self.bot.latency * 1000)
            await ctx.send(f"A latência é: {latency}ms")
        
        except Exception as e:
            print(f"Erro ao executar o comando !ping: {e}")
    

    # Comando: !avatar

    @commands.command()
    async def avatar(self, ctx, member: discord.Member = None):
        
        # member é a variavel que trata do membro que acionou o comando ou que foi acionado por outra pessoa
        # avatar_url é a variável referente ao avatar do membro
        # embed, title e color servem para mostrar o avatar da pessoa que acionou ou foi acionada no comando
        # embed.set_image serve para definir a imagem do avatar
        # embed.set_footer coloca uma observação no embed
        # icon_url serve para acionar a embed para quem acionou o comando ou para quem foi acionado pelo comando
        # ctx.send manda a embed no canal em que o comando foi acionado
        # except trata de erros que ocorrerem na execução do comando

        try:
            member = member or ctx.author
            avatar_url = member.avatar.url if member.avatar else member.default_avatar.url
            embed = discord.Embed(
                title=f"Avatar de {member.name}",
                color=discord.Color.blurple()
                )
            embed.set_image(url=avatar_url)
            embed.set_footer(text=f"Pedido por {ctx.author}",
                     icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
            await ctx.send(embed=embed)
        
        except Exception as e:
            print(f"Erro ao ver o avatar: {e}")
 
    # Comando: !info

    @commands.command()
    async def info(self, ctx):
        
        # embed, title, description e color são uma introdução à informações do bot
        # todos os embed.add_field são uma informação separada
        # user.name é referente ao nome do bot
        # user.id é referente ao id do bot
        # {len(commands.guilds)} é referente a todos os servidores do bot
        # {len(set(commands.get_all_member()))} é referente ao número total de membros que o bot abrange
        # {round(commands.latency * 1000)} é referente ao ping do bot
        # embed.set_footer serve para retornar uma "assinatura"
        # ctx.send manda a embed no canal em que o comando foi executado
        # except trata de erros do comando das informações do bot
        
        try:
            embed = discord.Embed(
            title="🤖 Informações do Bot",
            description="Informações sobre o bot Lua!",
            color=discord.Color.blue()
            )
            embed.add_field(name="Nome", value=self.bot.user.name, inline=True) # user.name
            
            embed.add_field(name="ID", value=self.bot.user.id, inline=True) # user.id
        
            embed.add_field(name="Servidores",
                    value=f"{len(self.bot.guilds)}", inline=True) # {len(commands.guilds)}
        
            embed.add_field(name="Usuários",
                    value=f"{len(set(self.bot.get_all_members()))}", inline=True) # {len(set(commands.get_all_member()))}
        
            embed.add_field(name="Latência",
                    value=f"{round(self.bot.latency * 1000)}ms", inline=True) # {round(commands.latency * 1000)}
        
            embed.set_footer(text="Desenvolvido loucamente no estilo php por Joseph")
        
            await ctx.send(embed=embed)
        
        except Exception as e:
            print(f"Erro ao executar o comando de informações do bot: {e}")


    # Comando: !infoserver


    @commands.command()
    async def infoserver(self, ctx):
        
        # guild, embed, title e color são referentes ao servidor em que o bot foi acionado
        # embed.set_thumbnail e url se referem a foto do servidor
        # todos os embed.add_field são uma informação separada do servidor
        # guild.id é referente ao id do servidor
        # guild.onwer é referente ao dono do servidor
        # guild.member_count é a quantidade total de membros no servidor
        # guild.created_at.strftime serve para expressar a data em ano, mês, dia, hora e minuto
        # guild.text_channels serve para mostrar o tamanho de canais de texto no servidor
        # guild.voice_channels serve para mostrar o tamanho de canais de voz no servidor
        # ctx.send manda a embed no canal em que foi acionado
        # except trata de erros na execução do comando das informações do servidor
        
        try:
            guild = ctx.guild
            embed = discord.Embed(
                title=f"📑 Informações do servidor: {guild.name}",
                color=discord.Color.green()
                )
            
            embed.set_thumbnail(
            url=guild.icon.url if guild.icon else discord.Embed.Empty)

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
            print(f"Erro ao executar o comando de informações do servidor: {e}")


# Registro de cog
# async com await


async def setup(bot):
    await bot.add_cog(Geral(bot))
