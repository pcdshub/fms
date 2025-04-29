import argparse
import os
import subprocess
import sys

from happi import Client
from happi.errors import SearchError

from .add_sensor import add_sensor
from .check_topology import check_topology
from .happi.containers import FMSRaritanItem

fms_happi_database = os.environ["HAPPI_CFG"]

with open(fms_happi_database, "r") as file:
    lines = file.readlines()
    for line in lines:
        if "path" in line:
            fms_happi_database = line.split("=")[1].strip()


def delete_sensor(sensor_name, client=None):
    if client is None:
        client = Client(path=fms_happi_database)
    item = client.find_item(name=sensor_name)

    if type(item) is FMSRaritanItem:
        try:
            parent_switch_item = client.find_item(name=item.parent_switch)
            port = "port" + str(item.root_sensor_port)
            sensor_list = getattr(parent_switch_item, port)
            sensor_list = [sensor for sensor in sensor_list if sensor[0] != sensor_name]
            print(f"deleted: {sensor_name} from: {sensor_list}")
            setattr(parent_switch_item, port, sensor_list)
            parent_switch_item.save()
        except SearchError:
            ...
    client.remove_item(item)


def validate():
    client = Client(path=fms_happi_database)
    results = client.validate()
    if len(results) == 0:
        print("Success! Valid FMS Database.")
    else:
        print(f"These devices are malformed! {results}")


def add_src_controller(controller_name=None, client=None):
    add_sensor(controller_name, client)


def add_fms_sensor(sensor_name=None, client=None):
    add_sensor(sensor_name, client)


def launch_nalms():
    command = "slam --topics FMS-alarms --bootstrap-servers 172.24.5.232:9094 &"
    subprocess.run(command, shell=True)


def setup_argument_parser():
    parser = argparse.ArgumentParser(
        prog="fms",
        description="A module for managing facillity monitoring raritan devices",
        epilog="Thank you for using the fms CLI!",
    )
    parser.add_argument(
        "--validate", action="store_true", dest="validate", help="validate database"
    )
    parser.add_argument(
        "--add_sensor",
        dest="add_sensor",
        help="walk through adding a sensor to FMS",
        default=None,
    )
    parser.add_argument(
        "--add_src_controller",
        dest="src_controller",
        help="walk through adding a raritan SRC controller to FMS",
        default=None,
    )
    parser.add_argument("-s", "--src", dest="src_controller", help="src controller")
    parser.add_argument("-p", "--port", dest="port", help="src controller port")

    parser.add_argument(
        "--check_topology",
        dest="src_controller",
        help="print the current FMS topology",
        default=None,
    )
    parser.add_argument(
        "--launch_nalms", action="store_true", help="launch the nalms home screen"
    )
    parser.add_argument("--delete_sensor", dest="delete_sensor", help="delete_sensor")

    parser.add_argument(
        "-hn",
        "--happi_name",
        dest="happi_name",
        help="happi database name",
        default=None,
    )

    return parser


print(f"the happi config is set to: {fms_happi_database}")


def main(argv):
    argument_parser = setup_argument_parser()
    options = argument_parser.parse_args()
    if options.add_sensor:
        add_fms_sensor(sensor_name=options.add_sensor)
    elif options.launch_nalms:
        launch_nalms()
    elif options.src_controller and not options.port:
        add_src_controller(controller_name=options.src_controller)
    elif options.validate:
        validate()
    elif options.src_controller and options.port:
        check_topology(options.src_controller, options.port)
    elif options.delete_sensor:
        delete_sensor(options.delete_sensor)
    else:
        argument_parser.print_help()


if __name__ == "__main__":
    main(sys.argv)
