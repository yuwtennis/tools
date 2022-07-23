import os

import logging
from datetime import datetime, timezone
from typing import Generator

import requests
import hashlib
from elasticsearch_dsl.connections import connections
from yfinance import Ticker
from economy.persistence import persist
from economy.model import WorldBank, StockQuote

logger = logging.getLogger(__name__)


def run(config: dict):
    """
    Crawl yahoo finance and send to elasticsearch

    Parameters
    ----------
    config: dict
        includes list of keys to crawl

    Returns
    -------
    None

    """
    connections.create_connection(hosts=[os.getenv('ES_HOST', 'localhost')], sniff_on_start=True)

    persist(list(iter_ticker(config.get('tickers'))), os.getenv('BACKEND_TYPE', 'stdout'))
    persist(
        list(iter_world_bank(
            config.get('indicators'),
            int(os.getenv('WB_FROM_YEAR')))),
        os.getenv('BACKEND_TYPE', 'stdout'))


def iter_ticker(ticker_list: list) -> Generator:
    """

    Parameters
    ----------
    ticker_list

    Returns
    -------
    Generator

    """
    for t in ticker_list:
        logger.info('Crawling %s...', t)
        ticker: Ticker = Ticker(t)
        detail: dict = ticker.info
        quote: StockQuote = StockQuote(updated_on=datetime.utcnow(), **detail)
        quote.meta.id = hashlib.sha256(quote.updated_on.isoformat().encode()).hexdigest()

        yield quote


def iter_world_bank(indicator_list: list, from_year: int) -> Generator:
    """

    Parameters
    ----------
    from_year
    indicator_list

    Returns
    -------
    Generator

    """
    for c in ['jpn']:
        curr_year: int = int(datetime.now().year)
        for i in indicator_list:
            logger.info('Crawling %s in %s...', i, c)
            url: str = f'http://api.worldbank.org/v2/country/{c}/indicators/{i}'
            r = requests.get(url, params={
                'date': f'{curr_year-from_year}:{curr_year}', 'format': 'json'})
            for detail in r.json()[1]:
                wb: WorldBank = WorldBank(updated_on=datetime.utcnow(), **detail)
                # Overwrite with beginning of month
                wb.date = datetime(year=int(wb.date), month=1, day=1, tzinfo=timezone.utc)
                wb.meta.id = hashlib.sha256(f"{wb.date}_{wb.indicator}".encode()).hexdigest()
                yield wb
