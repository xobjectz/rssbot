# This file is placed in the Public Domain.


"outline processor markup language"


from ..default import Default
from ..object  import construct, update
from ..run     import broker
from ..utils   import shortid, spl


from .rss import Rss


TEMPLATE = """<opml version="1.0">
    <head>
        <title>rssbot opml</title>
    </head>
    <body>
        <outline title="rssbot opml" text="24/7 feed fetcher">"""


class Parser:

    "Parser"

    @staticmethod
    def getnames(line):
        "return list of attribute names."
        return [x.split('="')[0]  for x in line.split()]

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
    def parse(txt, toke="outline", itemz=None):
        "parse on outlines."
        if itemz is None:
            itemz = ",".join(Parser.getnames(txt))
        result = []
        for attrz in Parser.getattrs(txt, toke):
            if not attrz:
                continue
            obj = Default()
            for itm in spl(itemz):
                if itm == "link":
                    itm = "href"
                val = Parser.getvalue(attrz, itm)
                if not val:
                    continue
                if itm == "href":
                    itm = "link"
                setattr(obj, itm, val.strip())
            result.append(obj)
        return result


def attrs(obj, txt):
    "parse attributes into the object."
    update(obj, Parser.parse(txt))


def exp(event):
    "export to opml."
    event.reply(TEMPLATE)
    nrs = 0
    for _fn, objr in broker.all("rss"):
        nrs += 1
        obj = Default()
        update(obj, objr)
        name = obj.name or f"url{nrs}"
        txt = f'<outline name="{name}" display_list="{obj.display_list}" xmlUrl="{obj.rss}"/>'
        event.reply(" "*12 + txt)
    event.reply(" "*8 + "</outline>")
    event.reply("    <body>")
    event.reply("</opml>")


def imp(event):
    "import opml."
    if not event.args:
        event.reply("imp <filename>")
        return
    fnm = event.args[0]
    with open(fnm, "r", encoding="utf-8") as file:
        txt = file.read()
    prs = Parser()
    nrs = 0
    insertid = shortid()
    for obj in prs.parse(txt, 'outline', "name,display_list,xmlUrl"):
        #if obj.xmlUrl and broker.find({"rss": obj.xmlUrl}):
        #    event.reply(f"skipping {obj.xmlUrl}")
        #    continue
        rss = Rss()
        construct(rss, obj)
        rss.rss = rss.xmlUrl
        rss.insertid = insertid
        broker.add(rss)
        nrs += 1
    if nrs:
        event.reply(f"added {nrs} urls.")
        