"""
Below are integration tests, please make sure you have 
Sonic DB available at localhost:1491 to run
"""
import uuid
import logging
import pytest

import pysonic


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('pysonic')


@pytest.fixture(scope='session')
def collection():
    return 'collection_integration_test'


@pytest.fixture(scope='session')
def bucket():
    return "bucket_test"


@pytest.fixture(scope='session')
def object():
    return str(uuid.uuid1()).replace("-", "")


@pytest.fixture(scope='session')
def text():
    return 'This is a test text in english'


@pytest.fixture(scope='session', autouse=True)
def run_test_context(collection, bucket, object, text):
    client = pysonic.Client()
    with client.mode('ingest') as c:
        c.push(collection, bucket, object, text)
    yield
    with client.mode('ingest') as c:
        r = c.flushc(collection)
        print(r)


def test_ping():
    client = pysonic.Client()
    with client.mode('search') as c:
        resp = c.ping()
        assert resp


def test_count(collection, bucket, object):
    client = pysonic.Client()
    with client.mode('ingest') as c:
        resp = c.count(collection, bucket)
        print(resp)


@pytest.mark.skip
def test_ingest():
    client = pysonic.Client()
    with client.mode('ingest') as c:
        c.push("test", "test", "product 22", "this is product_22")


def test_query(collection, bucket, object):
    client = pysonic.Client()
    with client.mode('search') as c:
        resp = c.query(collection, bucket, "This is a test text in english")
        assert resp == [object]


@pytest.mark.skip
def test_suggest(collection, bucket):
    client = pysonic.Client()
    with client.mode('search') as c:
        assert c.suggest(collection, bucket, "engli") == ['english']


@pytest.mark.skip
def test_flushb():
    client = pysonic.Client()
    with client.mode('ingest') as c:
        resp = c.flushb("test", "test")
        assert resp == ['product_1']
