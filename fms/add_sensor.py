import os
import subprocess

from happi import Client
from happi.errors import EnforceError, SearchError

from .happi.containers import FMSRaritanItem, FMSSRCItem
from .utils import TypeEnforcer as te

fms_happi_database = os.environ["HAPPI_CFG"]

with open(fms_happi_database, "r") as file:
    lines = file.readlines()
    for line in lines:
        if "path" in line:
            fms_happi_database = line.split("=")[1].strip()

sensor_name = 0


def update_captar(first_name, middle_item, last_name, client=None):
    if client is None:
        client = Client(path=fms_happi_database)
    first_item = client.find_item(name=first_name)
    last_item = client.find_item(name=last_name)

    if middle_item.captar_out != last_item.captar_in:
        last_item.captar_in = middle_item.captar_out
        middle_item.captar_in = first_item.captar_out
    else:
        first_item.captar_out = middle_item.captar_in
        middle_item.captar_out = last_item.captar_in

    middle_item.save()
    last_item.save()
    first_item.save()


def find_port(name, client=None):
    if client is None:
        client = Client(path=fms_happi_database)
    item = client.find_item(name=name)
    return item.root_sensor_port


def add_sensor_to_src(item, client=None):
    if client is None:
        client = Client(path=fms_happi_database)

    src_controller = client.find_item(name=item.parent_switch)
    if item.root_sensor_port == None:
        item.root_sensor_port = find_port(item.last_connection_name, client)
    print(f"Saving Current Item: {item.name} to Port: {item.root_sensor_port}")

    port = "port" + str(item.root_sensor_port)
    curr_sensor_list = getattr(src_controller, port)
    print(f"Current List: {curr_sensor_list}")

    index = 0
    found = False
    for sensor in curr_sensor_list:
        if "src" in item.last_connection_name:
            found = True
            break
        elif sensor[sensor_name] == item.last_connection_name:
            found = True
            break
        else:
            index += 1

    if found:
        # installation in middle, update captar.
        if index != len(curr_sensor_list) - 1:
            print(
                f"Last={curr_sensor_list[index + 1][sensor_name]} middle={item.name} last={curr_sensor_list[index][sensor_name]}"
            )
            update_captar(
                curr_sensor_list[index][sensor_name],
                item,
                curr_sensor_list[index + 1][sensor_name],
            )

        curr_sensor_list.insert(
            index + 1, (item.name, item.eth_dist_last, item.num_sensors)
        )

    else:
        curr_sensor_list.append((item.name, item.eth_dist_last, item.num_sensors))
    print(f"Updated List: {curr_sensor_list}")

    setattr(src_controller, port, curr_sensor_list)
    src_controller.save()


def add_sensor(sensor_name, client):
    if client is None:
        client = Client(path=fms_happi_database)

    beckhoff_sensor = te.get_list_str(["Y", "N"], "Beckhoff Y/N?\n")
    if beckhoff_sensor == "Y":
        subprocess.run(["happi", "add"])
        exit()

    sensor_prefix = te.get_str("Enter PV prefix\n")
    sensor_location = te.get_str("Enter rack, stand, or location\n")
    captar_in = te.get_str("Enter Captar # in\n")
    captar_out = te.get_str("Enter Captar # out\n")
    functional_group = te.get_str("Enter Functional Group e.g. racks, floor, laser\n")
    location_group = te.get_str("Enter Location Group\n")
    pcdsdevice = te.get_str("Enter device class\n")
    beamline = "FMS"

    if "src" in sensor_name:
        num_src_ports = 8
        item = client.create_item(
            item_cls=FMSSRCItem,
            name=sensor_name,
            prefix=sensor_prefix,
            captar_in=captar_in,
            captar_out=captar_out,
            location=sensor_location,
            beamline=beamline,
            functional_group=functional_group,
            location_group=location_group,
            device_class="pcdsdevices.fms.SRCController",
        )
        for i in range(num_src_ports):
            setattr(item, "port" + str(i), [(sensor_name, 0, 0)])
        item.save()
        return

    invalid = True
    while invalid:
        parent_switch = te.get_str("Enter a valid Parent SRC Controller happi name:\n")
        try:
            client.find_item(name=parent_switch)
            invalid = False
        except SearchError:
            ...

    root_sensor_port = te.get_str(
        "Enter port number if first sensor or leave blank if not\n"
    )

    invalid = True

    while invalid:
        last_connection_name = te.get_str("Enter a valid last sensor happi name:\n")
        try:
            client.find_item(name=last_connection_name)
            invalid = False
        except SearchError:
            if root_sensor_port is not None:
                invalid = False
            ...
    # options

    # validate input here
    eth_dist_last = te.get_int("Enter Eth Distance from last sensor/src\n")
    num_sensors = te.get_int(
        "Enter the number of sensors: DX2-T1H1: 3, DX2-T1: 1, DX2-WSC: 1\n"
    )

    if (root_sensor_port == "" or root_sensor_port == None) and (
        last_connection_name == "" or last_connection_name == None
    ):
        raise (EnforceError("must define root_sensor port or last connection in feet"))

    item = client.create_item(
        item_cls=FMSRaritanItem,
        name=sensor_name,
        prefix=sensor_prefix,
        parent_switch=parent_switch,
        root_sensor_port=root_sensor_port,
        eth_dist_last=eth_dist_last,
        last_connection_name=last_connection_name,
        num_sensors=num_sensors,
        captar_in=captar_in,
        captar_out=captar_out,
        location=sensor_location,
        beamline=beamline,
        functional_group=functional_group,
        location_group=location_group,
        device_class=pcdsdevice,
    )
    add_sensor_to_src(item, client)
    item.save()
