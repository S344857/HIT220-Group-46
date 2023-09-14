    # ------------------------------------------------------------------------------------
    # ASSUMPTIONS
    # ------------------------------------------------------------------------------------
    # 1. Node number 1 is the destination node where all water flows towards: 
    #       - Reason for assumption: Node 1 is placed in the Timor Sea which is the largest notable near-by body of water.
    #       - Rivers in-land are typically at a higher elevation than sea-level and flow toward a lower elevation.
    # 2. The map we have can be represented with a directed tree; all nodes are connected by exactly one path.
    #       - This is necessary, as if there exist multiple paths between two nodes, the direction of all edges may not be determinable based on the data we have.
    #       - This assumption holds true for our map.
    # 3. The range x and y coordinates can only be between the value of 0 to 650, inclusively.
    #       - This assumption holds true in accordance to the provided map.
    # 4. Dam can only be placed in junction node.
    #       - We assume that the junction resets the flow rate to 0, as dam will at least temporarily block any flow in the river below the dam while it is filling.
    #       - Assuming only one dam will be placed at a time.
    #       - We assume that in the funciton `new_flow(dam_x, dam_y)`, which simulates the flow rate of the subiquent nodes flow rate change if a dam is placed before a junciton, takes input of the nearest coordinate to the choosen junction rather then the coordinate for the dam itself.
    # ------------------------------------------------------------------------------------
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
        return f"\nNode: {str(self.node)},\nWeight: {str(self.weight)}, \nFlow_rate: {str(self.flow_rate)}, \nNext: {str(self.next)}\n"

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
        return f"\nX: {str(self.x)},\nY: {str(self.y)}, \nType: {str(self.type)}\n"


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
            raise KeyError("\nSource Node '" + str(source_id) + "' isn't in the graph")
        
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
    
    def is_junction(self, node: int):
        return self.data(node).type == "junction"
    
    def get_junction_list(self):
        temp_list = []
        for node in self.adjacency_list:
            if(self.is_junction(node)):
                if node not in temp_list:
                    temp_list.append(node)
        
        return temp_list

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

                # print(str(search_node) + " =("+str(edge.flow_rate)+")=> " + str(edge.node))

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
    
    # Prints reduction in flow rate at each junction along the river
    def new_flow(self, dam_x: int, dam_y:int):
        junction_to_dam = self.find_closest_junction(dam_x,dam_y)
        if not(self.data(junction_to_dam)):
            print("Junction doesn't exist")
            return

        # Find where the junctions flows towards
        junctions_dest = None
        for edge in LL_as_array(self.data(junction_to_dam))[1:]:
            if self.is_river(junction_to_dam, edge.node):
                junctions_dest = edge.node
                break
        
        if not(junctions_dest):
            print("Node isn't part of a river")
            return
        
        # Find the edge to dam
        for edge in LL_as_array(self.data(junction_to_dam))[1:]:
            if edge.node == junctions_dest:
                edge_to_dam = edge
        
        # Used for reducing flow rate of proceding rivers
        pre_dam_flow = edge_to_dam.flow_rate
        # Dam edge, assume stops all flow
        # edge_to_dam.flow_rate = 0

        print("The following junctions have a decreased flow of: "+str(pre_dam_flow))

        # Traverse down river unill reaching end
        river_path = self.traverse_to_node1(edge_to_dam.node)
        # For ever node that has a proceding node
        for i in range(len(river_path)-1):
            for edge in LL_as_array(self.data(river_path[i]))[1:]:
                # If edge dosen't go to next step in river, skip it
                if edge.node != river_path[i+1]: continue
                # Reduce flow by the amount provided pre-damming
                # edge.flow_rate -= pre_dam_flow
                new_flow_rate = edge.flow_rate - pre_dam_flow
                print(str(river_path[i]) + " (new flow: " + str(new_flow_rate)+")")
                
        
    def find_closest_junction(self, x, y):
        closest_junction = None
        closest_distance = float('inf')

        for node_id in self.adjacency_list:
            node = self.data(node_id)

            # Check if the node is a junction and calculate the distance
            if node.type == "junction":
                distance = self.path_distance(Vertex(x, y, ""), node)

                # Update the closest junction if a closer one is found
                if distance < closest_distance:
                    closest_distance = distance
                    closest_junction = node_id

        return closest_junction
                
    def print_flow_rate(self):
        # Iterate over all nodes
        for node in self.adjacency_list:
            print(str(node), end="")     # Start of path
            # Iterate over all edges
            for edge in LL_as_array(self.data(node))[1:]:
                # print(" -> " + str(edge.node), end="")
                print(f' -> ({edge.node},{edge.flow_rate})', end="")
            # Ends when pointing to null
            print(" -> None")
                

    
    def traverse_to_node1(self, source_node_id):
        # Create an empty list to store the traversed nodes
        traversed_nodes = []

        # Check if the source node exists in the graph
        if source_node_id not in self.adjacency_list:
            print("Source node not found in the graph.")
            return traversed_nodes

        # Initialize a queue for BFS traversal
        queue = [(source_node_id, [source_node_id])]  # Each item in the queue is a tuple (node, path)

        # Create a set to track visited nodes
        visited = set()

        # Perform BFS traversal
        while queue:
            current_node, path = queue.pop(0)
            # print(f'Current node: {current_node} => Path: {path}')
            visited.add(current_node)

            # Check if node 1 is reached
            if current_node == 1:
                traversed_nodes = path
                break

            # Add unvisited neighboring nodes to the queue
            for edge in LL_as_array(self.data(current_node))[1:]:
                 # Ignore non-rivers
                if not(self.is_river(current_node, edge.node)):
                    continue
                # print(f'\n    Edge:{edge}')
                neighbor_node = edge.node
                if neighbor_node not in visited:
                    new_path = path + [neighbor_node]
                    queue.append((neighbor_node, new_path))

        if not traversed_nodes:
            print("Node 1 is not reachable from the source node.")
        return traversed_nodes    
        


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

def validate_coordinate(x_coord, y_coord):
    x_flag = True if x_coord >= 0 and x_coord <= 650 else False
    y_flag = True if y_coord >= 0 and y_coord <= 650 else False
    return x_flag and y_flag


# Create a Graph object
graph = Graph()
# Parse the CSV file's data into graph's adjacency list
parse_csv_into_adjacency_list(graph)

# Populate the distance and flow rate of all paths
graph.populate_distance()
graph.populate_flow_rate()

userchoice = 1
while userchoice != 0:
    userchoice = input("Input betwwen 1 to 4 run the question progream or Input 0 to terminate: ")
    
    # ------------------------------------------------------------------------------------
    # QUESTION NUMBER 1
    # ------------------------------------------------------------------------------------
    if int(userchoice) == 1:
        while True:
            top_left_coord_string = input("Enter the Top-Left Coordinate of the Range as such: \nExample: x_coordinate, y_coordinate: 0,0 \nEnter Data:")
            bottom_right_coord_string = input("Enter the Bottom-Right Coordinate of the Range as such: \nExample: x_coordinate, y_coordinate: 300,300\nEnter Data:")

            temp_value_x = [int(i) for i in top_left_coord_string.split(',')]
            temp_value_y = [int(i) for i in bottom_right_coord_string.split(',')]

            if  validate_coordinate(temp_value_x[0], temp_value_x[1]) and validate_coordinate(temp_value_y[0], temp_value_y[1]):
                top_left_coord = (temp_value_x[0], temp_value_x[1])
                bottom_right_coord = (temp_value_y[0], temp_value_y[1])
                print(graph.junction_sort( top_left_coord, bottom_right_coord ))
                break
            else:
                print("Coordinate range out of bound. Try Again.")
                flag = input("Enter 0 to exit this program or else press enter.")
                if flag == '0':
                    break
        
        
        
    
    
    # ------------------------------------------------------------------------------------
    # QUESTION NUMBER 2
    # ------------------------------------------------------------------------------------
    elif int(userchoice) == 2:
        pass
    
    
    # ------------------------------------------------------------------------------------
    # QUESTION NUMBER 3
    # ------------------------------------------------------------------------------------
    elif int(userchoice) == 3:
        print("Please keep in mind that the coordinate will get the nearest junction regardless of the distance from the coordinate.\nEnter the Coordinate nearest to the dam you want to dam. ")
        x_coord = 0
        y_coord = 0
        while True:
            junction_to_dam = input("\nPlease enter the coordinate as such:\nexample:210,170\nEnter data: ")
            temp_value = [int(i) for i in junction_to_dam.split(',')]
            if validate_coordinate(temp_value[0], temp_value[1]):
                x_coord = temp_value[0]
                y_coord = temp_value[1]
                graph.new_flow(x_coord,y_coord)
                break
            else:
                print("Error: Coordinate out of bound. Try Again.")
                flag = input("Enter 0 to exit this program or else press enter.")
                if flag == '0':
                    break



    
    # ------------------------------------------------------------------------------------
    # QUESTION NUMBER 4
    # ------------------------------------------------------------------------------------
    elif int(userchoice) == 4:
        pass
    
    
    # ------------------------------------------------------------------------------------
    # PROGRAM TERMINATION
    # ------------------------------------------------------------------------------------
    else:
        break


