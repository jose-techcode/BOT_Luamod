from discord.ext import commands
from storage import DEV_ID

# Developer role

def is_dev():
    def predicate(ctx):
        return ctx.author.id == DEV_ID
    return commands.check(predicate)