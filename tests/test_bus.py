import pytest
import cta

@pytest.fixture
def conn():
    return cta.TransitClient()

def test_get_stops(conn):
    stops = conn.bus.get_stops(8, 'nb')
    assert type(stops) == dict
