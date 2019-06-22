import os
import re
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from whoosh.fields import Schema, TEXT, ID, DATETIME
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
    ix.close()
    print("Done")


def createSearchableDatafromUrl():
    url = "https://wanderinginn.com/2016/07/27/1-00/"
    if not os.path.exists("indexdir"):
        os.mkdir("indexdir")
    schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT(stored=True),
                    textdata=TEXT(stored=True), date=DATETIME, url=ID(stored=True), wordcount=TEXT)
    ix = create_in("indexdir", schema)
    writer = ix.writer()
    while True:
        currentPage = requests.get(url)
        soup = BeautifulSoup(currentPage.content, "lxml")
        body = soup.find("div", {"class": "entry-content"})
        title = soup.find("h1", {"class": "entry-title"})
        p_date = soup.find("time", {"class": "entry-date"})
        p_date_converted = datetime.strptime(p_date['datetime'], '%Y-%m-%dT%H:%M:%S+00:00')

        url_list = body.find_all('a')
        print(title.text)
        count = len(re.findall(r'\w+', body.text))
        writer.add_document(title=title.text, content=body.text, textdata=body.text, date=p_date_converted, url=url,
                            wordcount=count)
        print(url)
        try:
            url = url_list[-1].get('href')
        except:
            writer.commit()
            break
