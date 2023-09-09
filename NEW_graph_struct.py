import math     # For calculating distance 
import csv

CSV_FILE = "water_data.csv"


# Stores data about an edge in the graph
class Edge:
    def __init__(self, node: int):
        self.node = node            # Node that it points towards
        self.weight = None          # Represents distance approximation
        self.flow_rate = None       # Flow rate of river
        # Link to next edge in LinkedList 
        self.next = None

    def __str__(self):
        return f"Node: {str(self.node)},\nWeight: {str(self.weight)}, \nFlow_rate: {str(self.flow_rate)}, \nNext: {str(self.next)}\n"

# Stores data about a node/vertex in the graph
# Node ID is not stored here as it will be the key of the adjacency list
class Vertex:
    def __init__(self, x: int, y: int, type: str):
        self.x = x
        self.y = y
        self.type = type            # Type of location vertex represents
        self.incoming_edges = 0     # Number of edges pointing towards it
        # Pointer to the start of the LinkedList, representing the first connected edge
        self.next = None

    def __str__(self):
        return f"X: {str(self.x)},\nY: {str(self.y)}, \nType: {str(self.type)}, \nIncoming: {str(self.incoming_edges)}\n"


class Graph:
    def __init__(self):
        # Dictionary that stores the adjacency list representation
        # FORMAT|| node_id: vertex_data -> edge1 -> edge2...
        self.adjacency_list = {}

    
    def add_node(self, node_data: dict):
        # If node has already been added
        if self.adjacency_list.get(node_data["node_id"]):
            print("Error: Node is already in graph")
            return
        
        # Add a Vertex class object to adjacency list, with the key being the node's ID
        self.adjacency_list[node_data["node_id"]] = Vertex(node_data["x"], node_data["y"], node_data["type"])


    def add_edge(self, source_id: int, edge_to_add: Edge):
        # If source node doesn't exist
        if self.adjacency_list.get(source_id) is None:
            raise KeyError("Source Node '" + str(source_id) + "' isn't in the graph")
        
        # Get the end of the source id's LinkedList
        tail_edge = LL_as_array(self.adjacency_list[source_id])[-1]
        # Add to end
        tail_edge.next = edge_to_add

    def check_edge(self, source_id: int, destination_id: int):
        # If source node exists
        if not(self.adjacency_list.get(source_id)):
            return False
        
        # Search all edges connected to our source 
        for connected_edge in LL_as_array(self.adjacency_list[source_id])[1:]:
            if connected_edge.node == destination_id:
                return True
        # If prevous steps couldn't find, it isn't connected 
        return False
    
    def print_adjacency_list(self):
        # Iterate over all nodes
        for node in self.adjacency_list:
            linked_path = str(node)     # Start of path
            # Iterate over all edges
            for edge in LL_as_array(self.adjacency_list[node])[1:]:
                # Add to path
                linked_path += " -> " + str(edge.node)
            # Print the full path, ending when next points to null
            print(linked_path + " -> None")

    def populate_distance(self):
        # Iterate over all nodes
        for node in self.adjacency_list:
            # Iterate over that node's edges
            for edge in LL_as_array(self.adjacency_list[node])[1:]:
                # Calculate the lenght of path from head node, to connected node
                path_lenght = self.path_distance(self.adjacency_list[node], self.adjacency_list[edge.node])
                # Set the edge's weight to that
                edge.weight = path_lenght

    # Using Pythagoras Theorem to approximate lenght of path
    def path_distance(self, node1: Vertex, node2: Vertex):
        return math.sqrt((node2.x - node1.x)**2 + (node2.y - node1.y)**2)



# Add the CSV data into the graph
def parse_csv_into_adjacency_list(graph: Graph):
        # Running count of incoming edges to a node
        # Needed as node may not have been added yet
        incoming_count = {}

        # Reading the data from data.csv
        with open(CSV_FILE, mode="r", newline="") as file:
            # read the CSV file and assign to variable
            reader = csv.DictReader(file)

            # iterating over each CSV line
            for row in reader:
                # assigning values from file to variables
                node_id =   int(row["Node"])
                x =         int(row["x"])
                y =         int(row["y"])
                node_type = row["type"]

                # put value None if the linked node is 0 and we assume that the Node 0 means no next adjacent node
                if int(row["linked"]) == 0:
                    linked = None
                else:
                    linked = int(row["linked"])
                    # Since there is a linked node, add to its running count
                    # Initialise, if not done so already
                    if not(incoming_count.get(linked)): incoming_count[linked] = 0
                    incoming_count[linked] += 1     # Add to running count

                # if connected node already exists
                if graph.adjacency_list.get(linked) is not None:
                    # set the incoming node count to current running count
                    graph.adjacency_list[linked].incoming_edges = incoming_count[linked]

                # if the node already exists
                if graph.adjacency_list.get(node_id) is not None:
                    # set running count of incoming nodes
                    # Initialise count, if not done so already
                    if not(incoming_count.get(node_id)):
                        incoming_count[node_id] = 0
                    graph.adjacency_list[node_id].incoming_edges = incoming_count[node_id]
                
                # if node is not present in graph
                else:
                    # Create dictionary of the node's data
                    vertex_dict = {
                        "node_id": node_id,
                        "x": x,
                        "y": y,
                        "type": node_type
                    }
                    # Add node, by passing dictionary
                    graph.add_node(vertex_dict)
                # add the linked node to the adjacent node
                if linked: graph.add_edge(node_id, Edge(linked))


# Returns all steps of in a LinkedList as an array
def LL_as_array(LinkedList):
    if not hasattr(LinkedList, 'next'):
        raise TypeError("Input isn't a LinkedList")
        
    LL_as_array = []            # Array to all steps
    # Step down LinkedList until reaching empty 
    cur_node = LinkedList
    while cur_node:
        LL_as_array.append(cur_node)    # Add each step to list
        cur_node = cur_node.next
    
    return tuple(LL_as_array)


# Create a Graph object
graph = Graph()
# Parse the CSV file's data into graph's adjacency list
parse_csv_into_adjacency_list(graph)
# Populate the distance of all paths
graph.populate_distance()

# Print the adjacency list representation of the graph
graph.print_adjacency_list()

# Print the vertex data stored in the adjacency list
#for key in graph.adjacency_list: print(str(key)+"| \n"+str(graph.adjacency_list[key]))

# Check if an edge exists between two nodes
print(graph.check_edge(61,19))
