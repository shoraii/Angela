import discord
from discord.ext import commands
from botsettings import *

bot = commands.Bot(command_prefix='Angela, ')

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

bot.run(TOKEN)