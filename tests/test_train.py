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
