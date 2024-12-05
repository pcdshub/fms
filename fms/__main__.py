import sys, argparse, json
from happi import Client
from .utils import TypeEnforcer as te
from happi.item import OphydItem
from happi.errors import EnforceError, SearchError
from .happi.containers import FMSRaritanItem, FMSSRCItem
from typing import List
from .check_topology import check_topology
from .add_sensor import add_sensor

#fms_happi_database = "/reg/g/pcds/pyps/apps/hutch-python/device_config/db.json"
fms_happi_database = "fms_test.json"


def delete_sensor(sensor_name, client=None):
    if client == None:
        client = Client(path=fms_happi_database)
    item = client.find_item(name=sensor_name)

    if type(item) == FMSRaritanItem:
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
        print(f'These devices are malformed! {results}')

def get_all_src_status():
    get_src_controllers()

def get_src_controllers(client: Client=None) -> List[str]:
    if client is None:
        client = Client(path=fms_happi_database)
    ret = client.search(name='booch')
    print(ret)

def add_src_controller(controller_name=None, client=None):
    num_src_ports = 8
    if controller_name == None:
        controller_name = te.get_str("Enter controller name\n")

    if client == None:
        client = Client(path=fms_happi_database)

    item = client.create_item(item_cls=FMSSRCItem,
        name=controller_name,
        prefix="RTD:TEST:FMS"
    )
    for i in range(8):
        setattr(item, "port" + str(i), [(controller_name, 0, 0)])

    item.save()

def add_fms_sensor(sensor_name=None, client=None):
    add_sensor(sensor_name, client)

def SetupArgumentParser():
    parser = argparse.ArgumentParser(
                        prog="fms",
                        description='A module for managing facillity monitoring raritan devices',
                        epilog='Thank you for using the fms CLI!')
    parser.add_argument('--validate', action='store_true', dest="validate", help='validate database')
    parser.add_argument('--add_sensor', dest="add_sensor", help='walk through adding a sensor to FMS', default=None)
    parser.add_argument('--add_src_controller', dest="src_controller", help='walk through adding a raritan SRC controller to FMS', default=None)
    parser.add_argument('-s','--src', dest='src_controller', help='src controller')
    parser.add_argument('-p','--port', dest='port', help='src controller port')

    parser.add_argument('--list_all_sensors', action='store_true', help="print a list of sensors")
    parser.add_argument('--check_topology', dest='src_controller', help='print the current FMS topology', default=None)
    parser.add_argument('--launch_nalms', action='store_true',help="launch the nalms home screen")
    parser.add_argument('--delete_sensor', dest='delete_sensor', help="delete_sensor")
 
    parser.add_argument('-hn','--happi_name', dest='happi_name', help='happi database name', default=None)



    return parser

def main(argv):
    argument_parser = SetupArgumentParser()
    options = argument_parser.parse_args()
    if options.add_sensor:
        add_fms_sensor(sensor_name=options.add_sensor)
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

main(sys.argv)
