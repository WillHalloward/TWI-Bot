from whoosh import highlight, qparser
from whoosh import scoring
from whoosh.index import open_dir
from whoosh.qparser import QueryParser


class DiscordBoldFormatter(highlight.Formatter):
    def format_token(self, text, token, replace=False):
        tokentext = highlight.get_text(text, token, replace)
        return "**%s**" % tokentext


def search(query_str):
    ix = open_dir("indexdir")

    parser = QueryParser("content", ix.schema)
    parser.add_plugin(qparser.FuzzyTermPlugin())
    query = parser.parse(query_str)
    print(query)

    with ix.searcher(weighting=scoring.PL2) as searcher:
        results = searcher.search(query, limit=3)
        results.fragmenter = highlight.SentenceFragmenter()
        results.formatter = DiscordBoldFormatter()

        discord_output = ""
        for hit in results:
            title = hit["title"].rsplit('.', 1)[0]
            discord_output = discord_output + "\nChapter: " + title
            discord_output = discord_output + "\nScore: " + str(hit.score)
            discord_output = discord_output + "\nRank: " + str(hit.rank + 1)
            discord_output = discord_output + "\n" + hit.highlights("content")
        return discord_output

# TODO Make discord output an embed.
# TODO Allow search sorting by time instead of score
# TODO Add link to chapter in results
# TODO Add Pov tags to chapters to allow search on them.
# TODO allow choosing how many results to show.
# TODO Fix empty results on ex: "gun"
# TODO Fix highlight sometimes just highlighting 1 word.
# TODO Add command help
# TODO Add error messages
