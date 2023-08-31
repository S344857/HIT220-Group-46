import copy

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
        return "X: "+ str(self.x), "\nY: "+str(self.y),"\nType: " + str(self.type)

# Define a class for a single node in the linked list
class Node:
    def __init__(self, node_name, x, y, type, adjacent):
        # Initialize number to present the node
        self.node_name = node_name
        # Create a Location object with given coordinates and type
        self.location = Location(x=x, y=y, type=type)
        # Initialize a list of indeces for adjacent nodes
        self.adjacent = adjacent
        # Initialize reference to the next node (linked list pointer)
        self.next = None
        
    # returns a string representation of an object’s state
    def __str__(self) -> str:
        return f'Node_name: {self.node_name} \nLocation: {self.location} \nAdjacent: {self.adjacent} \nNext: {self.next}'


# data for coordinate of nodes
# format => index : Node(node_name, x_coord, y_coord, type_of_node, tuple(adjacenct_vertex_indeces)
nodes_data = {
    1: Node(1, 70, 100, "headwater", [42]),
    2: Node(2, 230, 190, "junction", [19, 35, 36]),
    3: Node(3, 120, 255, "headwater", [42]),
    4: Node(4, 120, 275, "headwater", [33]),
    5: Node(5, 195, 320, "headwater", [34]),
    6: Node(6, 225, 370, "headwater", [40]),
    7: Node(7, 230, 420, "headwater", [40]),
    8: Node(8, 260, 465, "headwater", [43]),
    9: Node(9, 315, 460, "headwater", [43]),
    10: Node(10, 325, 500, "headwater", [44]),
    11: Node(11, 350, 495, "headwater", [44]),
    12: Node(12, 355, 215, "headwater", [44]),
    13: Node(13, 380, 570, "headwater", [47]),
    14: Node(14, 360, 410, "headwater", [48]),
    15: Node(15, 385, 390, "headwater", [48]),
    16: Node(16, 245, 335, "headwater", [37]),
    17: Node(17, 225, 240, "headwater", [59]),
    18: Node(18, 240, 140, "headwater", [35]),
    19: Node(19, 330, 185, "headwater", [2]),
    20: Node(20, 330, 200, "headwater", [36]),
    21: Node(21, 340, 215, "headwater", [57]),
    22: Node(22, 365, 180, "headwater", [57]),
    23: Node(23, 430, 180, "headwater", [58]),
    24: Node(24, 451, 200, "headwater", [58]),
    25: Node(25, 430, 230, "headwater", [55]),
    26: Node(26, 451, 220, "headwater", [52]),
    27: Node(27, 425, 260, "headwater", [51]),
    28: Node(28, 410, 230, "headwater", [51]),
    29: Node(29, 520, 275, "headwater", [45]),
    30: Node(30, 570, 210, "headwater", [53]),
    31: Node(31, 510, 120, "headwater", [54]),
    32: Node(32, 520, 80, "headwater", [54]),
    33: Node(33, 150, 180, "junction", [34, 42, 4]),
    34: Node(34, 170, 210, "junction", [5, 33, 59]),
    35: Node(35, 230, 190, "junction", [2, 18, 59]),
    36: Node(36, 270, 250, "junction", [2, 20, 37]),
    37: Node(37, 280, 270, "junction", [16, 36, 39]),
    38: Node(38, 325, 335, "junction", [39, 41, 49]),
    39: Node(39, 320, 290, "junction", [37, 38, 55]),
    40: Node(40, 265, 360, "junction", [6, 7, 41]),
    41: Node(41, 290, 360, "junction", [38, 40, 43]),
    42: Node(42, 125, 100, "junction", [1, 3, 33]),
    43: Node(43, 310, 390, "junction", [8, 9, 41]),
    44: Node(44, 395, 450, "junction", [10, 11, 12, 47]),
    45: Node(45, 380, 340, "junction", [29, 46, 47]),
    46: Node(46, 380, 340, "junction", [50, 45, 49]),
    47: Node(47, 410, 430, "junction", [44, 13, 45]),
    48: Node(48, 350, 360, "junction", [49, 14, 15]),
    49: Node(49, 350, 350, "junction", [48, 46, 38]),
    50: Node(50, 425, 290, "junction", [46, 51, 52]),
    51: Node(51, 430, 280, "junction", [50, 27, 28]),
    52: Node(52, 450, 260, "junction", [26, 53, 50]),
    53: Node(53, 520, 250, "junction", [54, 30, 52]),
    54: Node(54, 540, 180, "junction", [31, 32, 53]),
    55: Node(55, 360, 260, "junction", [56, 25, 39]),
    56: Node(56, 370, 230, "junction", [57, 58, 55]),
    57: Node(57, 370, 220, "junction", [21, 22, 56]),
    58: Node(58, 380, 230, "junction", [56, 23, 24]),
    59: Node(59, 190, 205, "junction", [34, 35, 17]),
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
        if(self.head):
            # Initially assign the head value to current node 
            current = self.head
            # Traverse to the end of the linked list
            while(current.next):
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
        while(current):
          print(current.node_name + '-> ')
          current = current.next

    # Method to get the head node of the linked list
    def get_head(self):
        # Return the head node if it exists
        if(self.head):
            return self.head
        # Else raise an error
        else:
            raise ValueError('The value of head is `None`')


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
        # Deep copy the destination node and insert it into the source linked list
        # deep copy is used to prevent the usage of same reference node objects and creating a infinite traversal bug
        destination_node = copy.deepcopy(self.adjacency_list[destination].get_head())
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
                print(f'{current_node.node_name} -> ', end="")
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

# Create a Graph object
graph = Graph()
# Populate the graph using the given node data
graph.populate_graph(nodes_data)
# Print the adjacency list representation of the graph
graph.print_adjacency_list()