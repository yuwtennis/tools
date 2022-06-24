from elasticsearch_dsl import Document, Keyword, ScaledFloat, Date


class StockQuote(Document):

    updated_on = Date()
    symbol = Keyword()
    short_name = Keyword()
    regularMarketPrice = ScaledFloat(100)
