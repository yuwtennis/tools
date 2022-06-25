import hashlib
import importlib
import pprint
from abc import ABCMeta, abstractmethod
from datetime import datetime
from stocks.model import StockQuote


def persist(quote: dict, backend_type: str):
    """
    interface when persisting to backend

    Parameters
    ----------
    quote: str
    backend_type: str

    Raises
    ------
    ValueError

    """
    module: object = importlib.import_module('stocks.persistence')
    obj: Backends = getattr(module, backend_type.capitalize())()
    obj.store(quote)


class Backends(metaclass=ABCMeta):
    """
    Defines various backend procedures
    """
    @abstractmethod
    def store(self, quote: dict):
        raise NotImplemented


class Stdout(Backends):

    def store(self, quote: dict):
        """

        Parameters
        ----------
        quote

        Returns
        -------

        """
        pprint.pprint(quote)


class Elasticsearch(Backends):

    def store(self, quote: dict):
        """

        Parameters
        ----------
        quote

        Raises
        ------
        See
        https://github.com/elastic/elasticsearch-dsl-py/blob/master/elasticsearch_dsl/exceptions.py

        """

        quote: StockQuote = StockQuote(
            updated_on=datetime.utcnow(),
            symbol=quote.get('symbol'),
            short_name=quote.get('short_name'),
            regularMarketPrice=quote.get('regularMarketPrice')
        )

        quote.meta.id = hashlib.sha256(quote.updated_on.isoformat().encode()).hexdigest()
        quote.save()
