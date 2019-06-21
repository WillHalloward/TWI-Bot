import sys

from whoosh import highlight, qparser
from whoosh import scoring
from whoosh.index import open_dir
from whoosh.qparser import QueryParser

ix = open_dir("indexdir")

query_str = sys.argv[1]
parser = QueryParser("content", ix.schema)
parser.add_plugin(qparser.FuzzyTermPlugin())
query = parser.parse(query_str)

with ix.searcher(weighting=scoring.BM25F) as searcher:
    results = searcher.search(query)
    results.fragmenter = highlight.SentenceFragmenter()
    results.formatter = highlight.UppercaseFormatter()

    for hit in results:
        print(hit["title"])
        print("Score: " + str(hit.score))
        print("Rank: ", hit.rank)
        with open(hit["path"], encoding="utf8") as fileobj:
            filecontents = fileobj.read()
            print(hit.highlights("content", text=filecontents))
