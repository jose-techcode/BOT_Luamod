import discord
from discord.ext import commands
import asyncio
from datetime import timedelta

# --Comandos de moderação: !apagar, !lento, !silenciar, "dessilenciar automático", !dessilenciar, !trancar, !destrancar !expulsar, !banir, !desbanir, !dm

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
            await ctx.send(f"{member.mention} foi silenciado por {tempo} minutos.")
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

    # Comando: !dm

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def dm(self, ctx, membro: discord.Member, *, mensagem):
        # membro.send é o comando para o administrador poder mandar mensagem na dm de um membro
        try:
            await membro.send(mensagem)
            await ctx.send(f"Mensagem enviada para {membro.mention}!") 
        except Exception as e:
            await ctx.send(f"Não consegui enviar a DM. Talvez ela esteja bloqueada. Erro: {e}")

# Registro de cog

async def setup(bot):
    await bot.add_cog(Admin(bot))