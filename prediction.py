import json
import typing

import dateparser


async def bet(ctx, time, word: typing.Union[int, str]):
    d_time = dateparser.parse("in " + time)
    d_time = d_time.replace(microsecond=0)
    if "k" in word:
        word = int(word.split("k")[0]) * 1000
    await ctx.send("You bet {} and {} words.".format(d_time, word))
    message = await ctx.send("Is this correct?")
    confirm = '<:confirm:592712644344020992>'
    deny = '<:deny:592712576237043712>'
    await message.add_reaction(confirm)
    await message.add_reaction(deny)
    # WAIT FOR CHECK HERE TO LOOK IF THEY REACT WITH DENY OR CONFIRM.
    with open('data.json', 'r') as json_file:
        data = json.load(json_file)
        i = 0
        dupe_id = True
        for bets in data['bet']:
            if ctx.author.id == bets['user']:
                dupe_id = False
                index = i
        i += 1
        if dupe_id:
            data['bet'].append({
                'user': ctx.author.id,
                'time': str(d_time),
                'words': word
            })
        else:
            await ctx.send("It looks like you already have a standing bet with {} and {} words.\nwould you like to "
                           "replace it with your new bet with {} and {} words?"
                           .format(data['bet'][index]['time'], data['bet'][index]['words'], d_time, word))
            # WAIT FOR CHECK HERE TO LOOK IF THEY REACT WITH DENY OR CONFIRM.
            del data['bet'][index]
        with open('data.json', 'w+') as outfile:
            outfile.write(json.dumps(data, indent=4, sort_keys=True))
