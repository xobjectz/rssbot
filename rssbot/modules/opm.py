# This file is placed in the Public Domain.


"outline processor markup language"


from ..disk   import sync
from ..find   import find
from ..object import construct


from .rss import Rss, Parser


TEMPLATE = """<opml version="1.0">
    <head>
        <title>rssbot opml</title>
    </head>
    <body>
        <outline title="rssbot opml" text="24/7 feed fetcher">"""



def exp(event):
    "export to opml."
    event.reply(TEMPLATE)
    nrs = 0
    for _fn, obj in find("rss"):
        nrs += 1
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
    with open(fnm, "r") as file:
        txt = file.read()
    prs = Parser()
    nrs = 0
    for o in prs.parse(txt, 'outline', "name,display_list,xmlUrl"):
        nrs += 1
        if o.xmlUrl and find("rss", o):
            event.reply(f"skipping %{nrs} url is already there.")
            continue
        rss = Rss()
        construct(rss, o)
        sync(rss)
        event.reply(o)
