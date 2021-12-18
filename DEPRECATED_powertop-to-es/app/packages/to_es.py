import logging
import pprint
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from elasticsearch.helpers import BulkIndexError

# Singleton implementation
class ToEs:

    # Shared variable
    LOG_LEVEL = logging.INFO

    def __new__(cls):

        # Only create actual instance at very first time
        if not hasattr(cls, '_instance'):
            cls._instance = super(ToEs, cls).__new__(cls)

        return cls._instance

    def __init__(self, **kwargs):

        # Init elasticsearch instance just once
        self._es     = Elasticsearch()

        # Set logger for this class
        self._logger = self._prep_logger()

        self._logger.debug('ref: {}'.format(self._es))

    @staticmethod
    def get_instance():
        return ToEs()

    def send_to_es(self, data, index):
        def gendata(docs):
            for d in docs:
                self._logger.debug('Document: {}'.format(d))
                d.update({'_op_type': 'index' , '_index': index })

                yield d

        self._logger.debug('Input data: {}'.format(pprint.pformat(data)))

        try:
            bulk(self._es, gendata(data))

        except BulkIndexError as e:
            self._logger.error(e)

    def count_docs(self, **kwargs):

        return self._es.count(index=kwargs['index'], body=kwargs['body'])

    # All private stuffs are below
    def _prep_logger(self):
        logger_ = logging.getLogger(__name__)
        logger_.setLevel(self.LOG_LEVEL)

        return logger_
