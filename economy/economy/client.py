import os

import logging
from datetime import datetime
from typing import Generator

import requests
import hashlib
from elasticsearch_dsl.connections import connections
from yfinance import Ticker
from economy.persistence import persist
from economy.model import WorldBank, StockQuote

logger = logging.getLogger(__name__)

def run(ticker_list: list, indicator_list: list):
    """
    Crawl yahoo finance and send to elasticsearch

    Parameters
    ----------
    indicator_list
    ticker_list: list
        List of tickers to crawl

    Returns
    -------
    None

    """
    connections.create_connection(
        hosts=[os.getenv('ES_HOST', 'localhost')],
        sniff_on_start=True)

    persist(
        iter_ticker(ticker_list),
        os.getenv('BACKEND_TYPE', 'stdout'))
    persist(
        iter_world_bank(indicator_list),
        os.getenv('BACKEND_TYPE', 'stdout'))


def iter_ticker(ticker_list: list) -> Generator:
    """

    Parameters
    ----------
    ticker_list

    Returns
    -------

    """
    for t in ticker_list:
        logger.info('Crawling %s...', t)
        ticker: Ticker = Ticker(t)
        detail: dict = ticker.info
        quote: StockQuote = StockQuote(
            updated_on=datetime.utcnow(),
            symbol=detail.get('symbol'),
            short_name=detail.get('short_name'),
            regular_market_price=detail.get('regularMarketPrice')
        )

        quote.meta.id = hashlib.sha256(quote.updated_on.isoformat().encode()).hexdigest()

        yield quote


def iter_world_bank(indicator_list: list) -> Generator:
    """

    Parameters
    ----------
    indicator_list

    Returns
    -------

    """
    for c in ['jpn']:
        curr_year: int = int(datetime.now().year)
        for i in indicator_list:
            logger.info('Crawling %s in %s...', i, c)
            url: str = f'http://api.worldbank.org/v2/country/{c}/indicators/{i}'
            r = requests.get(url, params={
                'date': f'{curr_year-10}:{curr_year}', 'format': 'json'})
            for detail in r.json()[1]:
                wb: WorldBank = WorldBank(
                    updated_on=datetime.utcnow(),
                    date=detail.get('date'),
                    countryiso3code=detail.get('countryiso3code'),
                    indicator=detail.get('indicator'),
                    value=detail.get('value')
                )
                wb.meta.id = hashlib.sha256(f"{wb.date}_{wb.indicator}".encode()).hexdigest()
                yield wb
