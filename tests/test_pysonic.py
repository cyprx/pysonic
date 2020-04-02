"""
Below are integration tests, please make sure you have 
Sonic DB available at localhost:1491 to run
"""
import logging
import pytest

import pysonic


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('pysonic')


def test_ping():
    client = pysonic.Client()
    with client.mode('search') as c:
        resp = c.ping()
        assert resp


def test_query():
    client = pysonic.Client()
    with client.mode('search') as c:
        resp = c.query("test", "test", "this is")
        assert resp == ['product_1']


def test_ingest():
    client = pysonic.Client()
    with client.mode('ingest') as c:
        c.push("test", "test", "product_22", "this is product_22")


@pytest.mark.skip
def test_suggest():
    c = pysonic.Client()
    with c:
        c.mode(pysonic.Mode.SEARCH)
        assert c.suggest("test", "test", "thi") == ['this']
