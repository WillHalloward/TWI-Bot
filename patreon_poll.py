import json
from datetime import datetime

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
            with open("poll_url.txt", "w+") as d:
                d.write(url)
            return "https://www.patreon.com" + posts['attributes']['patreon_url']
    return "No poll found"





async def p_poll(ctx):
    try:
        with open("poll_url.txt", "r") as d:
            url = d.read()
    except:
        await ctx.send("**Error** - No poll set, Please run **!setPoll** to set poll")
        return
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
    for i in range(0, len(n_options)):
        print(option[i]['attributes']['text_content'])
        print(option[i]['attributes']['num_responses'])
        embed.add_field(name="{}".format(option[i]['attributes']['text_content']),
                        value="{}".format(option[i]['attributes']['num_responses']), inline=False)
    return await ctx.send(embed=embed)
# TODO Make poll automagically update every x min.
# TODO make bot pin poll.
# TODO make footer time in local time.
# TODO Poll stats?
