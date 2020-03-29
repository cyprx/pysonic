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
        print(resp)


def test_select_mode():
    c = pysonic.Client()
    with c:
        resp = c.mode(pysonic.Mode.SEARCH)
        print(resp)
        print(c.ping())


def test_query():
    c = pysonic.Client()
    with c:
        print(c.mode(pysonic.Mode.SEARCH))
        resp = c.query("test", "test", "this is")
        print(resp)


def test_ingest():
    c = pysonic.Client()
    with c:
        print(c.mode(pysonic.Mode.INGEST))
        print(c.push("test", "test", "product_22", "this is product_22"))


def test_suggest():
    c = pysonic.Client()
    with c:
        print(c.mode(pysonic.Mode.SEARCH))
        print(c.suggest("test", "test", "thi"))
