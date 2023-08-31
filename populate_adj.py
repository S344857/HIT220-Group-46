import math     # For calculating distance 
import csv

CSV_FILE = "data.csv"

class Node:
    def __init__(self, x: int, y: int, type: str, adjacent):
        self.x = x          # Initialize x-coordinate
        self.y = y          # Initialize y-coordinate
        self.type = type    # Initialize type of node
        self.adjacent = adjacent    # Initialize list of adjacent nodes

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

# Stores data about a node's edge
class Edge:
    def __init__(self, node: int, weight: float):
        self.node = node        # Node that it points towards
        self.weight = weight    # Represents distance approximation
        # For our specific data set, each node only links to one other
        #self.next = None

# Using Pythagoras Theorem to approximation lenght of path 
def path_distance(node1: Node, node2: Node):
    return math.sqrt((node2.x - node1.x)**2 + (node2.y - node1.y)**2)


# For each node, point all its connections to itself via an adjacency list
# Do so breadth-first, starting from the destination
def populate_adj(nodes_data: dict, destination: int):
    # Create dictionary to store the edges that each node has
    adjacency_list = {key: None for key in nodes_data}

    # Start search at destination
    to_search = (destination,)
    # Create blacklist for nodes that already face in the correct direction 
    visited = set()
    
    # Process nodes until all have been visited
    while len(visited) < len(adjacency_list):
        # Create list to hold nodes we want to search the next loop
        search_next_loop = []
        # Iterate over all nodes that have been assigned to search
        for search_node in to_search:
            # Iterate over all nodes adjacent to our search node
            for adjacent_node in nodes_data[search_node].adjacent:
                # Visited nodes already point in correct direction so skip them
                if adjacent_node in visited: continue

                # Point the adjacent back to current node
                adjacency_list[adjacent_node] = Edge(search_node, path_distance(nodes_data[adjacent_node], nodes_data[search_node]))
                # Add adjacent to list, in order to search that node during next loop
                search_next_loop.append(adjacent_node)
            # Since we iterated over its adjacent node, add it to our visited blacklist
            visited.add(search_node)
        # Finished search, so next loop search the ones we assigned during current loop
        to_search = tuple(search_next_loop)

    # Sanity tests
    #print(adjacency_list[32].node)
    #print(adjacency_list[54].node)
    #print(adjacency_list[42].node)

    return adjacency_list

# Print out a traversal of the graph from a starting node
def PrintTraversal(adjacency_list: dict, start_node: int):
    # Start iteration from current node's connection
    current_node = adjacency_list[start_node]
    # String with just the starting node
    full_path = str(start_node)
    # Traverse graph from start node until no adjacent
    while current_node:
        # Add the traversal step to the string
        full_path += " --> " + str(current_node.node)
        # Alternative step, includes distance between nodes
        #full_path += " =(" +  str(round(cur_node.weight, 1)) + ")=> " + str(cur_node.node)
        # For next iteration, start from current node's connection
        current_node = adjacency_list[current_node.node]
    
    print(full_path)

# Parse the CSV file into a variable
nodes_data = parse_csv(CSV_FILE)
# Populate the adjacentcy list, and print a traversal
PrintTraversal(populate_adj(nodes_data, 1), 6)