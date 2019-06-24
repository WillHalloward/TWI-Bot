import dateparser


async def bet(ctx, time, word):
    d_time = dateparser.parse("in " + time)
    print(d_time)
    if "k" in word:
        word = int(word.split("k")[0]) * 1000
    await ctx.send("You bet {} and {} words.".format(d_time, word))
