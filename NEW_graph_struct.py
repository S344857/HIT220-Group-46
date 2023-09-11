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
        # Pointer to the start of the LinkedList, representing the first connected edge
        self.next = None

    def __str__(self):
        return f"X: {str(self.x)},\nY: {str(self.y)}, \nType: {str(self.type)}\n"


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
        tail_edge = LL_as_array(self.data(source_id))[-1]
        # Add to end
        tail_edge.next = edge_to_add

    # Returns the vertex data, easier than keying the adj. list
    def data(self, node_id: int):
        return self.adjacency_list[node_id]

    def check_edge(self, source_id: int, destination_id: int):
        # If source node doesn't exist
        if not(self.adjacency_list.get(source_id)):
            return False
        
        # Search all edges connected to our source
        for connected_edge in LL_as_array(self.data(source_id))[1:]:
            if connected_edge.node == destination_id:
                return True
        # If couldn't find it, it isn't connected 
        return False
    
    def print_adjacency_list(self):
        # Iterate over all nodes
        for node in self.adjacency_list:
            print(str(node), end="")     # Start of path
            # Iterate over all edges
            for edge in LL_as_array(self.data(node))[1:]:
                print(" -> " + str(edge.node), end="")
            # Ends when pointing to null
            print(" -> None")

    def populate_distance(self):
        # Iterate over all nodes
        for node in self.adjacency_list:
            # Iterate over that node's edges
            for edge in LL_as_array(self.data(node))[1:]:
                # Calculate the lenght of path from head node, to connected node
                path_lenght = self.path_distance(self.data(node), self.data(edge.node))
                # Set the edge's weight to that
                edge.weight = path_lenght

    # Using Pythagoras Theorem to approximate lenght of path
    def path_distance(self, node1: Vertex, node2: Vertex):
        return math.sqrt((node2.x - node1.x)**2 + (node2.y - node1.y)**2)
    
    
    def populate_flow_rate(self):
        # Used for working out if an edge represents a river
        river_types = {"Katherine", "junction", "headwater", "Daley River", "flowgauge"}
        source_type = "headwater"
        source_flow = 1     # Assume flow
        # Some paths connect two 'river nodes' but are not rivers
        # so they are manually black listed
        black_list_path = set([ (50,33), (33,50) ])


        # Find the number of incoming rivers for every water node
        # and add all source nodes into the search queue for later
        search_queue = []
        incoming_rivers = {}    # Count of incoming river edges
        for node in self.adjacency_list:
            # Ignore non-rivers
            if self.data(node).type not in river_types: continue
            # Add source nodes to start BFS at later
            if self.data(node).type == source_type:
                search_queue.append(node)

            # Iterate over all node's edges
            for edge in LL_as_array(self.data(node))[1:]:
                # Ignore non-rivers
                if self.data(edge.node).type not in river_types: continue
                # Ignore blacklisted paths
                if (node, edge.node) in black_list_path: continue

                # Initialize running count, if not done so
                if not(incoming_rivers.get(edge.node)):
                    incoming_rivers[edge.node] = []
                incoming_rivers[edge.node].append(node)

        for key in incoming_rivers: print(str(key)+": "+str(incoming_rivers[key]) + str(self.data(key).type))
        #print(search_queue)
        

        while search_queue:
            search_next = []    # Queue for next search
            print(search_queue)
            for search_node in search_queue:
                #print("#" + str(search_node))
                for edge in LL_as_array(self.data(search_node))[1:]:
                    # Skip non-rivers and source types (river can't flow towards a source)
                    if (self.data(edge.node).type not in river_types): continue
                    # Rivers can't flow towards a source
                    if (self.data(edge.node).type == source_type) and (
                        self.data(edge.node).next != None ):    # But not the destination
                        continue
                    # If search_node -> edge_node is blacklisted, skip ut
                    if (search_node, edge.node) in black_list_path:
                        continue

                    # Added flow of one edge
                    print(str(search_node) + " -> " + str(edge.node) + " | " + str(incoming_rivers[edge.node]))
                    # Since we visited it, remove it
                    incoming_rivers[edge.node].remove(search_node)
                    # Search it next, if we visted all incoming nodes
                    if not(incoming_rivers[edge.node]):
                        search_next.append(edge.node)
                    

            print(search_next)
            print(input(""))
            search_queue = search_next
        
        


# Add the CSV data into the graph
def parse_csv_into_adjacency_list(graph: Graph):
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
                linked = None if int(row["linked"]) == 0 else int(row["linked"])

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


# Returns all steps in a LinkedList as an array
def LL_as_array(LinkedList):
    if not hasattr(LinkedList, 'next'):
        raise TypeError("Input isn't a LinkedList")
        
    LL_as_array = []            # Array to all steps
    # Step down LinkedList until pointing towards nothing
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
#graph.populate_flow_rate()

# Print the adjacency list representation of the graph
#graph.print_adjacency_list()

# Print the vertex data stored in the adjacency list
#for key in graph.adjacency_list: print(str(key)+"| \n"+str(graph.adjacency_list[key].next))

# Check if an edge exists between two nodes
print(graph.check_edge(61,19))
