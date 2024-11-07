from ..happi.containers import FMSRaritanItem, FMSBeckhoffItem, FMSSRCItem, FMSItem
from happi import Client
from happi.errors import DuplicateError, EntryError
from happi.item import OphydItem
from happi.backends.json_db import JSONBackend
import os, pytest

test_file = "test.db"

@pytest.fixture
def clean_files():
    db = JSONBackend(path=test_file, initialize=True)
    yield

    if os.path.exists(test_file):
        os.remove(test_file)

def assert_valid(client):
    assert len(client.validate()) == 0

def assert_invalid(client):
    assert len(client.validate()) != 0

def inc(x):
    return x + 1

def test_inc():
    assert inc(3) != 5

def test_OphydItem(clean_files):
    client = Client(path=test_file) 

    item = client.create_item(item_cls=OphydItem,
            name="test",
            prefix="TEST:PV")

    item.save()
    assert_valid(client)

    item = client.create_item(item_cls=OphydItem,
            name="test1",
            prefix="TEST:PV",
            bad_att=1)

    item.save()
    assert_valid(client)

def test_FMSItem(clean_files):
    client = Client(path=test_file) 

    item = client.create_item(item_cls=FMSItem,
            name="test",
            prefix="TEST:PV",
            high_alarm=1,
            moderate_alarm=1,
            low_alarm=1,
            bottom_alarm=1)

    item.save()
    assert_valid(client)

def test_FMSRaritanItem(clean_files):
    client = Client(path=test_file) 
    
    with pytest.raises(EntryError):
        item = client.create_item(item_cls=FMSRaritanItem,
                name="test",
                prefix="TEST:PV",
                high_alarm=1,
                moderate_alarm=1,
                low_alarm=1,
                bottom_alarm=1)

        item.save()
        print('hello')
