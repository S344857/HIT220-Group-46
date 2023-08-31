import copy

# class for node
class Location:
    def __init__(self, x, y, type):
        # x-coordinate
        self.x = x
        # y-coordinate
        self.y = y
        # type of node
        self.type = type
    
    def __str__(self):
        return "X: "+ str(self.x), "\nY: "+str(self.y),"\nType: " + str(self.type)


class Node:
    def __init__(self, node_name, x, y, type, adjacent):
        # number to present the node
        self.node_name = node_name
        # location data
        self.location = Location(x=x, y=y, type=type)
        # tuple of indeces for adjacent nodes
        self.adjacent = adjacent
        # reference to the next node
        self.next = None
    
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


# A Linked List class with a single head node
class LinkedList:
    def __init__(self):  
      self.head = None

    # insertion method for the linked list
    def insert(self, node):
        new_node = node
        if(self.head):
            current = self.head
            while(current.next):
                current = current.next
            current.next = new_node
        else:
            self.head = new_node

    # print method for the linked list
    def print_linked_list(self):
      current = self.head
      while(current):
        print(current.node_name + '-> ')
        current = current.next

    def get_head(self):
        if(self.head):
            return self.head
        else:
            raise ValueError('The value of head is `None`')


# Graph class
class Graph:
    def __init__(self):
        self.adjacency_list = []

    def add_node(self, node):
        current_list = LinkedList()
        current_list.insert(node)
        self.adjacency_list.append(current_list)

    def add_edges(self, source, destination):
        current_list = self.adjacency_list[source]
        destination_node = copy.deepcopy(self.adjacency_list[destination].get_head())
        current_list.insert(destination_node)

    def check_edge(self, source, destination):
        current_list = self.adjacency_list[source]
        destination_node = self.adjacency_list[destination].get_head()
        current_node = current_list.get_head()
        while current_node:
            if current_node.node_name == destination_node.node_name:
                return True
            current_node = current_node.next
        return False

    def search_node(self, node_name):
        for i in range(len(self.adjacency_list)):
            current_node = self.adjacency_list[i].get_head()
            if current_node.node_name == node_name:
                return i
        return None

    def print(self):
        for current_list in self.adjacency_list:
            current_node = current_list.get_head()
            while current_node:
                print(f'{current_node.node_name} -> ', end="")
                current_node = current_node.next
            print("None")

    def populate_graph(self, data_list):
        for index in data_list:
            self.add_node(node=data_list[index])
           
        
        for i in range(len(self.adjacency_list)):
            temp_node = self.adjacency_list[i].get_head()
            for j in range(len(temp_node.adjacent)):
                destination_name = temp_node.adjacent[j]
                destination_index = self.search_node(destination_name)
                if destination_index is not None:
                    self.add_edges(i, destination_index)


graph = Graph()
graph.populate_graph(nodes_data)
graph.print()