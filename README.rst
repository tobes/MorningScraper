MorningScraper:
===============

Simple scraper for morningstar.co.uk

A quick and dirty web page scraper for `morningstar.co.uk <http://morningstar.co.uk>`_.

.. warning:: Some stocks are updated via javascript and so the information is not available by just scraping the html.


**funds** are best referenced by ISIN e.g.

``'GB00B54RK123'`` - CF Odey Opus I Acc

``'LU1023728089'`` - Moorea Fd Euro Fixed Income IE

**stocks** are best referenced by name and exchange e.g.

``'LLOY LSE'`` - Lloyds Banking Group PLC

``'GOOG NASDAQ'`` - Google Inc Class C Capital Stock


Installation
^^^^^^^^^^^^

.. code::

    pip install MorningScraper
