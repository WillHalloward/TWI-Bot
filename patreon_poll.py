import json
from datetime import datetime, timedelta
from operator import itemgetter

import discord
import requests

import secrets


async def set_poll(ctx):
    url = "https://www.patreon.com/api/posts?include=user%2Cattachments%2Cuser_defined_tags%2Ccampaign%2Cpoll.choices%2Cpoll.current_user_responses.user%2Cpoll.current_user_responses.choice%2Cpoll.current_user_responses.poll%2Caccess_rules.tier.null%2Cimages.null%2Caudio.null&fields[post]=change_visibility_at%2Ccomment_count%2Ccontent%2Ccurrent_user_can_delete%2Ccurrent_user_can_view%2Ccurrent_user_has_liked%2Cembed%2Cimage%2Cis_paid%2Clike_count%2Cmin_cents_pledged_to_view%2Cpost_file%2Cpublished_at%2Cpatron_count%2Cpatreon_url%2Cpost_type%2Cpledge_url%2Cthumbnail_url%2Cteaser_text%2Ctitle%2Cupgrade_url%2Curl%2Cwas_posted_by_campaign_owner&fields[user]=image_url%2Cfull_name%2Curl&fields[campaign]=avatar_photo_url%2Cearnings_visibility%2Cis_nsfw%2Cis_monthly%2Cname%2Curl&fields[access_rule]=access_rule_type%2Camount_cents&fields[media]=id%2Cimage_urls%2Cdownload_url&sort=-published_at&filter[campaign_id]=568211&filter[is_draft]=false&filter[contains_exclusive_posts]=true&json-api-use-default-includes=false&json-api-version=1.0"
    page = requests.get(url, cookies=secrets.cookies)
    json_data = json.loads(page.text)
    for posts in json_data['data']:
        if posts['relationships']['poll']['data'] is not None:
            url = posts['relationships']['poll']['links']['related']
            links = {
                "api": url,
                "url": "https://www.patreon.com" + posts['attributes']['patreon_url']
            }
            message = await ctx.send("Poll set to <{}>".format(links['url']))

            with open("api_url.json", "w+") as d:
                json.dump(links, d)
            return True
    return False


async def p_poll(ctx):
    try:
        with open("api_url.json", 'r') as f:
            file_json = json.load(f)
    except OSError.filename:
        await ctx.send("**Error** - No poll set, Please run **!setpoll** to set poll")
        return
    page = requests.get(file_json['api'], cookies=secrets.cookies)
    json_data = json.loads(page.text)
    open_at = json_data['data']['attributes']['created_at']
    closes_at = json_data['data']['attributes']['closes_at']
    title = json_data['data']['attributes']['question_text']
    open_at_converted = datetime.strptime(open_at, '%Y-%m-%dT%H:%M:%S.%f+00:00')
    closes_at_converted = datetime.strptime(closes_at, '%Y-%m-%dT%H:%M:%S.%f+00:00')
    time_left = closes_at_converted - datetime.now() + timedelta(hours=3)
    hours = int(((time_left.total_seconds() // 3600) % 24))
    li = []
    for i in range(0, len(json_data['data']['relationships']['choices']['data'])):
        data = (json_data['included'][i]['attributes']['text_content'],
                json_data['included'][i]['attributes']['num_responses'])
        li.append(data)
    li = sorted(li, key=itemgetter(1), reverse=True)
    embed = discord.Embed(title="Poll", color=discord.Color(0x3cd63d),
                          description="**[{}]({})**".format(title, file_json['url']))
    embed.set_footer(
        text="Poll started at {} and closes at {} ({} days and {} hours left)".format(open_at_converted,
                                                                                      closes_at_converted,
                                                                                      time_left.days, hours))
    for option in li:
        embed.add_field(name=option[0], value=option[1], inline=False)
    return embed


async def update_poll(ctx):
    try:
        with open("api_url.json", 'r') as f:
            file_json = json.load(f)
    except OSError.filename:
        return
    msg = await ctx.fetch_message(file_json['poll_id'])
    await msg.edit(embed=await p_poll(ctx))


# TODO Make poll automagically update every x min.
# TODO make footer time in local time.
# TODO Poll stats?
# TODO Make !SetPoll unpin previous poll pin.
# TODO Make poll send out notification when poll is closed and declare winner.
