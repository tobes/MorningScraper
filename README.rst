MorningScraper:  Simple scraper for morningstar.co.uk
=====================================================

A quick and dirty web page scraper for `morningstar.co.uk <http://morningstar.co.uk>`_.

Some stocks are updated via javascript and so the information is not available by just scraping the html.


**funds** are best referenced by ISIN e.g.

``'GB00B54RK123'`` - CF Odey Opus I Acc

``'LU1023728089'`` - Moorea Fd Euro Fixed Income IE

**stocks** are best referenced by name and exchange e.g.

``'LLOY LSE'`` - Lloyds Banking Group PLC

``'GOOG NASDAQ'`` - Google Inc Class C Capital Stock




functions
^^^^^^^^^

morningscraper.\ **search(ref, verbose=False)**

Search morningstar.co.uk for ref

If ref is found and is a fund or stock return details

*Args*:
    ref (str): search term can be ISIN or search term

    verbose (bool): provide output

*Returns*:
    list of dicts: containing info

    .. code ::

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



morningscraper.\ **get_data(ref, verbose=False)**

Search morningstar.co.uk for ref

If ref is found return details for each fund/stock

*Args*:
    ref (str): search term can be ISIN or search term

    verbose (bool): provide output

*Returns*:
    list of dicts: containing info:

    .. code::

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



morningscraper.\ **get_url(url, verbose=False)**

open morningstar.co.uk url and return details

*Args*:
    url (str): url to parse

    verbose (bool): provide output

*Returns*:
    dict: containing info:

    .. code::

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
