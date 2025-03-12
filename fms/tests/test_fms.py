from ..happi.containers import FMSSRCItem
from happi import Client
from happi.item import OphydItem
from happi.backends.json_db import JSONBackend
from happi.errors import SearchError
import os
import pytest
from .test_utils import assert_valid, sensor_in_list
from fms.__main__ import add_src_controller, add_fms_sensor, delete_sensor

test_file = "test.db"

@pytest.fixture
def clean_files(monkeypatch):
    db = JSONBackend(path=test_file, initialize=True)
    client = Client(path=test_file) 
    sensor = [("temp1", "3"), ("temp2", "4")]

    inputs = iter(["N", "TST:PV", "R64", "L88", "L77", "TST", "TST", "class"])
    monkeypatch.setattr('builtins.input', lambda _:next(inputs))
    add_src_controller("src_tst_01", client)

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
    client, sensor = clean_files
    assert(sensor[0][sensor_name] == "temp1") 

    item = client.create_item(item_cls=FMSSRCItem,
            name="test_src",
            prefix="TEST:SRC:PV",
            port0=sensor,
            beamline="TST",
            location_group="TST",
            functional_group="TST")

    item.save()
    assert_valid(client)

    item = client.find_item(name="test_src")
    child_list = item.port0

    assert(sensor[0][sensor_name] == "temp1")
    assert(sensor[1][sensor_name] == "temp2")
    assert(child_list[0][sensor_name] == "temp1")
    assert(child_list[1][sensor_name] == "temp2")

def test_add_src_controller(clean_files, monkeypatch):
    inputs = iter(["N", "TST:PV", "R64", "L88", "L77", "TST", "TST", "class"])
    monkeypatch.setattr('builtins.input', lambda _:next(inputs))

    client, sensor = clean_files
    add_src_controller("a_new_src_controller", client)

    item = client.find_item(name="a_new_src_controller")
    assert(item.name == "a_new_src_controller")

    inputs = iter([1, 1, 1, 1, 1])
    monkeypatch.setattr('builtins.input', lambda _:next(inputs))
    with pytest.raises(ValueError):
        add_src_controller("a_bad_src_controller", client)

def test_add_root_raritan_sensor(clean_files, monkeypatch):
    client, sensor = clean_files

    inputs = iter(["N", "TST:PV", "R64", "L88", "L77", "TST", "TST", "class_ex",
                    "src_tst_01", "2", "not_found", 5, 1])
    monkeypatch.setattr('builtins.input', lambda _:next(inputs))
    add_fms_sensor("test_name", client=client)

def test_add_and_delete(clean_files, monkeypatch):
    client, sensor = clean_files

    inputs = iter(["N", "TST:PV", "R64", "L88", "L77", "TST", "TST", "class_ex",
                    "src_tst_01", "2", "not_found", 5, 1])
    monkeypatch.setattr('builtins.input', lambda _:next(inputs))
    add_fms_sensor("test_name", client=client)

    #check if its added
    item = client.find_item(name="test_name")
    assert(item.name == "test_name")

    #check if added to parent list
    parent_item = client.find_item(name=item.parent_switch)
    assert(sensor_in_list(item.name,parent_item.port2))

    delete_sensor(item.name, client=client)

    #check its deleted
    with pytest.raises(SearchError):
        item = client.find_item(name="test_name")

    #check deleted from parent sensor list
    parent_item = client.find_item(name=item.parent_switch)
    assert([sensor for sensor in parent_item.port2 if sensor[0] == "test_name"] == [])
