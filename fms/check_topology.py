import os

import matplotlib.pyplot as plt
import networkx as nx
from happi import Client

fms_happi_database = os.environ["HAPPI_CFG"]

with open(fms_happi_database, "r") as file:
    lines = file.readlines()
    for line in lines:
        if "path" in line:
            fms_happi_database = line.split("=")[1].strip()


def check_topology(src_controller, port, client=None):
    """Take an src controller name and port and creates
    a networkx topology graph. Keeps a running total
    of Ethernet length and sensors installed.

    Args:
        src_controller (str):
            Name of the SRC800 Controller.
        port (int):
            Sensor port number 0 indexed; actually 1 indexed on
            controller.
        client (str, optional):
            The path to the happi database. Defaults to None.
    """
    if client is None:
        client = Client(path=fms_happi_database)
    print(src_controller)
    src_controller = client.find_item(name=src_controller)
    curr_sensor_list = getattr(src_controller, "port" + str(port))
    if curr_sensor_list is None:
        print("No sensors installed on this port")
        return
    edges = []
    edge_labels = {}
    node_labels = {}
    total_cable_len = 0
    total_sensors = 0
    max_cable_len = 100
    max_sensors = 36

    sensor_name = 0
    sensor_eth_dis = 1
    num_sensors = 2

    print(curr_sensor_list)
    for i in range(len(curr_sensor_list)):
        curr_item = client.find_item(name=curr_sensor_list[i][sensor_name])

        node_labels[curr_sensor_list[i][sensor_name]] = (
            f"{curr_sensor_list[i][sensor_name]}\n{curr_item.location}\n{curr_item.captar_in}\n{curr_item.captar_out}"
        )
        total_cable_len += curr_sensor_list[i][sensor_eth_dis]
        total_sensors += curr_sensor_list[i][num_sensors]
        if i == len(curr_sensor_list) - 1:
            continue
        edges.append(
            (curr_sensor_list[i][sensor_name], curr_sensor_list[i + 1][sensor_name])
        )
        edge_labels[edges[i]] = curr_sensor_list[i + 1][sensor_eth_dis]
    print(node_labels)
    total_cable_len = (
        "len: " + str(total_cable_len) + "ft" + f" Max: {max_cable_len}ft\n"
    )
    total_sensors = "num sens: " + str(total_sensors) + f" Max: {max_sensors}"

    totals = total_cable_len + total_sensors

    print(f"preparing graph with edges: {edges}")
    G = nx.Graph()

    G.add_edges_from(edges)
    pos = nx.spring_layout(G)

    fig, ax = plt.subplots()
    fig.suptitle(f"{src_controller.name} port: {port}\n {totals}")
    width, height = fig.get_size_inches()

    if len(pos) == 0:
        # no edges
        G.add_node(src_controller.name)
        pos[curr_sensor_list[i][sensor_name]] = (0.5, 0.5)

    nx.draw(G, pos, with_labels=False, font_weight="bold")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color="green")
    print(f"drawing node labels: {node_labels}")
    nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=9)

    fig.tight_layout()
    plt.show()
