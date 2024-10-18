from ..happi.containers import FMSRaritanItem, FMSBeckhoffItem, FMSSRCItem, FMSItem
from happi import Client
from happi.item import OphydItem
from happi.backends.json_db import JSONBackend
import os, pytest, json
from .test_utils import assert_invalid, assert_valid

test_file = "test.db"

@pytest.fixture
def clean_files():
    db = JSONBackend(path=test_file, initialize=True)
    client = Client(path=test_file) 
    sensor = [("temp1", "3")]
    yield client, sensor

    if os.path.exists(test_file):
        os.remove(test_file)

def test_add(clean_files):
    client, sensor = clean_files
    item = client.create_item(item_cls=OphydItem,
            name="test",
            prefix="TEST:PV")
    item.save()
    assert_valid(client)

def test_add_src(clean_files):
    client, sensor = clean_files
    sensor_to_add = json.dumps(sensor)

    item = client.create_item(item_cls=FMSSRCItem,
            name="test_src",
            prefix="TEST:SRC:PV",
            port0=sensor_to_add)

    item.save()
    assert_valid(client)