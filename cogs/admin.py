import discord
from discord.ext import commands
from discord import app_commands
import asyncio
from datetime import timedelta

# --Comandos de moderação: !apagar, !lento, !silenciar, "dessilenciar automático", !dessilenciar, !expulsar, !banir, !desbanir


# Estrutura cog (herança)


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    # Comando: !apagar


    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def apagar(self, ctx, quantidade_mensagens: int):
        
        # ctx.channel.purge serve para poder apagar a quantidade de mensagens definidas no canal
        # limit serve para definir um limite de mensagens apagadas
        # ctx.send é para impedir apagar as mensagens caso dê algum erro na ação
        # delete_after=5 é a quantidade de segundos que o bot levará para apagar as mensagens
        # except irá tratar erros caso o bot não consiga apagar
        
        try:
            await ctx.channel.purge(limit=quantidade_mensagens)
            await ctx.send(f"Foram apagadas {quantidade_mensagens} mensagens.", delete_after=5)
        
        except Exception as e:
            await ctx.send(f"Não foi possível apagar as mensagens! Erro: {e}")


    # Comando: !lentidao


    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def lentidao(self, ctx, tempo: int):
        
        # ctx.channel.edit serve editar as configurações do canal
        # slowmode_delay é para especificar o tipo de edição que será realizado no servidor
        # o ctx.send serve para confirmar que a lentidão funcionou no canal
        # except irá confirmar se houve algum erro em aplicar lentidão a determinado canal
        
        try:
            await ctx.channel.edit(slowmode_delay=tempo)
            await ctx.send(f"O modo lento foi definido para {tempo} segundos")
        
        except Exception as e:
            await ctx.send(f"Não foi possível definir um tempo de lentidão no canal! Erro: {e}")


    # Comando: !silenciar (dessilenciar automático)


    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def silenciar(self, ctx, member: discord.Member, tempo: int):
        
        # "cargo" serve para procurar o cargo chamado "mutado", se não existir, retorna o erro
        # ctx.send traz uma mensagem se não tiver o cargo "mutado"
        # member.add_roles serve para adicionar o cargo "mutado" quando o membro for silenciado
        # ctx.send confirma que o membro foi silenciado
        # asyncio.sleep serve para aplicar o tempo definido na hora da punição
        # member.remove_roles irá retirar o cargo de "mutado" do membro que cumprir o silenciamento
        # except irá tratar sobre o silenciamento quando não for possível silenciar tal usuário
        
        try:
            cargo = discord.utils.get(ctx.guild.roles, name="mutado")
            if not cargo:
                await ctx.send("O cargo 'mutado' não foi encontrado no servidor.")
                return
            await member.add_roles(cargo, reason="Silenciado pelo bot")
            await ctx.send(f"{member.mention} foi silenciado por {tempo} segundos.")
            await asyncio.sleep(tempo)
            await member.remove_roles(cargo, reason="Tempo de silenciamento expirado.")
            await ctx.send(f"{member.mention} não está mais silenciado.")
        
        except Exception as e:
            await ctx.send(f"Não foi possível silenciar o usuário! Erro: {e}")


    # Comando: !dessilenciar (manual)


    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def dessilenciar(self, ctx, member: discord.Member):
        
        # cargo é a variável que serve para acessar o gerenciamento do nome "mutado" no servidor
        # if not cargo trata sobre quando não tem o nome "mutado" no servidor
        # member.remove_roles é para remover o cargo "mutado" que aplica silenciamento
        # ctx.send confirma que o dessilenciamento foi um sucesso
        # except irá tratar erros relacionados ao dessilenciamento do usuário
        
        try:
            cargo = discord.utils.get(ctx.guild.roles, name="mutado")
            if not cargo:
                await ctx.send("O cargo 'mutado' não foi encontrado no servidor.")
                return
            await member.remove_roles(cargo, reason="Dessilenciado manualmente")
            await ctx.send(f"{member.mention} foi dessilenciado!")
        
        except Exception as e:
            await ctx.send(f"Não foi possível dessilenciar o membro! Erro: {e}")


    # Comando: !expulsar


    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def expulsar(self, ctx, member: discord.Member, *, motivo="Não especificado"):
        
        # member.kick é um comando específico para expulsão
        # ctx.send serve para confirmar a punição
        # except serve para confirmar algum erro em meio a tentativa de expulsão de um membro
        
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
        # ctx.send serve para confirmar a punição
        # except trata de casos onde não é possível banir o membro
        
        try:
            await member.ban(reason=motivo)
            await ctx.send(f"{member.mention} foi banido do servidor! Motivo: {motivo}")
        
        except Exception as e:
            await ctx.send(f"Não foi possível banir determinado membro! Erro: {e}")


    # Comando: !desbanir


    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def desbanir(self, ctx, user_id: int):
        
        # user serve definir que o banimento deve ser realizado por id de usuário
        # ctx.guild.unban(user) serve para desbanir determinado usuário por id
        # ctx.send é para confirmar o desbanimento
        # except irá retornar erros em relação ao desbanimento caso haja
        
        try:
            user = await self.bot.fetch_user(user_id)
            await ctx.guild.unban(user)
            await ctx.send(f"O usuário {user.mention} foi desbanido com sucesso!")
        
        except Exception as e:
            await ctx.send(f"Não foi possível desbanir o usuário com ID {user_id}. Erro: {e}")


    # Comando: !dm

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def dm(self, ctx, membro: discord.Member, *, mensagem):
        
        # membro é a menção do usuário
        # mensagem é a mensagem ao qual será mandada no privado da pessoa
        # membro.mention é o membro que foi mencionado e não o que acionou o comando
        # ctx.send é para confirmar a mensagem no canal em que foi acionado o bot
        
        try:
            await membro.send(mensagem)
            await ctx.send(f"Mensagem enviada para {membro.mention}!")
        
        except Exception as e:
            await ctx.send(f"Não consegui enviar a DM. Talvez ela esteja bloqueada. Erro: {e}")


# Registro de cog
# async com await

async def setup(bot):
    await bot.add_cog(Admin(bot))