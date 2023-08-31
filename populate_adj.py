import math     # For calculating distance 
import csv

CSV_FILE = "data.csv"

class Node:
    def __init__(self, x: int, y: int, type: str, adjacent):
        self.x = x
        self.y = y
        self.type = type
        self.adjacent = adjacent

# node: (x, y, type, list of adjacent nodes)
nodes_data = {}

def parse_csv(file_name):
    data_list = {}
    # Reading the data from data.csv
    with open(file_name, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            node_id = int(row["index"])
            x = int(row["x_coord"])
            y = int(row["y_coord"])
            node_type = row["type_of_node"]
            adjacent_points = [int(point) for point in row["adjacent"].split('_')] # Using split() to read adjacent row
            data_list[node_id] = Node(x, y, node_type, adjacent_points)
    return data_list

class Edge:
    def __init__(self, node: int, weight: float):
        self.node = node
        self.weight = weight    # Represents distance approximation
        # For our specific data set, each node only links to one other
        #self.next = None

# Using Pythagoras Theorem to approximation lenght of path 
def path_distance(node1: Node, node2: Node):
    return math.sqrt((node2.x - node1.x)**2 + (node2.y - node1.y)**2)


# For each node, point all its connections to itself via an adjacency list
# Do so breadth-first, starting from the destination
def populate_adj(nodes_data: dict, destination: int):

    adjacency_list = {key: None for key in nodes_data}

    # Start search at destination
    to_search = (destination,)
    visited = set()
    
    # Until we have processed all nodes
    while len(visited) < len(adjacency_list):
        search_next_loop = []
        for search_node in to_search:
            # For all nodes connected to our search node
            for adjacent_node in nodes_data[search_node].adjacent:
                # Visited nodes already point in correct direction
                if adjacent_node in visited: continue

                # Link the adjacent back to current node
                adjacency_list[adjacent_node] = Edge(search_node, path_distance(nodes_data[adjacent_node], nodes_data[search_node]))
                search_next_loop.append(adjacent_node)
            visited.add(search_node)
        # Search all adjacent nodes during current loop next 
        to_search = tuple(search_next_loop)

    # Sanity tests
    #print(adjacency_list[32].node)
    #print(adjacency_list[54].node)
    #print(adjacency_list[42].node)

    return adjacency_list

# Print out a traversal of the graph
def PrintTraversal(adjacency_list: dict, start_node: int):
    cur_node = adjacency_list[start_node]
    full_path = str(start_node)
    # Traverse graph from start node until no adjacent
    while cur_node:
        full_path += " --> " + str(cur_node.node)
        #full_path += " =(" +  str(round(cur_node.weight, 1)) + ")=> " + str(cur_node.node)
        cur_node = adjacency_list[cur_node.node]
    
    print(full_path)


nodes_data = parse_csv(CSV_FILE)
PrintTraversal(populate_adj(nodes_data, 1), 6)