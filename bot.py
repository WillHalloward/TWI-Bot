from discord.ext import commands

import createSearchableData
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
async def find(ctx, query, n: int):
    try:
        output = search.search(query, n)
        await ctx.send(output)
    except:
        await ctx.send("Error")


@bot.command()
async def add(ctx, a: int, b: int):
    await ctx.send(a + b)


@bot.command()
async def refreshUrl(ctx):
    createSearchableData.createSearchableDatafromUrl()
    await ctx.send("@everyone Done")


@bot.command()
async def refreshIndex(ctx):
    createSearchableData.createSearchableData("TWI")
    await ctx.send("@everyone Done")


bot.run(secrets.bot_token)
