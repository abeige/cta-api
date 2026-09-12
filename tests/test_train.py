import pytest
import cta


@pytest.fixture
def client():
    return cta.TransitClient()


def test_get_arrivals_type(client):
    arrivals = client.train.get_arrivals(41220)
    assert type(arrivals) == dict


@pytest.mark.parametrize("args", [
    (),
    (80,),
    (80, 80),
    (12345, 12345),
])
def test_get_arrivals_args(client, args):
    with pytest.raises(AssertionError):
        client.train.get_arrivals(*args)


@pytest.mark.parametrize('kwargs', [
    {'station_id':80},
    {'stop_id':80},
])
def test_get_arrivals_kwargs(client, kwargs):
    with pytest.raises(AssertionError):
        client.train.get_arrivals(**kwargs)


def test_get_locations_exception(client):
    with pytest.raises(AssertionError):
        client.train.get_locations('Green')


def test_follow_exception(client):
    with pytest.raises(ValueError):
        client.train.follow('a')


def test_get_arrivals(client):
    assert 'ctatt' in client.train.get_arrivals(40380)


def test_follow(client):
    run_number = client.train.get_arrivals(40380)['ctatt']['eta'][0]['rn']
    assert 'ctatt' in client.train.follow(run_number)


def test_get_locations(client):
    assert 'ctatt' in client.train.get_locations('Red')
