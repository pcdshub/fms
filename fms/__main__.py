
import sys, optparse
from utils import TypeEnforcer as te
from happi import Client
from happi.item import OphydItem
from containers import FMSRaritanItem, FMSBeckhoffItem, FMSSRCItem
from typing import List

fms_happi_database = "fms_test.json"
def validate():
    client = Client(path=fms_happi_database)
    print(type(client.validate()))

def get_all_src_status():
    get_src_controllers()
def get_src_controllers(client: Client=None) -> List[str]:
    if client is None:
        client = Client(path=fms_happi_database)
    ret = client.search(name='booch')
    print(ret)

def add_src_controller():
    controller_name = te.get_str("Enter controller name\n")

    client = Client(path=fms_happi_database)

    item = client.create_item(item_cls=FMSSRCItem,
        name=controller_name,
        prefix="RTD:TEST:FMS"
    )
    item.save()

def add_fms_sensor():
    '''
    container_type = None
    root_sensor_port = None
    eth_dist_last = None
    root_sensor = None
    sensor_name = te.get_str("Enter sensor name\n")
    sensor_type = te.get_list_str(["Beckhoff", "Raritan"], "Enter sensor type Beckhoff/Raritan\n")

    if sensor_type == "Raritan":
        parent_switch = te.get_str("Enter Parent SRC Controller name:\n")
        root_sensor_port = te.get_str("Enter Port Number if root[0-8]\n")
        eth_dist_last = te.get_int("Enter Eth Distance from last sensor\n")
        root_sensor = te.get_bool("Is this the first sensor connected to the switch? True/False\n")    
        container_type = FMSRaritanItem
    else:
        container_type = FMSBeckhoffItem
    

    client = Client(path=fms_happi_database)

    item = client.create_item(item_cls=container_type,
        name=sensor_name,
        prefix="RTD:TEST:FMS",
        parent_switch=sensor_name,
        root_sensor=root_sensor,
        root_sensor_port=root_sensor_port,
        eth_dist_last=eth_dist_last
    )
    '''
    client = Client(path=fms_happi_database)

    item = client.create_item(item_cls=OphydItem,
        name="foob",
        prefix="RTD:TEST:FMS",
    )

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
                    action='store_true',
                    dest="add_sensor",
                    help='walk through adding a sensor to FMS')
    parser.add_option('--add_src_controller',
                    action='store_true',
                    dest="add_src_controller",
                    help='walk through adding a raritan SRC controller to FMS')
    parser.add_option('--check_topology',
                    action='store_true',
                    dest='config_file',
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
    return parser

def main(argv):
    options_parser = SetupOptionParser()
    (options, args) = options_parser.parse_args()

    if options.add_sensor:
        add_fms_sensor()
    elif options.add_src_controller:
        add_src_controller()
    elif options.src_status:
        get_all_src_status() 
    elif options.validate:
        validate() 
    else:
        options_parser.print_help()

main(sys.argv)
