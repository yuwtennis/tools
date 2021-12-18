import sys
import os
import pprint
sys.path.append(os.getcwd() + '/../app')

pprint.pprint(sys.path)

from packages.to_es import ToEs

def test_bulk():

    es = ToEs.get_instance()

    es.send_to_es([{'msg': 'hello world'}], 'myfirstindex')
    cnt = es.count_docs(index='myfirstindex' ,body='{"query":{ "match_all": {}}}')

    assert cnt['count'] > 0
