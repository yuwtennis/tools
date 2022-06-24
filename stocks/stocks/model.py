from elasticsearch_dsl import Document, Keyword, ScaledFloat, Date


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
    regularMarketPrice = ScaledFloat(100)
