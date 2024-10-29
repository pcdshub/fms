import sys, optparse, json, networkx as nx
from .utils import TypeEnforcer as te
from happi import Client
from happi.item import OphydItem
from happi.errors import EnforceError
from .happi.containers import FMSRaritanItem, FMSBeckhoffItem, FMSSRCItem
from typing import List

fms_happi_database = "fms_test.json"

def find_port(name, client=None):
    if client == None:
        client = Client(path=fms_happi_database)
    item = client.find_item(name=name)
    return item.root_sensor_port

def delete_sensor(sensor, client=None):
    if client == None:
        client = Client(path=fms_happi_database)
    item = client.find_item(name=sensor)
    client.remove_item(item)

def validate():
    client = Client(path=fms_happi_database)
    print(type(client.validate()))

def check_topology(src_controller, port, client=None):
    if client == None:
        client = Client(path=fms_happi_database)
    
    src_controller = client.find_item(name=src_controller)
    curr_sensor_list = json.loads(getattr(src_controller, "port" + port))

    for sensor in curr_sensor_list:
        print(sensor)

def get_all_src_status():
    get_src_controllers()
def get_src_controllers(client: Client=None) -> List[str]:
    if client is None:
        client = Client(path=fms_happi_database)
    ret = client.search(name='booch')
    print(ret)

def add_src_controller(client=None):
    controller_name = te.get_str("Enter controller name\n")

    if client == None:
        client = Client(path=fms_happi_database)

    item = client.create_item(item_cls=FMSSRCItem,
        name=controller_name,
        prefix="RTD:TEST:FMS"
    )
    item.save()

def add_sensor_to_src(item, client=None):
    if client == None:
        client = Client(path=fms_happi_database)

    src_controller = client.find_item(name=item.parent_switch)

    port = None
    if item.root_sensor_port != None:
        #root sensor
        curr_sensor_list = []
        port = "port" + item.root_sensor_port
    else:
        port = find_port(item.last_connection_name, client)
        print(f'Saving Port to Current Item: {item.name}')
        item.root_sensor_port = port

        port = "port" + str(port)
        raw_data = getattr(src_controller, port)                
        curr_sensor_list = json.loads(raw_data)
        print(f'Current List: {curr_sensor_list}')

    curr_sensor_list.append((item.name, item.eth_dist_last))
    print(f'Updated List: {curr_sensor_list}')

    setattr(src_controller, port, json.dumps(curr_sensor_list))
    src_controller.save()

def add_fms_sensor(sensor_name=None, client=None):
    container_type = None
    root_sensor_port = None
    eth_dist_last = None
    if sensor_name == None:
        sensor_name = te.get_str("Enter sensor name\n")
    sensor_type = te.get_list_str(["Beckhoff", "Raritan"], "Enter sensor type Beckhoff/Raritan\n")

    if sensor_type == "Raritan":
        parent_switch = te.get_str("Enter a valid Parent SRC Controller happi name:\n")
        #validate input here
        root_sensor_port = te.get_str("Enter port number if first sensor or leave blank if not")
        last_connection_name = te.get_str("Enter the happi name of the last sensor this one is attached to\n")
        #validate input here
        eth_dist_last = te.get_int("Enter Eth Distance from last sensor\n")
        container_type = FMSRaritanItem
        if root_sensor_port == "" or root_sensor_port == None and last_connection_name == "" or last_connection_name == None:
            raise(EnforceError("must define root_sensor port or last connection"))
    else:
        container_type = FMSBeckhoffItem
    
    if client == None:
        client = Client(path=fms_happi_database)

    item = client.create_item(item_cls=container_type,
        name=sensor_name,
        prefix="RTD:TEST:FMS",
        parent_switch=parent_switch,
        root_sensor_port=root_sensor_port,
        eth_dist_last=eth_dist_last,
        last_connection_name=last_connection_name
    )
    if type(item) == FMSRaritanItem:
        ret = add_sensor_to_src(item, client)
    item.save()

def SetupOptionParser():
    parser = optparse.OptionParser(usage=__doc__)
    parser.add_option('--validate',
                    action='store_true',
                    dest="validate",
                    help='validate database')
    parser.add_option('--src_status',
                    action='store_true',
                    dest="src_status",
                    help='get src config status')
    parser.add_option('--add_sensor',
                    dest="add_sensor",
                    help='walk through adding a sensor to FMS')
    parser.add_option('--add_src_controller',
                    action='store_true',
                    dest="add_src_controller",
                    help='walk through adding a raritan SRC controller to FMS')
    parser.add_option('--check_topology',
                    action='store_true',
                    dest='check_topology',
                    help='print the current FMS topology')
    parser.add_option('--list_all_sensors',
                    action='store_true',
                    help="print a list of sensors")
    parser.add_option('--print_active_alarms',
                    action='store_true',
                    help="prints a list of all alarms")
    parser.add_option('--launch_nalms',
                    action='store_true',
                    help="launch the nalms home screen")
    parser.add_option('--delete_sensor',
                    action='store_true',
                    help="launch the nalms home screen")
    return parser

def main(argv):
    options_parser = SetupOptionParser()
    (options, args) = options_parser.parse_args()

    if options.add_sensor:
        add_fms_sensor(options.add_sensor)
    elif options.add_src_controller:
        add_src_controller()
    elif options.src_status:
        get_all_src_status() 
    elif options.validate:
        validate() 
    elif options.check_topology:
        check_topology(args[0], args[1])
    elif options.delete_sensor:
        delete_sensor(args[0])
    else:
        options_parser.print_help()

main(sys.argv)
