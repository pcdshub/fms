
from happi import Client
import matplotlib.pyplot as plt
import networkx as nx, json

fms_happi_database = "fms_test.json"

def check_topology(src_controller, port, client=None):
    if client == None:
        client = Client(path=fms_happi_database)
    
    src_controller = client.find_item(name=src_controller)
    sensor_list_data = getattr(src_controller, "port" + str(port))
    if sensor_list_data == None:
        print("No sensors installed on this port")
        return
    curr_sensor_list = json.loads(sensor_list_data)
    edges = []
    edge_labels = {}
    node_labels = {}
    total_cable_len = 0
    total_systems = 6
    for i in range(len(curr_sensor_list)):
        node_labels[curr_sensor_list[i][0]] = f"{curr_sensor_list[i][0]}\n\n MEC-PR60-E2"
        total_cable_len += curr_sensor_list[i][1]
        if i == len(curr_sensor_list) - 1:
            continue
        edges.append((curr_sensor_list[i][0], curr_sensor_list[i+1][0]))
        edge_labels[edges[i]] = curr_sensor_list[i + 1][1]
    total_cable_len = "total cable len: " + str(total_cable_len) + "ft" + "\nMax: 100ft"
    
    print(f"preparing graph with edges: {edges}")
    G = nx.Graph()
    #G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    pos = nx.spring_layout(G)
    #plt.figure()
    fig, ax = plt.subplots() 
    nx.draw(G, pos, with_labels=False, font_weight='bold')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='green')
    nx.draw_networkx_labels(G, pos, labels=node_labels)
    ax.text(0.8,0.10,
        total_cable_len,
        horizontalalignment="center",
        verticalalignment="top")
    fig.tight_layout()
    plt.show()