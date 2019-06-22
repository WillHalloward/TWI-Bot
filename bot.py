from discord.ext import commands

import search
import secrets

bot = commands.Bot(command_prefix='!', description="test bot")


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command()
async def find(ctx, query):
    output = search.search(query)
    await ctx.send(output)


@bot.command()
async def add(ctx, a: int, b: int):
    await ctx.send(a + b)


bot.run(secrets.bot_token)
