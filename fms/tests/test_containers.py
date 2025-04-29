import os

import pytest
from happi import Client
from happi.backends.json_db import JSONBackend
from happi.errors import EnforceError, EntryError
from happi.item import OphydItem

from ..happi.containers import FMSItem, FMSRaritanItem, FMSSRCItem
from .test_utils import assert_valid

test_file = "test.db"


@pytest.fixture
def clean_files():
    db = JSONBackend(path=test_file, initialize=True)
    yield

    if os.path.exists(test_file):
        os.remove(test_file)


@pytest.fixture
def sensors():
    sensors = [("temp1", "3"), ("temp2", "4")]
    yield sensors


def test_OphydItem(clean_files):
    client = Client(path=test_file)

    item = client.create_item(item_cls=OphydItem, name="test", prefix="TEST:PV")

    item.save()
    assert_valid(client)

    item = client.create_item(
        item_cls=OphydItem, name="test1", prefix="TEST:PV", bad_att=1
    )

    item.save()
    assert_valid(client)


def test_FMSItem(clean_files):
    client = Client(path=test_file)

    item = client.create_item(
        item_cls=FMSItem,
        name="test",
        prefix="TEST:PV",
        high_alarm=1,
        moderate_alarm=1,
        low_alarm=1,
        bottom_alarm=1,
        beamline="TST",
        location_group="TST",
        functional_group="TST",
    )

    item.save()
    assert_valid(client)


def test_FMSRaritanItem(clean_files):
    client = Client(path=test_file)

    # missing required entry info
    with pytest.raises(EntryError):
        item = client.create_item(
            item_cls=FMSRaritanItem,
            name="test",
            prefix="TEST:PV",
            high_alarm=1,
            moderate_alarm=1,
            low_alarm=1,
            bottom_alarm=1,
            beamline="TST",
            location_group="TST",
            functional_group="TST",
            num_sensors=1,
        )

        item.save()
    # valid data
    item = client.create_item(
        item_cls=FMSRaritanItem,
        name="test",
        prefix="TEST:PV",
        high_alarm=1,
        moderate_alarm=1,
        low_alarm=1,
        bottom_alarm=1,
        parent_switch="test_src",
        last_connection_name="tst-sensor-01",
        eth_dist_last=3,
        beamline="TST",
        location_group="TST",
        functional_group="TST",
        num_sensors=1,
    )
    item.save()
    assert_valid(client)

    with pytest.raises(EnforceError):
        item = client.create_item(
            item_cls=FMSRaritanItem,
            name="test1",
            prefix="TEST:PV",
            high_alarm=1,
            moderate_alarm=1,
            low_alarm=1,
            bottom_alarm=1,
            parent_switch="test_src",
            root_sensor=True,
            root_sensor_port="10",
            eth_dist_last=3,
            beamline="TST",
            location_group="TST",
            functional_group="TST",
            num_sensors=1,
        )
        item.save()


def test_FMSSRCItem(clean_files, sensors):
    client = Client(path=test_file)

    # valid item
    item = client.create_item(
        item_cls=FMSSRCItem,
        name="test",
        prefix="TEST:PV",
        high_alarm=1,
        moderate_alarm=1,
        low_alarm=1,
        bottom_alarm=1,
        beamline="TST",
        location_group="TST",
        functional_group="TST",
    )

    item.save()
    assert_valid(client)

    item = client.create_item(
        item_cls=FMSSRCItem,
        name="test1",
        prefix="TEST:PV",
        high_alarm=1,
        moderate_alarm=1,
        low_alarm=1,
        bottom_alarm=1,
        port0=sensors,
        beamline="TST",
        location_group="TST",
        functional_group="TST",
    )

    item.save()
    assert_valid(client)

    item = client.find_item(name="test1")
    sensors = item.port0
    assert type(sensors) is list
    assert sensors[0][0] == "temp1"
