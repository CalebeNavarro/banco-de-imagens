
from app import app

test_client = app.test_client()

def test_first():
    print(test_client.options('/upload'))
    assert 'POST' in (test_client.options('/upload').headers['Allow'])

