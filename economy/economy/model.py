from datetime import datetime

from elasticsearch_dsl import Document, Keyword, ScaledFloat, Date, InnerDoc, Object


class StockQuote(Document):
    """
    Model for stock quote

    Attributes
    ----------
    updated_on:
    symbol:
    short_name:
    regularMarketPrice:
    """
    updated_on = Date()
    symbol = Keyword()
    short_name = Keyword()
    regular_market_price = ScaledFloat(100)

    def save(self, **kwargs):
        # override the index to go to the proper timeslot
        kwargs['index'] = datetime.now().strftime('stock-quote-%Y')
        return super().save(**kwargs)


class Indicator(InnerDoc):
    """

    """
    id = Keyword()
    value = Keyword()


class WorldBank(Document):
    """

    """
    updated_on = Date()
    countryiso3code = Keyword()
    indicator = Object(Indicator)
    date = Date()
    value = ScaledFloat(100)

    def save(self, **kwargs):
        # override the index to go to the proper timeslot
        kwargs['index'] = datetime.now().strftime('world-bank-%Y')
        return super().save(**kwargs)
