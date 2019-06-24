import discord
from whoosh import highlight, qparser, scoring
from whoosh.index import open_dir
from whoosh.qparser import GtLtPlugin, QueryParser
from whoosh.qparser.dateparse import DateParserPlugin


class DiscordBoldFormatter(highlight.Formatter):
    def format_token(self, text, token, replace=False):
        tokentext = highlight.get_text(text, token, replace)
        return "**%s**" % tokentext


async def search(query_str, ctx):
    ix = open_dir("indexdir")
    parser = QueryParser("content", ix.schema)
    parser.add_plugin(qparser.FuzzyTermPlugin())
    parser.add_plugin(GtLtPlugin())
    parser.add_plugin(DateParserPlugin())
    query = parser.parse(query_str)
    print(query)
    with ix.searcher(weighting=scoring.PL2) as searcher:
        results = searcher.search(query, limit=5)
        results.fragmenter = highlight.SentenceFragmenter()
        results.fragmenter.surround = 50
        results.fragmenter.maxchars = 10000
        results.formatter = DiscordBoldFormatter()
        embed = discord.Embed(title="Results", color=discord.Color(0x3cd63d),
                              description="From search: **{}**".format(query_str))
        for hit in results:
            # embed.add_field(name="[{}]({})".format(hit["title"], hit["url"]), value="{}".format(hit.highlights("content")))
            embed.add_field(name="\u200b",
                            value=f"[{hit['title']}]({hit['url']})\n"
                            f"{hit.highlights('content', minscore=0)}",
                            inline=False)
    await ctx.send(embed=embed)


async def word_count(query_str, ctx):
    ix = open_dir("indexdir")
    parser = QueryParser("title", ix.schema)
    query = parser.parse(query_str)
    parser.add_plugin(DateParserPlugin())
    print(query)
    with ix.searcher(weighting=scoring.BM25F) as searcher:
        results = searcher.search(query)
        embed = discord.Embed(title="Wordcount", color=discord.Color(0x3cd63d))
        for hit in results:
            embed.add_field(name="{}".format(hit["title"]), value="Wordcount: **{}**".format(hit["wordcount"]))
        await ctx.send(embed=embed)

# TODO Allow search sorting by time instead of score
# TODO Add Pov tags to chapters to allow search on them.
# TODO Fix empty results on ex: "gun", "crow"
# TODO Fix highlight sometimes just highlighting 1 word.
# TODO Add command help
# TODO Add error handling
# TODO automatically add the latest public chapter to index
# TODO Remove next chapter/previous chapter from bottom of content
