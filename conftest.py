import pytest


@pytest.fixture
def client():
    from app import app

    # for test client api reference
    # http://flask.pocoo.org/docs/1.0/api/#test-client
    client = app.test_client()
    yield client
