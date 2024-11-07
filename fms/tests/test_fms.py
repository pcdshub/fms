from ..happi.containers import FMSRaritanItem, FMSBeckhoffItem, FMSSRCItem, FMSItem
from happi import Client
from happi.item import OphydItem
from happi.backends.json_db import JSONBackend
import os, pytest, json
from .test_utils import assert_invalid, assert_valid
from fms.__main__ import add_src_controller, add_fms_sensor

test_file = "test.db"

@pytest.fixture
def clean_files():
    db = JSONBackend(path=test_file, initialize=True)
    client = Client(path=test_file) 
    sensor = [("temp1", "3"), ("temp2", "4")]

    yield client, sensor

    assert_valid(client)
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
    sensor_name = 0
    distance = 1
    client, sensor = clean_files
    assert(sensor[0][sensor_name] == "temp1") 

    item = client.create_item(item_cls=FMSSRCItem,
            name="test_src",
            prefix="TEST:SRC:PV",
            port0=sensor)

    item.save()
    assert_valid(client)

    item = client.find_item(name="test_src")
    child_list = item.port0
    assert(sensor[0][sensor_name] == "temp1") 
    assert(sensor[1][sensor_name] == "temp2") 

def test_add_src_controller(clean_files, monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "a_new_src_controller")
    client, sensor = clean_files
    add_src_controller(client)

    item = client.find_item(name="a_new_src_controller")
    assert(item.name == "a_new_src_controller")

    monkeypatch.setattr('builtins.input', lambda _: 1)
    with pytest.raises(ValueError):
        add_src_controller(client)

def test_add_raritan_sensor(clean_files, monkeypatch):
    client, sensor = clean_files

    inputs = iter(["src_mec_01"])
    monkeypatch.setattr('builtins.input', lambda _:next(inputs))
    add_src_controller(client)

    inputs = iter(["foo", "Raritan","src_mec_01","3","", 10])
    monkeypatch.setattr('builtins.input', lambda _:next(inputs))
    add_fms_sensor(client=client)

    inputs = iter(["foo_name", "foo_type", "foo_type", "foo_type","src-mec-01","3", 10, ])
    monkeypatch.setattr('builtins.input', lambda _:next(inputs))

    with pytest.raises(ValueError):
       add_fms_sensor(client)
