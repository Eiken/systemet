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

        numresults = len(dic)
        if numresults == 0:
            rsu = u'Found no products'
            output(bot, rsu)
            continue

        rsu = u'Found {0} products, showing 5'.format(numresults)
        output(bot, rsu)

        #max results 5
        dic = dic[:5]
        for r in dic:          
            out = u'{0} ({1})'.format(r.get('name'), r.get('product_number')).ljust(30)
            out += u' - {0} kr'.format(r.get('price')).ljust(10)
            out += u' - apk: {0}'.format(r.get('apk'))
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
