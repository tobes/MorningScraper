import sys
import re

from decimal import Decimal
from datetime import datetime

from bs4 import BeautifulSoup


if sys.version_info[0] == 3:
    from urllib.request import urlopen
    from urllib.parse import quote, urlsplit
elif sys.version_info[0] == 2:
    from urllib import urlopen, quote
    from urlparse import urlsplit
else:
    raise Exception('Python version 2 or 3 required')

SITE = 'morningstar.co.uk'
SITE_BASE = 'http://www.' + SITE
SEARCH_BASE = SITE_BASE + '/uk/funds/SecuritySearchResults.aspx?search=%s'


def dmy_2_date(value):
    ''' Convert dd/mm/yyyy date string into python date '''
    return datetime.strptime(value, '%d/%m/%Y').date()


def fix_url(url):
    ''' Fully qualify url if domain missing '''
    if url.startswith('/'):
        url = SITE_BASE + url
    return url


def search(ref, verbose=False):
    ''' Search morningstar.co.uk for ref
        If ref is found and is a fund or stock return details

        Args:
            ref (str): search term can be ISIN or search term
            verbose (bool): provide output

        Returns:
            list of dicts: containing info::
                dict for stock:
                {
                    'name': (str) name of stock
                    'url': (str) url for stock info
                    'type': (str) 'Stock'
                    'ticker': (str) ticker name
                    'currency': (str) currency code of stock
                }

                dict for fund:
                {
                    'name': (str) name of fund
                    'url': (str) url for fund info
                    'type': (str) 'Fund'
                    'ISIN': (str) ISIN of fund
                }
    '''

    if verbose:
        print('Search for: %s' % ref)
    data = urlopen(SEARCH_BASE % quote(ref)).read()
    parsed_html = BeautifulSoup(data)
    results = []
    stocks = parsed_html.find_all(
        'table', id='ctl00_MainContent_stockTable'
    )
    if stocks:
        stocks = stocks[0].find_all('tr')[1:]
        for stock in stocks:
            results.append({
                'name': stock.td.text,
                'url': fix_url(stock.td.a.get('href')),
                'type': 'Stock',
                'ticker': stock.find_all('td', class_='searchTicker')[0].text,
                'currency': stock.find_all(
                    'td', class_='searchCurrency'
                )[0].text,
            })
    funds = parsed_html.find_all(
        'table', id='ctl00_MainContent_fundTable'
    )
    if funds:
        funds = funds[0].find_all('tr')[1:]
        for fund in funds:
            data = fund.find_all('td')
            results.append({
                'name': data[0].text,
                'url': fix_url(data[0].a.get('href')),
                'type': 'Fund',
                'ISIN': data[1].text,
            })

    if verbose:
        if results:
            print('%s item(s) found.' % len(results))
            for item in results:
                print('\t%s\t%s' % (item['type'], item['name']))
        else:
            print('No items found.')
    return results


def get_data(ref, verbose=False):
    ''' Search morningstar.co.uk for ref
        If ref is found return details for each fund/stock

        Args:
            ref (str): search term can be ISIN or search term
            verbose (bool): provide output

        Returns:
            list of dicts: containing info::
                [{
                    'name': (str) name of the fund/stock
                    'ISIN': (str) ISIN reference for the fund/stock
                    'date': (Date) date of valuation
                    'value': (Decimal) value of the fund/stock
                    'currency': (str) currency e.g. GBP USD
                    'change': (str) percent change, including %
                    'type': (str) e.g. Fund Stock
                    'url': (str) fully qualified url info gathered from
                }, ...]
    '''
    results = search(ref, verbose=verbose)
    output = []
    for item in results:
        data = get_url(item['url'], verbose=verbose)
        if data:
            output.append(data)
    return output


def get_url(url, verbose=False):
    ''' open morningstar.co.uk url and return details

        Args:
            url (str): url to parse
            verbose (bool): provide output

        Returns:
            dict: containing info::
                {
                    'name': (str) name of the fund/stock
                    'ISIN': (str) ISIN reference for the fund/stock
                    'date': (Date) date of valuation
                    'value': (Decimal) value of the fund/stock
                    'currency': (str) currency e.g. GBP USD
                    'change': (str) percent change, including %
                    'type': (str) e.g. Fund Stock
                    'url': (str) fully qualified url info gathered from
                }
    '''
    if verbose:
        print('\nOpening %s' % url)
    if not urlsplit(url).netloc.endswith(SITE):
        raise Exception('Non morningstar.co.uk url %r' % url)
    result = None
    if '/uk/funds/snapshot/snapshot' in url:
        try:
            result = _get_funds(url)
        except:
            result = None
    elif '/uk/stockreport/' in url:
        try:
            result = _get_stock(url)
        except:
            result = None
    else:
        raise Exception('Unrecognised url %r' % url)
    if verbose:
        print(result)
    return result


def _get_funds(url):
    ''' Get and parse returned html for fund pages e.g.
        http://www.morningstar.co.uk/uk/funds/snapshot/snapshot.aspx?id=F00000NGEH
    '''
    data = urlopen(url).read()
    parsed_html = BeautifulSoup(data)
    title = parsed_html.find_all('div', class_='snapshotTitleBox')[0].h1.text
    table = parsed_html.find_all('table', class_='overviewKeyStatsTable')[0]
    for tr in table.find_all('tr'):
        tds = tr.find_all('td')
        if len(tds) != 3:
            continue
        if tds[0].text.startswith('NAV'):
            date = tds[0].span.text
            (currency, value) = tds[2].text.split()
        if tds[0].text.startswith('Day Change'):
            change = tds[2].text.strip()
        if tds[0].text.startswith('ISIN'):
            isin = tds[2].text.strip()
    return {
        'title': title,
        'value': Decimal(value),
        'currency': currency,
        'change': change,
        'date': dmy_2_date(date),
        'url': url,
        'ISIN': isin,
        'type': 'Fund',
    }


def _get_stock(url):
    ''' Get and parse returned html for stock pages e.g.
        http://tools.morningstar.co.uk/uk/stockreport/default.aspx?SecurityToken=0P000090RG]3]0]E0WWE$$ALL
    '''
    data = urlopen(url).read()
    parsed_html = BeautifulSoup(data)
    title = parsed_html.find_all('span', class_='securityName')[0].text
    value = parsed_html.find_all('span', id='Col0Price')[0].text
    change = parsed_html.find_all('span', id='Col0PriceDetail')[0].text
    change = change.split('|')[1].strip()
    date = parsed_html.find_all('p',  id='Col0PriceTime')[0].text[6:16]
    currency = parsed_html.find_all('p',  id='Col0PriceTime')[0].text
    currency = re.search(r'\|\s([A-Z]{3,4})\b', currency).group(1)
    isin = parsed_html.find_all('td',  id='Col0Isin')[0].text
    return {
        'title': title,
        'value': Decimal(value),
        'currency': currency,
        'change': change,
        'date': dmy_2_date(date),
        'url': url,
        'ISIN': isin,
        'type': 'Stock',
    }


if __name__ == '__main__':
    get_data('GB00B54RK123', verbose=True)
    get_data('LLOY LSE', verbose=True)
    get_data('GOOG NASDAQ', verbose=True)
    get_data('LU1023728089', verbose=True)
