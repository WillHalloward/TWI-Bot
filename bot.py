import discord
from discord.ext import commands

import createSearchableData
import patreon_poll
import prediction
import search
import secrets

bot = commands.Bot(command_prefix='!', description="test bot")
bot.remove_command("help")



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
async def wordcount(ctx, chapter):
    await search.word_count(chapter, ctx)

@bot.command()
@commands.is_owner()
async def refreshUrl(ctx):
    createSearchableData.createSearchableDatafromUrl()
    await ctx.send("@everyone Done")


@bot.command()
@commands.is_owner()
async def refreshIndex(ctx):
    createSearchableData.createSearchableData("TWI")
    await ctx.send("@everyone Done")


@bot.command()
async def poll(ctx):
    await patreon_poll.p_poll(ctx)


@bot.command()
async def bet(ctx, time, words):
    await prediction.bet(ctx, time, words)


@bot.command()
async def av(ctx):
    embed = discord.Embed(title="Avatar", color=discord.Color(0x3cd63d))
    embed.set_image(url=ctx.author.avatar_url)
    await ctx.send(embed=embed)


@bot.command()
@commands.is_owner()
async def setPoll(ctx):
    await ctx.send("New poll set to <{}>".format(await patreon_poll.set_poll(ctx)))
    message = await patreon_poll.p_poll(ctx)
    await message.pin()


@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Help", color=discord.Color(0x3cd63d), description="List of commands")
    embed.add_field(name="!find", value="Searches in The Wandering Inn after the text given.\n"
                                        "Usage: !find: \"the dragon roared\", !find magnolia.\n"
                                        "**Note** searches longer than 1 word need to be surrounded in \"\"")
    embed.add_field(name="!wordcount", value="Gets the wordcount of the chapter given.\n"
                                             "Usage: !wordcount 6.25, !wordcount \"1.06 D\"\n"
                                             "**Note** searches longer than 1 word need to be surrounded in \"\"")
    embed.add_field(name="!poll", value="Posts the current tally of the patreon poll.")
    embed.add_field(name="!bet", value="Stake a bet on the time and word count of the next chapter.\n"
                                       "Usage: !bet 1h 1k, !bet \"2h 30m\" 17k")
    embed.add_field(name="!av", value="Posts the full version of your current avatar")
    await ctx.send(embed=embed)


bot.run(secrets.bot_token)
