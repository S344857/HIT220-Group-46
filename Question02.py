import csv
import math
import itertools

# Read CSV file 
nodes_data = {}
with open("water_data.csv", mode="r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        node_id = int(row["Node"])
        x = float(row["x"])
        y = float(row["y"])
        linked_ids = [int(linked) for linked in row["linked"].split(',') if linked != '']
        nodes_data[node_id] = {"x": x, "y": y, "linked": linked_ids, "type": row["type"]}

# Using Pythagoras Theorem to calculate the distance between two nodes 
def calculate_distance(node1, node2):
    x1, y1 = node1["x"], node1["y"]
    x2, y2 = node2["x"], node2["y"]
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

# X, Y range
x_min, y_min = 70, 100
x_max, y_max = 580, 580

# Filter nodes within the specified range
nodes_in_range = {node_id: node_info for node_id, node_info in nodes_data.items() if
                  x_min <= node_info["x"] <= x_max and y_min <= node_info["y"] <= y_max}

#for key in nodes_in_range: print(f"{key}: {nodes_in_range[key]}")
# Generate all possible permutations of nodes within the range
permutations = itertools.permutations(nodes_in_range.keys())



# Tracking the best path and its distance
best_path = None
best_distance = float('inf')

# Calculate distances
count = 0
limit = 100000
for path in permutations:
    count += 1
    if count == limit: break
    if count % 16789 == 0: print(str(count)+" ("+str(limit-count)+" remaining)")

    path_distance = 0
    prev_node = None

    for node_id in path:
        node_info = nodes_in_range[node_id]

        if prev_node is not None:
            #print(f"distance: node_info[{node_id}]({node_info['x']}, {node_info['y']})")
            #print(f"distance: nde_in_ra[{prev_node}]({nodes_in_range[prev_node]['x']}, {nodes_in_range[prev_node]['y']})")
            #print(input(""))
            distance = calculate_distance(node_info, nodes_in_range[prev_node])
            path_distance += distance

        prev_node = node_id

    # Add the distance from the last node back to the starting node
    path_distance += calculate_distance(node_info, nodes_in_range[path[0]])

    # Update the best path if this path is shorter
    if path_distance < best_distance:
        best_distance = path_distance
        best_path = path


print("Shortest path to visit nodes within (70,100)(580,580):")
shortest_path_list = [f"{node_id}" for node_id in best_path]
print(shortest_path_list)
print(f"Total distance of the shortest path: {best_distance}")
