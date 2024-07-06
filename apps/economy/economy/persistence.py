import hashlib
import importlib
import pprint
from abc import ABCMeta, abstractmethod
from datetime import datetime
from typing import Generator

from economy.model import StockQuote


def persist(entities: list, backend_type: str):
    """
    interface when persisting to backend

    Parameters
    ----------
    entities: list
    backend_type: str

    Raises
    ------
    ValueError

    """
    module: object = importlib.import_module('economy.persistence')
    obj: Backends = getattr(module, backend_type.capitalize())()
    obj.store(entities)


class Backends(metaclass=ABCMeta):
    """
    Defines various backend procedures
    """
    @abstractmethod
    def store(self, entities: list):
        raise NotImplemented


class Stdout(Backends):

    def store(self, entities: Generator):
        """

        Parameters
        ----------
        entities

        Returns
        -------

        """
        pprint.pprint(entities)


class Elasticsearch(Backends):

    def store(self, entities: Generator):
        """

        Parameters
        ----------
        entities

        Raises
        ------
        See
        https://github.com/elastic/elasticsearch-dsl-py/blob/master/elasticsearch_dsl/exceptions.py

        """

        # FIXME as bulk request
        for e in entities:
            e.save()
