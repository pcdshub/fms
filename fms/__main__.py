import sys, argparse, json
from happi import Client
from .utils import TypeEnforcer as te
from happi.item import OphydItem
from happi.errors import EnforceError
from .happi.containers import FMSRaritanItem, FMSBeckhoffItem, FMSSRCItem
from typing import List
from .check_topology import check_topology
from .grafana import fetch_alert, create_alert_rule, delete_alert_rule
from .serialize_alert import ProvisionedAlertRule, AlertQuery, Model, Evaluator, Operator, Reducer, Query, RelativeTimeRange
from apischema import serialize

fms_happi_database = "fms_test.json"

def create_alert():
    query_model = Model(
        alias_="test1",
        refId="A",
        target="MR1K1:BEND:MMS:XUP.RBV") 

    alert_query = AlertQuery(model=query_model, refId="A")

    classic_model = Model(
        alias_="test2",
        refId='B',
        conditions=[dict(evaluator=Evaluator(params=[38]),
            operator=Operator(),
            query=Query(params=["A"]),
            reducer=Reducer())],
        type_="classic_conditions") 

    classic_query = AlertQuery(
        model=classic_model,
        refId="B",
        datasourceUid="-100",
        relativeTimeRange=RelativeTimeRange(from_=0,to=0))

    alert = ProvisionedAlertRule(
        title="Temperature Raritan MEC",
        ruleGroup="XRT Racks",
        folderUID="FRogdAwGz",
        data=[alert_query, classic_query])

    #with open("test_serial_10.json", "w") as f:
        #f.write(json.dumps(serialize(GrafanaAlert, alert)))

    create_alert_rule(json.dumps(serialize(ProvisionedAlertRule, alert)))

    #this works
    #with open("test_serial_10.json", "r") as f:
    #    create_alert_rule(f.read())

def delete_alert(alert_uid):
    delete_alert_rule(alert_uid)
    

def get_alert(alert_uid):
    alert = fetch_alert(alert_uid)

    print(f"writing alert to file: {alert}")
    with open("sample_alert.txt", "w") as f:
        f.write(alert)


def find_port(name, client=None):
    if client == None:
        client = Client(path=fms_happi_database)
    item = client.find_item(name=name)
    return item.root_sensor_port

def delete_sensor(sensor_name, client=None):
    if client == None:
        client = Client(path=fms_happi_database)
    item = client.find_item(name=sensor_name)

    if type(item) == FMSRaritanItem:
        parent_switch_item = client.find_item(name=item.parent_switch)
        port = "port" + str(item.root_sensor_port)
        sensor_list = getattr(parent_switch_item, port)
        print(f"current list to delete from: {sensor_list}")
        sensor_list = [sensor for sensor in sensor_list if sensor[0] != sensor_name]
        print(f"deleted: {sensor_name} from: {sensor_list}")
        setattr(parent_switch_item, port, sensor_list)
        parent_switch_item.save()

    client.remove_item(item)

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
        curr_sensor_list = getattr(src_controller, port)                
        print(f'Current List: {curr_sensor_list}')

    curr_sensor_list.append((item.name, item.eth_dist_last))
    print(f'Updated List: {curr_sensor_list}')

    setattr(src_controller, port, curr_sensor_list)
    src_controller.save()

def add_fms_sensor(sensor_name=None, client=None):
    container_type = None
    root_sensor_port = None
    eth_dist_last = None
    if sensor_name == None:
        sensor_name = te.get_str("Enter sensor name\n")
        print(sensor_name)
    sensor_type = te.get_list_str(["Beckhoff", "Raritan"], "Enter sensor type Beckhoff/Raritan\n")
    print(sensor_type)
    sensor_prefix = te.get_str("Enter PV")

    if sensor_type == "Raritan":
        parent_switch = te.get_str("Enter a valid Parent SRC Controller happi name:\n")
        print(parent_switch)
        #validate input here
        root_sensor_port = te.get_str("Enter port number if first sensor or leave blank if not")
        print(f"roote sensor port is: {root_sensor_port}")
        last_connection_name = te.get_str("Enter the happi name of the last sensor this one is attached to\n")
        print(f"last conn {last_connection_name}")
        #validate input here
        eth_dist_last = te.get_int("Enter Eth Distance from last sensor\n")
        print(eth_dist_last)
        container_type = FMSRaritanItem
        if (root_sensor_port == "" or root_sensor_port == None) and (last_connection_name == "" or last_connection_name == None):
            raise(EnforceError("must define root_sensor port or last connection"))
    else:
        container_type = FMSBeckhoffItem
    
    if client == None:
        client = Client(path=fms_happi_database)

    item = client.create_item(item_cls=container_type,
        name=sensor_name,
        prefix=sensor_prefix,
        parent_switch=parent_switch,
        root_sensor_port=root_sensor_port,
        eth_dist_last=eth_dist_last,
        last_connection_name=last_connection_name
    )
    if type(item) == FMSRaritanItem:
        ret = add_sensor_to_src(item, client)
    item.save()

def SetupArgumentParser():
    parser = argparse.ArgumentParser(
                        prog="fms",
                        description='A module for managing facillity monitoring devices',
                        epilog='Thank you for using the fms CLI!')
    parser.add_argument('--validate',
                    action='store_true',
                    dest="validate",
                    help='validate database')
    parser.add_argument('--src_status',
                    action='store_true',
                    dest="src_status",
                    help='get src config status')
    parser.add_argument('--add_sensor',
                    dest="add_sensor",
                    help='walk through adding a sensor to FMS')
    parser.add_argument('--add_src_controller',
                    action='store_true',
                    dest="add_src_controller",
                    help='walk through adding a raritan SRC controller to FMS')
    parser.add_argument('--check_topology',
                    action='store_true',
                    dest='check_topology',
                    help='print the current FMS topology')
    parser.add_argument('-s','--src',
                    dest='src_controller',
                    help='src controller')
    parser.add_argument('-p','--port',
                    dest='port',
                    help='src controller port')
    parser.add_argument('-a','--aid',
                    dest='alert_id',
                    help='alert uid')
    parser.add_argument('--list_all_sensors',
                    action='store_true',
                    help="print a list of sensors")
    parser.add_argument('--print_active_alarms',
                    action='store_true',
                    help="prints a list of all alarms")
    parser.add_argument('--launch_nalms',
                    action='store_true',
                    help="launch the nalms home screen")
    parser.add_argument('--delete_sensor',
                    dest='delete_sensor',
                    help="delete_sensor")
    parser.add_argument('--get_alert',
                    action='store_true',
                    help='alert rule id to GET')
    parser.add_argument('--create_alert',
                    action='store_true',
                    help='create alert rule')
    parser.add_argument('--delete_alert',
                    action='store_true',
                    help='delete alert rule')
    return parser

def main(argv):
    argument_parser = SetupArgumentParser()
    options = argument_parser.parse_args()
    print(options)
    if options.add_sensor:
        add_fms_sensor(options.add_sensor)
    elif options.add_src_controller:
        add_src_controller()
    elif options.src_status:
        get_all_src_status() 
    elif options.validate:
        validate() 
    elif options.check_topology:
        check_topology(options.src_controller, options.port)
    elif options.delete_sensor:
        delete_sensor(options.delete_sensor)
    elif options.get_alert:
        get_alert(options.alert_id)
    elif options.create_alert:
        create_alert() 
    elif options.delete_alert:
        delete_alert(options.alert_id) 
    else:
        argument_parser.print_help()

main(sys.argv)
