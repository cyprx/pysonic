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
    c = pysonic.Client()
    with c:
        resp = c.ping()
        assert resp


def test_select_mode():
    c = pysonic.Client()
    with c:
        resp = c.mode(pysonic.Mode.SEARCH)
        assert resp


@pytest.mark.skip
def test_query():
    c = pysonic.Client()
    with c:
        print(c.mode(pysonic.Mode.SEARCH))
        resp = c.query("test", "test", "this is")
        assert resp == ['product_1']


def test_ingest():
    c = pysonic.Client()
    with c:
        c.mode(pysonic.Mode.INGEST)
        assert c.push("test", "test", "product_22", "this is product_22")


def test_suggest():
    c = pysonic.Client()
    with c:
        c.mode(pysonic.Mode.SEARCH)
        assert c.suggest("test", "test", "thi") == ['this']
