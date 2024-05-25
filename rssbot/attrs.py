# This file is placed in the Public Domain.


"attributes"



from .object import Default, update
from .utils  import spl
 

class Parser:

    "Parser"

    @staticmethod
    def getnames(line):
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
    def parse(txt, toke="outline", items=None):
        "parse on outlines."
        if items is None:
            items = ",".join(Parser.getnames(txt))
        result = []
        for attrs in Parser.getattrs(txt, toke):
            if not attrs:
                continue
            obj = Default()
            for itm in spl(items):
                if itm == "link":
                    itm = "href"
                val = Parser.getvalue(attrs, itm)
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
        