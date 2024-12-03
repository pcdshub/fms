from happi import Client
from happi.errors import SearchError
from .happi.containers import FMSRaritanItem
from .utils import TypeEnforcer as te

fms_happi_database = "fms_test.json"
sensor_name = 0

def find_port(name, client=None):
    if client == None:
        client = Client(path=fms_happi_database)
    item = client.find_item(name=name)
    return item.root_sensor_port

def add_sensor_to_src(item, client=None):
    if client == None:
        client = Client(path=fms_happi_database)

    src_controller = client.find_item(name=item.parent_switch)
    if item.root_sensor_port == None:
        item.root_sensor_port = find_port(item.last_connection_name, client)
    print(f'Saving Port to Current Item: {item.name}')

    port = "port" + str(item.root_sensor_port)
    curr_sensor_list = getattr(src_controller, port)                
    print(f'Current List: {curr_sensor_list}')

    index = 0
    found = False
    for sensor in curr_sensor_list:
        if sensor[sensor_name] == item.last_connection_name:
            found = True
            break
        else:
            index += 1

    if found:
        curr_sensor_list.insert(index + 1, (item.name, item.eth_dist_last, item.num_sensors))
    else:
        curr_sensor_list.append((item.name, item.eth_dist_last, item.num_sensors))
    print(f'Updated List: {curr_sensor_list}')

    setattr(src_controller, port, curr_sensor_list)
    src_controller.save()

def add_sensor(sensor_name, client):
    if client == None:
        client = Client(path=fms_happi_database)

    sensor_prefix = te.get_str("Enter PV prefix\n")
    sensor_location = te.get_str("Enter rack, stand, or location\n")
    captar_in = te.get_str("Enter Captar # in\n")
    captar_out = te.get_str("Enter Captar # out\n")

    invalid = True
    while(invalid):
        parent_switch = te.get_str("Enter a valid Parent SRC Controller happi name:\n")
        try: 
            client.find_item(name=parent_switch)
            invalid = False
        except SearchError:
            ...
    #validate input here

    root_sensor_port = te.get_str("Enter port number if first sensor or leave blank if not\n")

    invalid = True
    while(invalid):
        last_connection_name = te.get_str("Enter a valid last sensor happi name:\n")
        try: 
            client.find_item(name=last_connection_name)
            invalid = False
        except SearchError:
            if root_sensor_port:
                invalid = False
            ...
    #options

    #validate input here
    eth_dist_last = te.get_int("Enter Eth Distance from last sensor/src\n")
    num_sensors = te.get_int("Enter the number of sensors: DX2-T1H1: 3, DX2-T1: 1, DX2-WSC: 1\n")

    if (root_sensor_port == "" or root_sensor_port == None) and (last_connection_name == "" or last_connection_name == None):
        raise(EnforceError("must define root_sensor port or last connection in feet"))
    

    item = client.create_item(item_cls=FMSRaritanItem,
        name=sensor_name,
        prefix=sensor_prefix,
        parent_switch=parent_switch,
        root_sensor_port=root_sensor_port,
        eth_dist_last=eth_dist_last,
        last_connection_name=last_connection_name,
        num_sensors=num_sensors
    )
    add_sensor_to_src(item, client)
    item.save()