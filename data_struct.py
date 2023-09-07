import csv
import math

CSV_FILE = "data.csv"

# data for coordinate of nodes
# format => index : Node(node_name, x_coord, y_coord, type_of_node, tuple(adjacenct_vertex_indeces)
nodes_data = {}


# Define a class for the location of a node
class Location:
    def __init__(self, x, y, type):
        # Initialize x-coordinate
        self.x = x
        # Initialize y-coordinate
        self.y = y
        # Initialize type of node
        self.type = type

    # returns a string representation of an object’s state
    def __str__(self):
        return f"X: {str(self.x)},\nY: {str(self.y)},\nType: { str(self.type)}"


# Define a class for a single node in the linked list
class Node:
    def __init__(self, node_name, x, y, type, adjacent):
        # Initialize number to present the node
        self.node_name = node_name
        # Create a Location object with given coordinates and type
        self.location = Location(x=x, y=y, type=type)
        # Initialize a list of indeces for adjacent nodes
        self.adjacent = adjacent
        self.weight = None
        self.flow_rate = None
        # Initialize reference to the next node (linked list pointer)
        self.next = None

    # returns a string representation of an object’s state
    def __str__(self) -> str:
        return f"Node_name: {self.node_name} \nLocation: {self.location} \nAdjacent: {self.adjacent} \nNext: {self.next}"

    # Helper method to return the Class data in Dictionary Format
    def get_data(self):
        return {
            "node_name": self.node_name,
            "x": self.location.x,
            "y": self.location.y,
            "type": self.location.type,
            "adjacent": self.adjacent,
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
    def add_node(self, node):
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
        # get the destination node data in dictionary format
        destination_node_data = self.adjacency_list[destination].get_head().get_data()
        # create a new node with the destination node data
        destination_node = Node(
            destination_node_data["node_name"],
            destination_node_data["x"],
            destination_node_data["y"],
            destination_node_data["type"],
            destination_node_data["adjacent"],
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

    # Using Pythagoras Theorem to approximation lenght of path
    def path_distance(self, node_one: Node, node_two: Node):
        return math.sqrt(
            (node_two.x - node_one.x) ** 2 + (node_two.y - node_one.y) ** 2
        )


class Util:
    def parse_csv(self):
        data_list = {}
        # Reading the data from data.csv
        with open(CSV_FILE, mode="r", newline="") as file:
            reader = csv.DictReader(file)

            for row in reader:
                node_id = int(row["index"])
                x = int(row["x_coord"])
                y = int(row["y_coord"])
                node_type = row["type_of_node"]
                adjacent_points = [
                    int(point) for point in row["adjacent"].split("_")
                ]  # Using split() to read adjacent row
                data_list[node_id] = Node(node_id, x, y, node_type, adjacent_points)
        return data_list


# Instantiate the Util class
util = Util()
# Parsing the CSV file into Node objects
nodes_data = util.parse_csv()
# Create a Graph object
graph = Graph()
# Populate the graph using the given node data
graph.populate_graph(nodes_data)
# Print the adjacency list representation of the graph
graph.print_adjacency_list()
