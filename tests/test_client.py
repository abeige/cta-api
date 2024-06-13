import pytest
import cta


@pytest.fixture
def client():
    return cta.TransitClient()


@pytest.mark.parametrize("args", [
    (0,),
    (0, 1),
    (29999, 0),
])
def test_bus_id_len(client, args):
    assert client.bus.assert_id_len(*args) is None


@pytest.mark.parametrize("args", [
    (30000,),
    (30000, 30001),
    (-1,),
    (60000,),
    (10, 30847),
])
def test_bus_id_len_error(client, args):
    with pytest.raises(AssertionError):
        client.bus.assert_id_len(*args)


@pytest.mark.parametrize("args", [
    (30000, ),
    (30000, 30001),
    (49999, ),
    (49999, 49998),
    (48830, ),
])
def test_train_id_len(client, args):
    assert client.train.assert_id_len(*args) is None


@pytest.mark.parametrize("args", [
    (0, ),
    (-1, ),
    (50000, ),
    (29999, 0),
])
def test_train_id_len_error(client, args):
    with pytest.raises(AssertionError):
        client.train.assert_id_len(*args)
