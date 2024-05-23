# This file is placed in the Public Domain.


"parsing"


import html
import re


from .object import Default
from .run    import spl


class Parser:

    "Parser"

    @staticmethod
    def getitem(line, item):
        "match items."
        lne = ''
        index1 = line.find(f'<{item}>')
        if index1 == -1:
            return lne
        index1 += len(item) + 2
        index2 = line.find(f'</{item}>', index1)
        if index2 == -1:
            return lne
        lne = line[index1:index2]
        if 'CDATA' in lne:
            lne = lne.replace('![CDATA[', '')
            lne = lne.replace(']]', '')
            lne = lne[1:-1]
        return lne.strip()

    @staticmethod
    def getitems(text, token):
        "loop for items."
        index = 0
        result = []
        stop = False
        while not stop:
            index1 = text.find(f'<{token}', index)
            if index1 == -1:
                break
            index1 += len(token) + 2
            index2 = text.find(f'</{token}>', index1)
            if index2 == -1:
                break
            lne = text[index1:index2]
            result.append(lne)
            index = index2
        return result

    @staticmethod
    def parse(txt, toke="item", items='title,link'):
        "parse a text for tokens."
        result = []
        for line in Parser.getitems(txt, toke):
            line = line.strip()
            obj = Default()
            for itm in spl(items):
                val = Parser.getitem(line, itm)
                if val:
                    val = unescape(val.strip())
                    val = val.replace("\n", "")
                    val = striphtml(val)
                    setattr(obj, itm, val)
            result.append(obj)
        return result


class OPMLParser:

    @staticmethod
    def getvalue(line, attr):
        "retrieve attribute value."
        lne = ''
        index1 = line.find(f'{attr}="')
        if index1 == -1:
            return lne
        index1 += len(attr) + 2
        index2 = line.find('"', index1)
        if index2 == -1:
            index2 = line.find('/>', index1)
        if index2 == -1:
            return lne
        lne = line[index1:index2]
        if 'CDATA' in lne:
            lne = lne.replace('![CDATA[', '')
            lne = lne.replace(']]', '')
            #lne = lne[1:-1]
        return lne

    @staticmethod
    def getattrs(line, token):
        "split for attributes."
        index = 0
        result = []
        stop = False
        while not stop:
            index1 = line.find(f'<{token} ', index)
            if index1 == -1:
                return result
            index1 += len(token) + 2
            index2 = line.find('/>', index1)
            if index2 == -1:
                return result
            result.append(line[index1:index2])
            index = index2
        return result

    @staticmethod
    def parse(txt, toke="outline", items="xmlUrl"):
        result = []
        for attrs in OPMLParser.getattrs(txt, toke):
            if not attrs:
                continue
            obj = Default()
            for itm in spl(items):
                if itm == "link":
                    itm = "href"
                val = OPMLParser.getvalue(attrs, itm)
                if not val:
                    continue
                if itm == "href":
                    itm = "link"
                setattr(obj, itm, val.strip())
            result.append(obj)
        return result


def striphtml(text):
    "strip html."
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


def unescape(text):
    "unescape text."
    txt = re.sub(r'\s+', ' ', text)
    return html.unescape(txt)
