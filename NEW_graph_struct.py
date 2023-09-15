import math     # For calculating distance 
import csv

CSV_FILE = "water_data.csv"

# Used for working out if an edge represents a river
river_types = {"Katherine", "junction", "headwater", "Daley River", "flowgauge"}

source_type = "headwater"


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
            print(node_data)
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
        return self.adjacency_list.get(node_id)

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
    
    # Returns all vertices within a given region
    #top_left/bottom_right: (x, y)
    def vertices_in_region(self, top_left: tuple, bottom_right: tuple):
        if len(top_left) != 2 or len(bottom_right) != 2:
            raise ValueError("Region courner(s) must have two arguments (x, y)")

        in_region = []      # All nodes found within region
        for node in self.adjacency_list:
            if (self.data(node).x >= top_left[0] and self.data(node).x <= bottom_right[0]) and (
                self.data(node).y >= top_left[1] and self.data(node).y <= bottom_right[1]):
                in_region.append(node)
        
        return in_region
    
    def is_river(self, source: int, destination: int):
        # Some paths connect two 'river nodes' but are not rivers
        # so they are manually black listed
        non_river_blacklist = set([ (50,33), (33,50) ])
        # Both nodes must be river types
        if (self.data(destination).type not in river_types) or (
            self.data(source).type not in river_types
        ): return False
        # Rivers can't flow towards a source
        if (self.data(destination).type == source_type) and (
            self.data(destination).next != None ):    # But can to the destination
            return False
        
        # Skip blacklisted paths
        if (source, destination) in non_river_blacklist: return False

        # If it didn't fail the prevous test, it must be a river
        return True

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
        source_flow = 1     # Assume flow

        # Find the number of incoming rivers for every water node
        # and add all source nodes into the search queue for later
        search_queue = []
        incoming_rivers = {}    # Count of incoming river edges
        incoming_flow = {}      # Running sum of incoming flow to a node
        for node in self.adjacency_list:
            # No need to search further if node can't be a river
            if self.data(node).type not in river_types: continue
            # Add source nodes to start BFS at later
            if self.data(node).type == source_type:
                incoming_flow[node] = source_flow
                search_queue.append(node)

            # Iterate over all node's edges
            for edge in LL_as_array(self.data(node))[1:]:
                # Ignore non-rivers
                if not(self.is_river(node, edge.node)):
                    continue

                # Initialize running count, if not done so
                if not(incoming_rivers.get(edge.node)):
                    incoming_rivers[edge.node] = 0
                # Since there is a incoming node
                incoming_rivers[edge.node] += 1
        
        # Breadth-first-search all edges, starting at source nodes
        # Only add node to queue if all incoming edges already searched
        while search_queue:
            search_node = search_queue[0]   # Node is from end of queue
            for edge in LL_as_array(self.data(search_node))[1:]:
                # Skip non-rivers
                if not(self.is_river(search_node, edge.node)):
                    continue

                # Set flow of edge
                edge.flow_rate = incoming_flow[search_node]
                # Initialize edge's running count, if not done so
                if not(incoming_flow.get(edge.node)):
                    incoming_flow[edge.node] = 0
                # Add edges flow to nodes running sum of flow
                incoming_flow[edge.node] += edge.flow_rate

                # Since we visited it, remove it
                incoming_rivers[edge.node] -= 1

                #print(str(search_node) + " =("+str(edge.flow_rate)+")=> " + str(edge.node))

                # Search it next, if we visted all incoming nodes
                if incoming_rivers[edge.node] == 0:
                    search_queue.append(edge.node)
                
            # Since we set all outgoing edges, we don't need it anymore
            incoming_flow.pop(search_node)
            search_queue.pop(0)         # Move the queue foward by one 
    
    # Return junctions in region in order of flow rate (highest to lowest)
    def junction_sort(self, top_left: tuple, bottom_right: tuple):
        # Dictionary of all junctions's flow rate withn a given range
        verticies_dict = {}
        for node in self.vertices_in_region(top_left, bottom_right):
            # Ignore non-junction sources
            if self.data(node).type not in river_types: continue
            # Source isn't a junction
            if self.data(node).type == source_type: continue

            for edge in LL_as_array(self.data(node))[1:]:
                # Ignore non-rivers
                if not(self.is_river(node, edge.node)):
                    continue

                verticies_dict[node] = edge.flow_rate
        #print(verticies_dict)
        # Return sorted in reverse order (highest to lowest)
        return MergedSort_Dict(verticies_dict)[::-1]
        
        


# Add the CSV data into the graph
def parse_csv_into_adjacency_list(graph: Graph):
        # Reading the data from data.csv
        with open(CSV_FILE, mode="r", newline="") as file:
            # read the CSV file and assign to variable
            reader = csv.DictReader(file)
            # iterating over each CSV line
            for row in reader:
                # Get nodes id from file
                node_id =   int(row["Node"])
                # put value None if the linked node is 0 and we assume that the Node 0 means no next adjacent node
                linked = None if int(row["linked"]) == 0 else int(row["linked"])

                # Create dictionary of data from values in file
                vertex_dict = {
                    "node_id":  node_id,
                    "x":        int(row["x"]),
                    "y":        int(row["y"]),
                    "type":     row["type"]
                }
                # Add node if not in graph already, by passing dictionary
                if not(graph.data(node_id)):
                    graph.add_node(vertex_dict)
                # add the linked node to the adjacentcy list
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

# Merge Sort on a dictionaries values
# Returns list of keys, based on their values in ascending order
def MergedSort_Dict(dictionary: dict):
    # Will order array of keys, based on the values
    keys = list(dictionary)   
    # Loop until the sub-array becomes the array
    n = 1       # Len of sub-array ()
    while n < len(keys):
        # Loop through the number of sub-array pairs of lenght n
        for mid_i in range(n, len(keys), n*2):
            # Split into two halfs
            Left = keys[mid_i-n:mid_i]
            Right = keys[mid_i:mid_i+n]

            # Merge by adding smallest un-added element of both arrays
            L_i = R_i = 0       # Index of smallest un-added element
            a_i = mid_i-n       # Index of location in sorting array
            # Until added all values from either sub-array
            while (L_i < len(Left)) and (R_i < len(Right)):
                # Compare dictionary values
                if dictionary[Left[L_i]] <= dictionary[Right[R_i]]:
                    keys[a_i] = Left[L_i]
                    L_i += 1
                else:
                    keys[a_i] = Right[R_i]
                    R_i += 1
                a_i += 1
            # Add left-over elements of Left
            while L_i < len(Left):
                keys[a_i] = Left[L_i]
                L_i += 1
                a_i += 1
            # Add left-over elements of Right
            while R_i < len(Right):
                keys[a_i] = Right[R_i]
                R_i += 1
                a_i += 1
        n += n  # Sub-array size: 1, 2, 4, 8, 16...
    # List of keys, ordered by their values
    return tuple(keys)


# Create a Graph object
graph = Graph()
# Parse the CSV file's data into graph's adjacency list
parse_csv_into_adjacency_list(graph)

# Populate the distance and flow rate of all paths
graph.populate_distance()
graph.populate_flow_rate()

# Print a list of junctions, from highest to smallest flow rate in region
print(graph.junction_sort( (0,0), (300,300) ))


# Print the adjacency list representation of the graph
#graph.print_adjacency_list()

# Print the vertex data stored in the adjacency list
#for key in graph.adjacency_list: print(str(key)+"| \n"+str(graph.adjacency_list[key].next))

# Check if an edge exists between two nodes
#print(graph.check_edge(61,19))
