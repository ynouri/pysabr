from falcon import testing
import pytest


@pytest.fixture()
def client(scope='module'):
    from web.app import app
    return testing.TestClient(app)


def test_sabr(client):
    params = {'k': 1.0, 'f': 0.02, 't': 1.0, 'a': 0.20,
              'b': 1.0, 'r': 0.0, 'n': 0.0}
    result = client.simulate_get(path='/sabr', params=params)
    assert float(result.text) == 0.2


def test_alpha(client):
    params = {'v': 0.6, 'f': 0.02, 't': 1.0,
              'b': 1.0, 'r': 0.0, 'n': 0.0}
    result = client.simulate_get(path='/alpha', params=params)
    assert float(result.text) == 0.60
