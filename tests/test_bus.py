import pytest
import cta


@pytest.fixture
def client():
    return cta.TransitClient()


def test_get_vehicles(client: cta.TransitClient):
    result = client.bus.get_vehicles(route=8)
    assert 'bustime-response' in result

    vid = result['bustime-response']['vehicle'][0]['vid']
    assert 'bustime-response' in client.bus.get_vehicles(vid)


def test_get_routes(client: cta.TransitClient):
    assert 'bustime-response' in client.bus.get_routes()


def test_get_directions(client: cta.TransitClient):
    assert 'bustime-response' in client.bus.get_directions(route=8)


def test_get_patterns(client: cta.TransitClient):
    assert 'bustime-response' in client.bus.get_patterns(route=8)


def test_get_predictions(client: cta.TransitClient):
    assert 'bustime-response' in client.bus.get_predictions(stop_id=18184, route=8)


def test_both_param_error(client):
    with pytest.raises(AssertionError):
        client.bus.get_predictions(stop_id=18184, route=8, vehicle_id=700)


def test_no_param_error(client):
    with pytest.raises(AssertionError):
        client.bus.get_predictions(route=8)


def test_incompatible_param_error(client):
    with pytest.raises(AssertionError):
        client.bus.get_predictions(vehicle_id=700, route=8)


def test_get_stops(client: cta.TransitClient):
    assert 'bustime-response' in client.bus.get_stops(8, 'nb')


