import os

import logging

from elasticsearch_dsl.connections import connections
from yfinance import Ticker
from stocks.persistence import persist


def run(ticker_list: list):
    """
    Crawl yahoo finance and send to elasticsearch

    Parameters
    ----------
    ticker_list: list
        List of tickers to crawl

    Returns
    -------
    None

    """
    connections.create_connection(
        hosts=[os.getenv('ES_HOST', 'localhost')],
        sniff_on_start=True)

    for t in ticker_list:
        logging.info('Crawling %s...', t)
        ticker: Ticker = Ticker(t)
        detail: dict = ticker.info
        persist(detail, os.getenv('BACKEND_TYPE', 'stdout'))
