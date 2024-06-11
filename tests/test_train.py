import pytest
import cta


@pytest.fixture
def conn():
    return cta.TransitClient()


def test_get_arrivals_type(conn):
    arrivals = conn.train.get_arrivals(41220)
    assert type(arrivals) == dict


@pytest.mark.parametrize("args", [
    (),
    (80,),
    (80, 80),
    (12345, 12345),
])
def test_get_arrivals_args(conn, args):
    with pytest.raises(AssertionError):
        conn.train.get_arrivals(*args)


@pytest.mark.parametrize('kwargs', [
    {'station_id':80},
    {'stop_id':80},
])
def test_get_arrivals_kwargs(conn, kwargs):
    with pytest.raises(AssertionError):
        conn.train.get_arrivals(**kwargs)


def test_get_locations_exception(conn):
    with pytest.raises(AssertionError):
        conn.train.get_locations('Green')


def test_follow_exception(conn):
    with pytest.raises(ValueError):
        conn.train.follow('a')
