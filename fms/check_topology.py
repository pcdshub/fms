
from happi import Client
import matplotlib.pyplot as plt
import networkx as nx 
fms_happi_database = "fms_test.json"

def check_topology(src_controller, port, client=None):
    if client == None:
        client = Client(path=fms_happi_database)
    print(src_controller)   
    src_controller = client.find_item(name=src_controller)
    curr_sensor_list = getattr(src_controller, "port" + str(port))
    if curr_sensor_list == None:
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

        node_labels[curr_sensor_list[i][sensor_name]] = f"{curr_sensor_list[i][sensor_name]}\n{curr_item.location}\n{curr_item.captar_in}\n{curr_item.captar_out}"
        total_cable_len += curr_sensor_list[i][sensor_eth_dis]
        total_sensors += curr_sensor_list[i][num_sensors]
        if i == len(curr_sensor_list) - 1:
            continue
        edges.append((curr_sensor_list[i][sensor_name], curr_sensor_list[i+1][sensor_name]))
        edge_labels[edges[i]] = curr_sensor_list[i + 1][sensor_eth_dis]

    total_cable_len = "len: " + str(total_cable_len) + "ft" + f"\nMax: {max_cable_len}ft\n"
    total_sensors = "num sens: " + str(total_sensors) + f"\nMax: {max_sensors}"

    totals = total_cable_len + total_sensors
    
    print(f"preparing graph with edges: {edges}")
    G = nx.Graph()
    #G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    pos = nx.spring_layout(G)
    #plt.figure()
    fig, ax = plt.subplots() 
    fig.suptitle(f"{src_controller.name} port: {port}")
    nx.draw(G, pos, with_labels=False, font_weight='bold')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='green')
    nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=9)
    ax.text(0.8,0.10,
        totals,
        horizontalalignment="center",
        verticalalignment="center")
    fig.tight_layout()
    plt.show()