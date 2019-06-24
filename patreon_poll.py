import json
from datetime import datetime

import discord
import requests

import secrets


async def p_poll(ctx):
    url = "https://www.patreon.com/api/polls/218745"
    page = requests.get(url, cookies=secrets.cookies)
    json_data = json.loads(page.text)
    open_at = json_data['data']['attributes']['created_at']
    closes_at = json_data['data']['attributes']['closes_at']
    title = json_data['data']['attributes']['question_text']
    open_at_converted = datetime.strptime(open_at, '%Y-%m-%dT%H:%M:%S.%f+00:00')
    closes_at_converted = datetime.strptime(closes_at, '%Y-%m-%dT%H:%M:%S.%f+00:00')
    option = json_data['included']
    n_options = json_data['data']['relationships']['choices']['data']
    embed = discord.Embed(title="Poll", color=discord.Color(0x3cd63d), description="**{}**".format(title))
    embed.set_footer(text="Poll started at {} and closes at {}".format(open_at_converted, closes_at_converted))
    x = len(n_options)
    for i in range(0, x):
        print(option[i]['attributes']['text_content'])
        print(option[i]['attributes']['num_responses'])
        embed.add_field(name="{}".format(option[i]['attributes']['text_content']),
                        value="{}".format(option[i]['attributes']['num_responses']), inline=False)
    # for options in option:
    await ctx.send(embed=embed)
# TODO Get latest poll automatically
# TODO Make poll automagically update every x min.
# TODO make bot pin poll.
# TODO make 2 separate commands, !setpoll and poll
# TODO make footer time in local time.
