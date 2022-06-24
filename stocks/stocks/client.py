import datetime
import hashlib
from yfinance import Ticker
from stocks.stocks.model import StockQuote


def run(ticker_list: list):

    for t in ticker_list:
        ticker: Ticker = Ticker(t)
        detail: dict = ticker.info

        quote: StockQuote = StockQuote(
            updated_on=datetime.datetime.utcnow(),
            symbol=detail.get('symbol'),
            short_name=detail.get('short_name'),
            regularMarketPrice=detail.get('regularMarketPrice')
        )

        quote.meta.id = hashlib.sha256(quote.updated_on.isoformat()).hexdigest()
        quote.save()
