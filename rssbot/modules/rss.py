# This file is placed in the Public Domain.
#
# pylint: disable=C,R,W0201,W0612,E0402


"rich site syndicate"


import html.parser
import re
import time
import urllib
import urllib.request
import _thread


from urllib.error import HTTPError, URLError
from urllib.parse import quote_plus, urlencode


from ..brokers import Broker
from ..default import Default
from ..locates import find, last
from ..objects import Object, fmt, update
from ..parsers import laps
from ..persist import sync
from ..repeats import Repeater
from ..utility import fntime
from ..threads import launch


def init():
    fetcher = Fetcher()
    fetcher.start()
    return fetcher


DEBUG = False


fetchlock = _thread.allocate_lock()


class Feed(Default):

    pass


class Rss(Default):

    def __init__(self):
        Default.__init__(self)
        self.display_list = 'title,link,author'


class Seen(Default):

    def __init__(self):
        Default.__init__(self)
        self.urls = []


class Fetcher(Object):

    def __init__(self):
        self.dosave = False
        self.seen = Seen()
        self.seenfn = None

    @staticmethod
    def display(obj):
        result = ''
        displaylist = []
        try:
            displaylist = obj.display_list or 'title,link'
        except AttributeError:
            displaylist = 'title,link,author'
        for key in displaylist.split(","):
            if not key:
                continue
            data = getattr(obj, key, None)
            if not data:
                continue
            data = data.replace('\n', ' ')
            data = striphtml(data.rstrip())
            data = unescape(data)
            result += data.rstrip()
            result += ' - '
        return result[:-2].rstrip()

    def fetch(self, feed):
        with fetchlock:
            counter = 0
            result = []
            for obj in reversed(list(getfeed(feed.rss, feed.display_list))):
                fed = Feed()
                update(fed, obj)
                update(fed, feed)
                if 'link' in fed:
                    url = urllib.parse.urlparse(fed.link)
                    if url.path and not url.path == '/':
                        uurl = f'{url.scheme}://{url.netloc}/{url.path}'
                    else:
                        uurl = fed.link
                    if uurl in self.seen.urls:
                        continue
                    self.seen.urls.append(uurl)
                counter += 1
                if self.dosave:
                    sync(fed)
                result.append(fed)
        if result:
            sync(self.seen, self.seenfn)
        txt = ''
        feedname = getattr(feed, 'name', None)
        if feedname:
            txt = f'[{feedname}] '
        for obj in result:
            txt2 = txt + self.display(obj)
            for bot in Broker.all():
                if "announce" in dir(bot):
                    bot.announce(txt2.rstrip())
        return counter

    def run(self):
        thrs = []
        for fnm, feed in find('rss'):
            thrs.append(launch(self.fetch, feed, name=f"{feed.rss}"))
        return thrs

    def start(self, repeat=True):
        self.seenfn = last(self.seen)
        if repeat:
            repeater = Repeater(300.0, self.run)
            repeater.start()


class Parser(Object):

    @staticmethod
    def getitem(line, item):
        lne = ''
        try:
            index1 = line.index(f'<{item}>') + len(item) + 2
            index2 = line.index(f'</{item}>')
            lne = line[index1:index2]
            if 'CDATA' in lne:
                lne = lne.replace('![CDATA[', '')
                lne = lne.replace(']]', '')
                lne = lne[1:-1]
        except ValueError:
            lne = None
        return lne

    @staticmethod
    def parse(txt, item='title,link'):
        result = []
        for line in txt.split('<item>'):
            line = line.strip()
            obj = Object()
            for itm in item.split(","):
                setattr(obj, itm, Parser.getitem(line, itm))
            result.append(obj)
        return result


class OPML(Parser):

    @staticmethod
    def getitem(line, item):
        lne = ''
        try:
            index1 = line.index(f"{item}") + len(item) + 2
            sub1 = line[index1:]
            lne = sub1.split('" ')[0][:-3]
        except ValueError:
            pass
        if 'CDATA' in lne:
            lne = lne.replace('![CDATA[', '')
            lne = lne.replace(']]', '')
            lne = lne[1:-1]
        return lne

    @staticmethod
    def parse(txt, item='title,text,xmlUrl'):
        result = []
        for line in txt.split("<outline "):
            line = line.strip()
            line = line[2:]
            obj = Object()
            for itm in item.split(","):
                lne = OPML.getitem(line, itm)
                setattr(obj, itm, lne)
            result.append(obj)
        return result


def getfeed(url, item):
    if DEBUG:
        return [Object(), Object()]
    try:
        result = geturl(url)
    except (ValueError, HTTPError, URLError):
        return [Object(), Object()]
    if not result:
        return [Object(), Object()]
    return Parser.parse(str(result.data, 'utf-8'), item)


def gettinyurl(url):
    postarray = [
        ('submit', 'submit'),
        ('url', url),
    ]
    postdata = urlencode(postarray, quote_via=quote_plus)
    req = urllib.request.Request('http://tinyurl.com/create.php',
                  data=bytes(postdata, 'UTF-8'))
    req.add_header('User-agent', useragent("rss fetcher"))
    with urllib.request.urlopen(req) as htm: # nosec
        for txt in htm.readlines():
            line = txt.decode('UTF-8').strip()
            i = re.search('data-clipboard-text="(.*?)"', line, re.M)
            if i:
                return i.groups()
    return []


def geturl(url):
    if not url.startswith("http://") and not url.startswith("https://"):
        return ""
    url = urllib.parse.urlunparse(urllib.parse.urlparse(url))
    req = urllib.request.Request(url)
    req.add_header('User-agent', useragent("rss fetcher"))
    with urllib.request.urlopen(req) as response: # nosec
        response.data = response.read()
        return response


def striphtml(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


def unescape(text):
    txt = re.sub(r'\s+', ' ', text)
    return html.unescape(txt)


def useragent(txt):
    return 'Mozilla/5.0 (X11; Linux x86_64) ' + txt


def dpl(event):
    if len(event.args) < 2:
        event.reply('dpl <stringinurl> <item1,item2>')
        return
    setter = {'display_list': event.args[1]}
    for fnm, feed in find('rss', {'rss': event.args[0]}):
        if feed:
            update(feed, setter)
            sync(feed)
    event.reply('ok')


def nme(event):
    if len(event.args) != 2:
        event.reply('nme <stringinurl> <name>')
        return
    selector = {'rss': event.args[0]}
    for fnm, feed in find('rss', selector):
        if feed:
            feed.name = event.args[1]
            sync(feed)
    event.reply('ok')


def opm(event):
    result = OPML.parse(TXT)
    for obj in result:
        event.reply(f"{obj.title} {obj.xmlUrl}")


def rem(event):
    if len(event.args) != 1:
        event.reply('rem <stringinurl>')
        return
    selector = {'rss': event.args[0]}
    for fnm, feed in find('rss', selector):
        if feed:
            feed.__deleted__ = True
            sync(feed, fnm)
    event.reply('ok')


def res(event):
    if len(event.args) != 1:
        event.reply('res <stringinurl>')
        return
    selector = {'rss': event.args[0]}
    for fnm, feed in find('rss', selector, deleted=True):
        if feed:
            feed.__deleted__ = False
            sync(feed, fnm)
    event.reply('ok')


def rss(event):
    if not event.rest:
        nrs = 0
        for fnm, feed in find('rss'):
            nrs += 1
            elp = laps(time.time()-fntime(fnm))
            txt = fmt(feed)
            event.reply(f'{nrs} {txt} {elp}')
        if not nrs:
            event.reply('no rss feed found.')
        return
    url = event.args[0]
    if 'http' not in url:
        event.reply('i need an url')
        return
    for fnm, result in find('rss', {'rss': url}):
        if result:
            event.reply(f'already got {url}')
            return
    feed = Rss()
    feed.rss = event.args[0]
    sync(feed)
    event.reply('ok')


TXT = """<opml version="1.0">
    <head>
        <title>Sample OPML file for RSSReader</title>
    </head>
    <body>
        <outline title="News" text="News">
            <outline text="Big News Finland" title="Big News Finland" type="rss" xmlUrl="http://www.bignewsnetwork.com/?rss=37e8860164ce009a"/>
            <outline text="Euronews" title="Euronews" type="rss" xmlUrl="http://feeds.feedburner.com/euronews/en/news/"/>
            <outline text="Reuters Top News" title="Reuters Top News" type="rss" xmlUrl="http://feeds.reuters.com/reuters/topNews"/>
            <outline text="Yahoo Europe" title="Yahoo Europe" type="rss" xmlUrl="http://rss.news.yahoo.com/rss/europe"/>
        </outline>

        <outline title="Leisure" text="Leisure">
            <outline text="CNN Entertainment" title="CNN Entertainment" type="rss" xmlUrl="http://rss.cnn.com/rss/edition_entertainment.rss"/>
            <outline text="E! News" title="E! News" type="rss" xmlUrl="http://uk.eonline.com/syndication/feeds/rssfeeds/topstories.xml"/>
            <outline text="Hollywood Reporter" title="Hollywood Reporter" type="rss" xmlUrl="http://feeds.feedburner.com/thr/news"/>
            <outline text="Reuters Entertainment" title="Reuters Entertainment" type="rss"  xmlUrl="http://feeds.reuters.com/reuters/entertainment"/>
            <outline text="Reuters Music News" title="Reuters Music News" type="rss" xmlUrl="http://feeds.reuters.com/reuters/musicNews"/>
            <outline text="Yahoo Entertainment" title="Yahoo Entertainment" type="rss" xmlUrl="http://rss.news.yahoo.com/rss/entertainment"/>
        </outline>

        <outline title="Sports" text="Sports">
            <outline text="Formula 1" title="Formula 1" type="rss" xmlUrl="http://www.formula1.com/rss/news/latest.rss"/>
            <outline text="MotoGP" title="MotoGP" type="rss" xmlUrl="http://rss.crash.net/crash_motogp.xml"/>
            <outline text="N.Y.Times Track And Field" title="N.Y.Times Track And Field" type="rss" xmlUrl="http://topics.nytimes.com/topics/reference/timestopics/subjects/t/track_and_field/index.html?rss=1"/>
            <outline text="Reuters Sports" title="Reuters Sports" type="rss" xmlUrl="http://feeds.reuters.com/reuters/sportsNews"/>
            <outline text="Yahoo Sports NHL" title="Yahoo Sports NHL" type="rss" xmlUrl="http://sports.yahoo.com/nhl/rss.xml"/>
            <outline text="Yahoo Sports" title="Yahoo Sports" type="rss" xmlUrl="http://rss.news.yahoo.com/rss/sports"/>
        </outline>

        <outline title="Tech" text="Tech">
            <outline text="Coding Horror" title="Coding Horror" type="rss" xmlUrl="http://feeds.feedburner.com/codinghorror/"/>
            <outline text="Gadget Lab" title="Gadget Lab" type="rss" xmlUrl="http://www.wired.com/gadgetlab/feed/"/>
            <outline text="Gizmodo" title="Gizmodo" type="rss" xmlUrl="http://gizmodo.com/index.xml"/>
            <outline text="Reuters Technology" title="Reuters Technology" type="rss" xmlUrl="http://feeds.reuters.com/reuters/technologyNews"/>
        </outline>
    </body>
</opml>
"""
