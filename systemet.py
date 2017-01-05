#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import urllib
import json
import sys

try:
    from sopel import module
    from sopel import formatting
except:
    module = None
    formatting = None

def output(bot, out):
    if bot is not None:
        bot.say(out)
    else:
        print(out)

def runMe(bot, tickers):
    if not tickers:
        output(bot, "No arguments passed")
        return

    tickers = tickers.split(',')
    totalPercentage = []

    url = "http://systemetapi.se/product?"

    for ticker in tickers:
        if int(sys.version[0]) == 2:
            ticker = ticker.encode('utf-8')

        ticker = ticker.replace(' ', '%')	
        searchString = '%{0}%'.format(ticker)
        q = {
            'name': searchString,
            'order_by': 'apk',
            'order': 'DESC'
        }
        if int(sys.version[0]) == 2:
            da = urllib.urlencode(q)
        elif int(sys.version[0]) > 2:
            da = urllib.parse.urlencode(q)
        query = url + da
        result = requests.get(query)
        content = result.content
        if int(sys.version[0]) > 2:
            content = content.decode('UTF-8')
        dic = json.loads(content)

        #max results 5 and real
        existdic = []
        for r in dic:
            systemeturl = 'http://www.systembolaget.se/{0}'.format(r.get('product_number'))
            if int(sys.version[0]) == 2:
                a = urllib.urlopen(systemeturl)
            elif int(sys.version[0]) > 2:
                try:
                    a = urllib.request.urlopen(systemeturl)
                except:
                    a = None

            if a and a.getcode() != 404:
                existdic.append((r, systemeturl))

        numresults = len(existdic)
        if numresults == 0:
            rsu = u'Found no products'
            output(bot, rsu)
            continue

        rsu = u'Found {0} products, showing 5'.format(numresults)
        output(bot, rsu)
        existdic = existdic[:5]
        for r, url in existdic:
            tags = [t.get('name').title() for t in r.get('tags')]
            out = u'{0} ({1})'.format(r.get('name'), r.get('product_number'))
            if formatting:
                out = formatting.bold(out)
            out += u' - {0}'.format(', '.join(tags))
            out += u' - {0} kr'.format(r.get('price'))
            out += u' - {0} liter'.format(r.get('volume'))
            out += u' - {0} apk'.format(r.get('apk'))
            out += u' - {0}'.format(url)
            output(bot, out)


try:
    @module.commands('systemet')
    def yf(bot, trigger):
        tickers = trigger.group(2)
        runMe(bot, tickers)

except:
    #module not available
    pass

def test():
    tickers = 'smirnoff gold,triple'
    tickers = 'sofiero'
    tickers = u'åbro'
    tickers = 'Campo Viejo'
    runMe(None, tickers)

if __name__ == "__main__":
    test()
