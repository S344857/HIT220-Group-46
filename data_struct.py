import csv
import math

CSV_FILE = "water_data.csv"

# data for coordinate of nodes
# format => index : Node(node_name, x_coord, y_coord, type_of_node, tuple(adjacenct_vertex_indeces)
nodes_data = {}


# Define a class for the location of a node
class Location:
    def __init__(self, x, y):
        # Initialize x-coordinate
        self.x = x
        # Initialize y-coordinate
        self.y = y

    # returns a string representation of an object’s state
    def __str__(self):
        return f"X: {str(self.x)},\nY: {str(self.y)}"


# Define a class for a single node in the linked list
class Node:
    def __init__(self, node_name, x, y, type, adjacent, incoming_edges=0, distance=None, flow_rate=None):
        # Initialize number to present the node
        self.node_name = node_name
        # Create a Location object with given coordinates and type
        self.location = Location(x=x, y=y)
        # Initialize a list of indeces for adjacent nodes
        self.adjacent = adjacent
        self.type = type
        # Stores the number of incoming edges
        self.incoming_edges = incoming_edges

        # Edge data
        self.distance = distance
        self.flow_rate = flow_rate
        # Initialize reference to the next node (linked list pointer)
        self.next = None

    # returns a string representation of an object’s state
    def __str__(self) -> str:
        return f"Node_name: {self.node_name} \nLocation: {self.location} \nIncoming: {self.incoming_edges} \nAdjacent: {self.adjacent} "

    # Helper method to return the Class data in Dictionary Format
    def get_data(self):
        return {
            "node_name": self.node_name,
            "x": self.location.x,
            "y": self.location.y,
            "type": self.type,
            "incoming_edges": self.incoming_edges,
            "adjacent": self.adjacent,
            "distance": self.distance,
            "flow_rate": self.flow_rate
        }


# Class for a linked list of nodes
class LinkedList:
    def __init__(self):
        # Initialize the head of the linked list
        self.head = None

    # Method to insert a node at the end of the linked list
    def insert(self, node):
        # Create a new_node with the given node
        new_node = node
        # If the linked list is not empty
        if self.head:
            # Initially assign the head value to current node
            current = self.head
            # Traverse to the end of the linked list
            while current.next:
                # Traverse to the next node until 'None' is encountered
                current = current.next
            # Add the new node to the end
            current.next = new_node
        else:
            # If the linked list is empty, set the new node as the head
            self.head = new_node

    # Method to print the linked list
    def print_linked_list(self):
        # Initially assign the head value to current node
        current = self.head
        # Traverse and print each node in the linked list
        while current:
            print(current.node_name + "-> ")
            current = current.next

    # Method to get the head node of the linked list
    def get_head(self):
        # Return the head node if it exists
        if self.head:
            return self.head
        # Else raise an error
        else:
            raise ValueError("The value of head is `None`")


# Class representing a graph
class Graph:
    def __init__(self):
        # Initialize an empty list to store linked lists (adjacency lists)
        self.adjacency_list = []

    # Method to add a node to the graph
    def add_node(self, node: Node):
        # Create a new linked list and insert the node
        current_list = LinkedList()
        # insert the new node to the linked list
        current_list.insert(node)
        # Add the linked list to the adjacency list
        self.adjacency_list.append(current_list)

    # Method to add edges between nodes in the graph
    def add_edges(self, source, destination):
        # Get the source linked list
        current_list = self.adjacency_list[source]

        # get source node head
        current_head_node = current_list.get_head()

        # get destination node head
        destination_node_head = self.adjacency_list[destination].get_head()

        # get the destination node data in dictionary format
        destination_node_data = destination_node_head.get_data()

        # get the distance between the source and destination nodes
        distance = self.path_distance(current_head_node, destination_node_head)

        # calculate distance between the destination node and the head node in the lined lislt

        # create a new node with the destination node data
        destination_node = Node(
            node_name=destination_node_data["node_name"],
            x=destination_node_data["x"],
            y=destination_node_data["y"],
            type=destination_node_data["type"],
            adjacent=destination_node_data["adjacent"],
            distance=distance,
        )
        # insert the edge end node to the adjacency list
        current_list.insert(destination_node)

    # Method to check if an edge exists between two nodes
    def check_edge(self, source, destination):
        # Get the source linked list
        current_list = self.adjacency_list[source]
        # Get the destination node
        destination_node = self.adjacency_list[destination].get_head()
        # get the head node of the source adjacency list
        current_node = current_list.get_head()
        # Traverse the source linked list to check for the destination node
        while current_node:
            # return True if the node_name / node / index matches
            if current_node.node_name == destination_node.node_name:
                return True
            # continue traversal with the use of reference to the next node
            current_node = current_node.next
        # return False if no result is obtained after full traversal of the linked list
        return False

    # Method to search for a node in the graph and return its index
    def search_node(self, node_name):
        # Iterating over the adjacency list
        for i in range(len(self.adjacency_list)):
            # Get the head node of the iterated linked list
            current_node = self.adjacency_list[i].get_head()
            # if the node_name / index / code matches of the input value
            if current_node.node_name == node_name:
                # return the index
                return i
        # Return None if the input value is not found
        return None

    # Method to print the adjacency list representation of the graph
    def print_adjacency_list(self):
        # Iterating over the Adjacency List
        for current_list in self.adjacency_list:
            # Assign current node with the head node of each Linked List
            current_node = current_list.get_head()
            # Iterating as long as None is not encountered
            while current_node:
                # Print the current node_name / index / code
                print(f"{current_node.node_name} -> ", end="")
                # reference to the next node in the Linked List
                current_node = current_node.next
            # Print to denote the end of the Linked List
            print("None")

    # Method to populate the graph using the given data
    def populate_graph(self, data_list):
        # Add nodes to the graph
        # Iterating over the Input list
        for index in data_list:
            # Add node to Graph
            self.add_node(node=data_list[index])

        # Add edges to the graph based on the adjacent vertices
        # Iterating over the adjacent of each of the Head node of the Linked Lists
        for i in range(len(self.adjacency_list)):
            # Assign the head node to a temporary varaible
            temp_node = self.adjacency_list[i].get_head()
            # Iterating over the adjacent node_name / code / index of the node
            for j in range(len(temp_node.adjacent)):
                # Assign the node_name / code / index to a variable
                destination_name = temp_node.adjacent[j]
                # search for the index of the input node_name / code / index and get it's index in the adjacency_list
                destination_index = self.search_node(destination_name)
                # if the return index value is not None (Not Found in the adjacency_list)
                if destination_index is not None:
                    # add the edge from the current node to the destination node
                    self.add_edges(i, destination_index)

    # function using Pythagoras Theorem to approximation lenght of path
    def path_distance(self, node_one: Node, node_two: Node):
        return math.sqrt(
            (node_two.location.x - node_one.location.x) ** 2
            + (node_two.location.y - node_one.location.y) ** 2
        )


    # Function populates the flow rate of all edges
    def populate_flow_rate(self):
        # Used for working out if an edge represents a river
        river_types = {"Katherine", "junction", "headwater", "Daley River", "flowgauge"}
        source_type = "headwater"
        source_flow = 1     # Assume flow
        # Store the running sum of incoming flow for each node
        # Finding income edges, to sum flow, you need to search all vertex+edges
        node_flow = {}

        print("Populating flow rate...")
        # Get all source nodes, to start search at
        search_queue = []
        for node in graph.adjacency_list:
            node_flow[node.head.node_name] = 0   # Initialize flow to be zero
            if node.head.type == source_type:
                search_queue.append(node.head)

        # Peforms a BFS, starting from source nodes
        visited = set()
        while search_queue:
            print(search_queue[0].node_name)
            # Iterate over connected nodes
            connected = search_queue[0].next
            while connected:
                # Skip non-river edges and visited nodes
                if (connected.type not in river_types) or (connected.node_name in visited):
                    connected = connected.next
                    continue

                if search_queue[0].type == source_type:
                    node_flow[connected.node_name] += source_flow
                    connected.flow_rate = source_flow
                else:
                    
                    connected.flow_rate

                print(" -> " + str(connected.node_name) + " | " + str(connected.flow_rate))
                #search_queue.append(node.head.node_name)
                connected = connected.next
            search_queue.pop(0)
            
        

    def sort_flow_rate():
        pass

# Class containing helper functions
class Util:
    # function to parse the CSV file to Map data type
    def parse_csv(self):
        data_list = {}
        # number of incoming edges to a node
        # Needed as node may not have been added yet
        incoming_count = {}

        # Reading the data from data.csv
        with open(CSV_FILE, mode="r", newline="") as file:
            # read the CSV file and assign to variable
            reader = csv.DictReader(file)

            # iterating over each of the CSV line
            for row in reader:
                # assigning values from file to variables
                node_id = int(row["Node"])
                x = int(row["x"])
                y = int(row["y"])
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
                if data_list.get(linked) is not None:
                    # set the incoming node count to current running count
                    data_list[linked].incoming_edges = incoming_count[linked]

                # if the node already exists
                if data_list.get(node_id) is not None:
                    # add the linked node to the adjacent node list
                    data_list[node_id].adjacent.append(linked)

                    # add running count of incoming nodes
                    # Initialise count, if not done so already
                    if not(incoming_count.get(node_id)):
                        incoming_count[node_id] = 0
                    data_list[node_id].incoming_edges = incoming_count[node_id]
                
                # if node is not present in the data_list
                else:
                    # add the node to the data_list
                    data_list[node_id] = Node(node_id, x, y, node_type, [linked])
        
        #for line in incoming_count:
        #    print(str(line)+": "+str(incoming_count[line]))
        # return the data_list variable
        return data_list


# Instantiate the Util class
util = Util()
# Parsing the CSV file into Node objects
nodes_data = util.parse_csv()
# Create a Graph object
graph = Graph()
# Populate the graph using the given node data
graph.populate_graph(nodes_data)
#for node_id in nodes_data: print(str(nodes_data[node_id]) + "\n")


graph.adjacency_list[1].head.node_name = 999
# Print the adjacency list representation of the graph
graph.print_adjacency_list()



#print(graph.adjacency_list[2].head.next)
#graph.populate_flow_rate()



"""
river_types = {"Katherine", "junction", "headwater", "Daley River"}
for entry in graph.adjacency_list:
    if entry.head.type != "headwater": continue
    node = entry.head
    print(str(entry.head.node_name))
    while node.next:
        print(
            "   ("+ str(entry.head.type)  + ") -> "
            + str(node.next.node_name) +" ("+ str(node.next.type) + ")"
            )
        node = node.next
"""
