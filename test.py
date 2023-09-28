import math
import csv

CSV_FILE = "water_data.csv"
river_types = {
    "Katherine",
    "junction",
    "headwater",
    "Daley River",
    "flowgauge",
    "sea entrance",
}
source_type = "headwater"

class Edge:
    def __init__(self, node: int):
        self.node = node
        self.weight = None
        self.flow_rate = None
        self.next = None

class Vertex:
    def __init__(self, x: int, y: int, type: str):
        self.x = x
        self.y = y
        self.type = type
        self.next = None

class Graph:
    def __init__(self):
        self.adjacency_list = {}

    def add_node(self, node_data: dict):
        if self.adjacency_list.get(node_data["node_id"]):
            print("Error: Node is already in graph")
            print(node_data)
            return
        self.adjacency_list[node_data["node_id"]] = Vertex(
            node_data["x"], node_data["y"], node_data["type"]
        )

    def add_edge(self, source_id: int, edge_to_add: Edge):
        if self.adjacency_list.get(source_id) is None:
            raise KeyError("\nSource Node '" + str(source_id) + "' isn't in the graph")
        tail_edge = LL_as_array(self.data(source_id))[-1]
        tail_edge.next = edge_to_add

    def data(self, node_id: int):
        return self.adjacency_list.get(node_id)

    def check_edge(self, source_id: int, destination_id: int):
        if not (self.adjacency_list.get(source_id)):
            return False
        for connected_edge in LL_as_array(self.data(source_id))[1:]:
            if connected_edge.node == destination_id:
                return True
        return False

    def is_river(self, source: int, destination: int):
        non_river_blacklist = set([(50, 33), (33, 50)])
        if (self.data(destination).type not in river_types) or (
            self.data(source).type not in river_types
        ):
            return False
        if self.data(destination).type == source_type:
            return False
        if (source, destination) in non_river_blacklist:
            return False
        return True

    def is_junction(self, node: int):
        return self.data(node).type == "junction"

    def populate_distance(self):
        for node in self.adjacency_list:
            for edge in LL_as_array(self.data(node))[1:]:
                path_lenght = self.path_distance(self.data(node), self.data(edge.node))
                edge.weight = path_lenght

    def path_distance(self, node1: Vertex, node2: Vertex):
        return math.sqrt((node2.x - node1.x) ** 2 + (node2.y - node1.y) ** 2)

    def populate_flow_rate(self):
        source_flow = 1
        search_queue = []
        incoming_rivers = {}
        incoming_flow = {}
        for node in self.adjacency_list:
            if self.data(node).type not in river_types:
                continue
            if self.data(node).type == source_type:
                incoming_flow[node] = source_flow
                search_queue.append(node)
            for edge in LL_as_array(self.data(node))[1:]:
                if not (self.is_river(node, edge.node)):
                    continue
                if not (incoming_rivers.get(edge.node)):
                    incoming_rivers[edge.node] = 0
                incoming_rivers[edge.node] += 1

        while search_queue:
            search_node = search_queue[0]
            for edge in LL_as_array(self.data(search_node))[1:]:
                if not (self.is_river(search_node, edge.node)):
                    continue
                edge.flow_rate = incoming_flow[search_node]
                if not (incoming_flow.get(edge.node)):
                    incoming_flow[edge.node] = 0
                incoming_flow[edge.node] += edge.flow_rate
                incoming_rivers[edge.node] -= 1
                if incoming_rivers[edge.node] == 0:
                    search_queue.append(edge.node)
            incoming_flow.pop(search_node)
            search_queue.pop(0)

    def find_closest_junction(self, x, y):
        closest_junction = None
        closest_distance = float("inf")
        for node_id in self.adjacency_list:
            node = self.data(node_id)
            if node.type == "junction":
                distance = self.path_distance(Vertex(x, y, ""), node)
                if distance < closest_distance:
                    closest_distance = distance
                    closest_junction = node_id
        return closest_junction
  
    def distance_to_headwater(self, junction, headwater):
        """Calculate the distance (number of steps) from a junction to a headwater."""
        
        # Initialize the distance counter to zero
        distance = 0
        
        # Starting from the given junction
        current_node = junction
        # Keep track of visited nodes to avoid cycles or infinite loops
        visited = set()
        
        # Keep looking for the headwater until we find it or until we traverse all nodes
        while current_node != headwater and current_node not in visited:
            
            # Mark the current node as visited
            visited.add(current_node)
            
            # If the current node is not in the adjacency list or has no downstream connections
            if current_node not in self.adjacency_list or not self.adjacency_list[current_node]:
                return float('inf')  # Mark it as unreachable and return a large number
             
            
            # Move to the downstream node
            # current_node = self.adjacency_list[current_node][0]
            
            data_output = self.data(current_node)
            ll_array = LL_as_array(data_output)
            
            if len(ll_array) > 1:
                current_node = ll_array[1].node
            else:
                # Handle the error case
                # print("Unexpected length for LL_as_array output!")
                return float('inf')
            # current_node = LL_as_array(self.data(current_node))[1].node
            
            # Increment the distance counter
            distance += 1
        
        # If we found the headwater, return the calculated distance
        if current_node == headwater:
            return distance
        
        # Otherwise, return that it's unreachable
        return float('inf')
    
    def is_headwater(self, node_id):
        if self.data(node_id).type == "headwater":
            return True
        elif self.data(node_id).type == None:
            return False
        else:
            return False
    
    def trace_path_to_headwater(self, junction):
        """Trace back from a junction to its potential headwater sources."""
        sources = []
        stack = [junction]
        visited = set()

        while stack:
            current = stack.pop()
            visited.add(current)

            # Check if current is a headwater
            if self.is_headwater(current):
                sources.append(current)
                continue

            # Extract adjacent nodes
            adjacent_nodes = ll_as_array(self.data(current))

            # Add all upstream nodes to the stack
            for upstream_node in adjacent_nodes:
                if upstream_node not in visited:
                    stack.append(upstream_node)

        return sources


    def chemical_source(self, sequence):
        # Create a set of junctions to consider
        to_consider = set(j[0] for j in sequence)

        # Filter out downstream contaminated junctions
        for j, conc in sequence:
            for other_j, other_conc in sequence:
                # If we find an upstream junction with a higher concentration
                if j != other_j and other_conc > conc and self.distance_to_headwater(j, other_j) != float('inf'):
                    # Remove the current junction from consideration
                    to_consider.discard(j)
                    break

        # Create a dictionary to store the distances to each headwater
        distances = {}
        for j in to_consider:
            # For each junction, trace the path to its headwaters
            for hw in self.trace_path_to_headwater(j):
                # If the headwater is not already in the distances dictionary, add it
                if hw not in distances:
                    distances[hw] = []
                # Calculate the distance from the current junction to the headwater and append it to the list
                distances[hw].append(self.distance_to_headwater(j, hw))
                
        # Initialize the likely source to be None and the minimum sum of distances to be a large number
        source = []
        min_distance_sum = float('inf')
        # For each headwater and its list of distances
        for hw, d_list in distances.items():
            # Calculate the sum of squared distances
            distance_sum = sum(d**2 for d in d_list)
            # If this sum is smaller than the current minimum
            if distance_sum < min_distance_sum:
                # Update the source to be the current headwater
                source = [hw]
                # Update the minimum sum of distances
                min_distance_sum = distance_sum
            # If the sum is equal to the current minimum, append the headwater to the list of sources
            elif distance_sum == min_distance_sum:
                source.append(hw)
        
        # Return the list of potential sources
        return source    


def parse_csv_into_adjacency_list(graph: Graph):
    with open(CSV_FILE, mode="r", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            node_id = int(row["Node"])
            linked = None if int(row["linked"]) == 0 else int(row["linked"])
            vertex_dict = {
                "node_id": node_id,
                "x": int(row["x"]),
                "y": int(row["y"]),
                "type": row["type"],
            }
            if not (graph.data(node_id)):
                graph.add_node(vertex_dict)
            if linked:
                graph.add_edge(node_id, Edge(linked))

def LL_as_array(LinkedList):
    if not hasattr(LinkedList, "next"):
        raise TypeError("Input isn't a LinkedList")
    LL_as_array = []
    cur_node = LinkedList
    while cur_node:
        LL_as_array.append(cur_node)
        cur_node = cur_node.next
    return tuple(LL_as_array)

def ll_as_array(LinkedList):
    if not hasattr(LinkedList, "next"):
        raise TypeError("Input isn't a LinkedList")
    
    array_representation = []
    cur_node = LinkedList.next  # Skip the Vertex and start with the Edge
    
    while cur_node:
        array_representation.append(cur_node.node)  # Extract the adjacent node ID
        cur_node = cur_node.next
    
    return array_representation


graph = Graph()
# Parse the CSV file's data into graph's adjacency list
parse_csv_into_adjacency_list(graph)

# Populate the distance and flow rate of all paths
graph.populate_distance()
graph.populate_flow_rate()

print(graph.chemical_source([(58,3),(55,10),(52,5)]))  # Expected: [25]
print(graph.chemical_source([(57,10),(56,5),(55,2)]))  # Expected: [22, 21]
