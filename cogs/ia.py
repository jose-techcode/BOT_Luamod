import discord
from discord.ext import commands
import asyncio
import logging
from datetime import timedelta
from storage import DEV_ID
from storage import API_KEY_OPEN_ROUTER
from openai import OpenAI

class Ia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=API_KEY_OPEN_ROUTER,
        )
        self.mention_mode = False

    @commands.command()
    @commands.is_owner()
    async def on(self, ctx):
        self.mention_mode = True
        await ctx.send("Modo chat ativado! Modelo de conversa: @Lua <text>")

    @commands.command()
    @commands.is_owner()
    async def off(self, ctx):
        self.mention_mode = False
        await ctx.send("Modo chat desativado!")

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.bot:
            return

        if self.mention_mode and self.bot.user in message.mentions:
            content = message.content.replace(f"<@{self.bot.user.id}>", "").strip()
            
            try:
                completion = self.client.chat.completions.create(
                    extra_headers={
                        "HTTP-Referer": "https://github.com/jose-techcode/Bot_Lua",
                        "X-Title": "Lua",
                    },
                    model="MODEL", # Substitua "MODEL" pelo modelo da IA
                    messages=[
                        {"role": "user", "content": content}
                    ]
                )
                await message.channel.send(completion.choices[0].message.content)
                return

            except Exception as e:
                logging.exception(f"Erro no comando.")
                if message.author.id == DEV_ID:
                    await message.channel.send(f"Erro: {e}")
                else:
                    await message.channel.send("Algo deu errado...")

async def setup(bot):
    await bot.add_cog(Ia(bot))