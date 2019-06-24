from discord.ext import commands

import createSearchableData
import patreon_poll
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
    await search.search(query, ctx)

@bot.command()
async def add(ctx, a: int, b: int):
    await ctx.send(a + b)


@bot.command()
async def wordcount(ctx, chapter):
    await search.word_count(chapter, ctx)

@bot.command()
async def refreshUrl(ctx):
    createSearchableData.createSearchableDatafromUrl()
    await ctx.send("@everyone Done")


@bot.command()
async def refreshIndex(ctx):
    createSearchableData.createSearchableData("TWI")
    await ctx.send("@everyone Done")


@bot.command()
async def poll(ctx):
    await patreon_poll.p_poll(ctx)

bot.run(secrets.bot_token)
