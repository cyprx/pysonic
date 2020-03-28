import pytest

from pysonic import pysonic


@pytest.mark.skip
def test_ping():
    c = pysonic.Client()
    with c:
        resp = c.ping()
        print(resp)


@pytest.mark.skip
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
