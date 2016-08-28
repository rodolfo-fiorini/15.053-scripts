__author__ = 'rodolfob'

import urllib2
import pandas.io.data as web
import datetime

from bs4 import BeautifulSoup

site = "http://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

#returns a dictionary with company ticker as "values" matched to their Global Industry Classification Standard, or GICS, or industry "key"
def scrape_dict(site):
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = urllib2.Request(site, headers=hdr)
    response = urllib2.urlopen(req)
    soup = BeautifulSoup(response, "html.parser")
    table = soup.find("table", {"class": "wikitable sortable"})

    sector_tickers= dict()
    for row in table.findAll('tr'):
        col = row.findAll('td')
        if len(col) > 0:
            sector = str(col[3].string.strip()).lower().replace(' ', '_')
            ticker = str(col[0].string.strip())
            if sector not in sector_tickers:
                sector_tickers[sector] = list()
            sector_tickers[sector].append(ticker)
    return sector_tickers
sector_tickers = scrape_dict(site)

#meshes ticker values into one array of S&P500 tickers
tickers = []
for sector, ticker_array in sector_tickers.iteritems():
    for ticker in ticker_array:
        tickers.append(ticker)

#makes sure that there are no repeating tickers, there are 505 tickers
uniq = []
seen = set()
for ticker in tickers:
    if ticker not in seen:
        uniq.append(ticker)
        seen.add(ticker)

#sort ticker array alphabetically
tickers.sort()

#An HDF5 file is a container for two kinds of objects: datasests, which are array-like collections of data, and groups, which are folder-like
#containers that hold datasets and other groups ---- ****Groups work like dictionaries, and datasets work like NumPy arrays


start = datetime.datetime(2005,1,1)
end = datetime.datetime(2015,1,1)

failures = ["ABBV", "ALLE", "CFG", "CSRA", "FTV", "HPE", "KHC", "MNK", "NAVI", "NEE", "NWS", "NWSA", "PYPL", "QRVO", "SYF", "UA-C", "WLTW", "WRK", "ZTS"]
for i in failures:
    tickers.remove(i)

print tickers
closing_prices = []
#for ticker in tickers[0:10]:
ticker_data = web.DataReader(tickers, 'yahoo', start, end)
#closing_prices.append(ticker_data["Close"])
#print closing_prices

ticker_data["Close"].to_csv("snp500data.csv")