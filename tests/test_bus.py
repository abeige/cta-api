import pytest
import cta

@pytest.fixture
def client():
    return cta.TransitClient()

def test_get_stops(client):
    stops = client.bus.get_stops(8, 'nb')
    assert type(stops) == dict
