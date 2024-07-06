from datetime import datetime

from elasticsearch_dsl import Document, Keyword, ScaledFloat, Date, InnerDoc, Object


class StockQuote(Document):
    """
    Model for stock quote

    Attributes
    ----------
    updated_on:
    """
    updated_on = Date()

    def save(self, **kwargs):
        # override the index to go to the proper timeslot
        kwargs['index'] = datetime.now().strftime('stock-quote-%Y')
        return super().save(**kwargs)


class WorldBank(Document):
    """

    """
    updated_on = Date()
    obs_status = Keyword()
    unit = Keyword()

    def save(self, **kwargs):
        # override the index to go to the proper timeslot
        kwargs['index'] = datetime.now().strftime('world-bank-%Y')
        return super().save(**kwargs)
