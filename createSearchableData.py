import os

from whoosh.fields import Schema, TEXT, ID
from whoosh.index import create_in


def createSearchableData(root):
    schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT(stored=True),
                    textdata=TEXT(stored=True))
    if not os.path.exists("indexdir"):
        os.mkdir("indexdir")
    ix = create_in("indexdir", schema)
    writer = ix.writer()
    filepath = [os.path.join(root, i) for i in os.listdir(root)]
    for path in filepath:
        print(path)
        fp = open(path, 'r', encoding="UTF-8")
        text = fp.read()
        writer.add_document(title=path.split("\\")[1], path=path, content=text, textdata=text)
        fp.close()
    print("Almost done")
    writer.commit()
    print("Done")
