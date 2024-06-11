import pytest
import cta


@pytest.fixture
def conn():
    return cta.TransitClient()


def test_get_arrivals_type(conn):
    arrivals = conn.train.get_arrivals(41220)
    assert type(arrivals) == dict


def test_get_arrivals_exception(conn):
    # station_id too short (default)
    with pytest.raises(AssertionError):
        conn.train.get_arrivals(80)

    # can't specify both, both too short
    with pytest.raises(AssertionError):
        conn.train.get_arrivals(80, 80)

    # can't specify both
    with pytest.raises(AssertionError):
        conn.train.get_arrivals(12345, 12345)

    # station_id too short
    with pytest.raises(AssertionError):
        conn.train.get_arrivals(station_id=80)

    # stop_id too short
    with pytest.raises(AssertionError):
        conn.train.get_arrivals(stop_id=80)
