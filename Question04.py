import csv
import math

nodes_data = {}

# Range of nodes that nodes occur in
x_min, y_min = 70, 100
x_max, y_max = 580, 580

# List to store nodes within the range
nodes_within_range = []

# Read the CSV dataset and check if each node's coordinates are within the range, build a dictionary of nodes
with open('water_data.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        node = int(row['Node'])
        x = float(row['x'])
        y = float(row['y'])
        if x_min <= x <= x_max and y_min <= y <= y_max:
            nodes_within_range.append(node)
            
        nodes_data[node] = {
            "x": x,
            "y": y,
        }
    for row in reader:
        node_id = int(row["Node"])
        x = float(row["x"])
        y = float(row["y"])
        linked_ids = [int(linked) for linked in row["linked"].split(',') if linked != '']
        nodes_data[node_id] = {"x": x, "y": y, "linked": linked_ids, "type": row["type"]}

nodes_data = {}
with open("water_data.csv", mode="r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        node_id = int(row["Node"])
        x = float(row["x"])
        y = float(row["y"])
        linked_ids = [int(linked) for linked in row["linked"].split(',') if linked != '']
        nodes_data[node_id] = {"x": x, "y": y, "linked": linked_ids, "type": row["type"]}

# Function to calculate the distance between two nodes using Pythagoras Theorem
def calculate_distance(node1, node2):
    x1, y1 = node1["x"], node1["y"]
    x2, y2 = node2["x"], node2["y"]
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

# First range 
x_min, y_min = 70, 100
x_max, y_max = 220, 320

# Initialize total distance for (70,100) and (220,320) range
total_distance1 = 0

# Iterate through all nodes and find the distance to their linked node within the range
for node_id, node_info in nodes_data.items():
    if x_min <= node_info["x"] <= x_max and y_min <= node_info["y"] <= y_max:
        for linked_node_id in node_info["linked"]:
            linked_node_info = nodes_data.get(linked_node_id)
            if linked_node_info and x_min <= linked_node_info["x"] <= x_max and y_min <= linked_node_info["y"] <= y_max:
                distance = calculate_distance(node_info, linked_node_info)
                total_distance1 += distance

print(f"Total distance to visit all the nodes within (70,100) and (220,320) via boat: {total_distance1}")

# Range of nodes that Branch off of Node 62
x_min, y_min = 220, 100
x_max, y_max = 420, 600

# List to store nodes within the range
nodes_within_range = []

# Read the CSV dataset and check if each node's coordinates are within the range
with open('water_data.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        node = int(row['Node'])
        x = float(row['x'])
        y = float(row['y'])
        if x_min <= x <= x_max and y_min <= y <= y_max:
            nodes_within_range.append(node)

# Define the range of coordinates
x_min, y_min = 220, 100
x_max, y_max = 420, 600

# Initialize total distance
total_distance2 = 0

# Iterate through all nodes and find the distance to their linked node within the range
for node_id, node_info in nodes_data.items():
    if x_min <= node_info["x"] <= x_max and y_min <= node_info["y"] <= y_max:
        for linked_node_id in node_info["linked"]:
            linked_node_info = nodes_data.get(linked_node_id)
            if linked_node_info and x_min <= linked_node_info["x"] <= x_max and y_min <= linked_node_info["y"] <= y_max:
                distance = calculate_distance(node_info, linked_node_info)
                total_distance2 += distance

print(f"Total distance to visit all the nodes within (220,100) and (420, 600) via boat: {total_distance2}")

# Range of nodes that Branch off of Last area
x_min, y_min = 420, 80
x_max, y_max = 580, 600

# List to store nodes within the range
nodes_within_range = []

with open('water_data.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        node = int(row['Node'])
        x = float(row['x'])
        y = float(row['y'])
        if x_min <= x <= x_max and y_min <= y <= y_max:
            nodes_within_range.append(node)

# Define the range of coordinates
x_min, y_min = 420, 80
x_max, y_max = 580, 600

# Initialize total distance
total_distance3 = 0

# Iterate through all nodes and find the distance to their linked node within the range
for node_id, node_info in nodes_data.items():
    if x_min <= node_info["x"] <= x_max and y_min <= node_info["y"] <= y_max:
        for linked_node_id in node_info["linked"]:
            linked_node_info = nodes_data.get(linked_node_id)
            if linked_node_info and x_min <= linked_node_info["x"] <= x_max and y_min <= linked_node_info["y"] <= y_max:
                distance = calculate_distance(node_info, linked_node_info)
                total_distance3 += distance

print(f"Total distance to visit all the nodes within (420, 80) and (580, 600) via boat: {total_distance3}")

node1 = nodes_data[62]
node2 = nodes_data[50]

# Using Pythagoras Theorem calculate the road distance
distance = math.sqrt((node2["x"] - node1["x"])**2 + (node2["y"] - node1["y"])**2)
print("Road distance from Node 62 to Katherine:", distance)

#Total time  travelled on water
total_water_distance = (total_distance1 + total_distance2 + total_distance3)/32
print(f"Travel time via boat {total_water_distance} hours")

# Time to travel on the road
drive_time = distance / 60
print(f"Travel time via road {drive_time} hours")
=======
import csv
import math

nodes_data = {}

# Range of nodes that nodes occur in
x_min, y_min = 70, 100
x_max, y_max = 580, 580

# List to store nodes within the range
nodes_within_range = []

# Read the CSV dataset and check if each node's coordinates are within the range, build a dictionary of nodes
with open('water_data.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        node = int(row['Node'])
        x = float(row['x'])
        y = float(row['y'])
        if x_min <= x <= x_max and y_min <= y <= y_max:
            nodes_within_range.append(node)
            
        nodes_data[node] = {
            "x": x,
            "y": y,
        }
    for row in reader:
        node_id = int(row["Node"])
        x = float(row["x"])
        y = float(row["y"])
        linked_ids = [int(linked) for linked in row["linked"].split(',') if linked != '']
        nodes_data[node_id] = {"x": x, "y": y, "linked": linked_ids, "type": row["type"]}

nodes_data = {}
with open("water_data.csv", mode="r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        node_id = int(row["Node"])
        x = float(row["x"])
        y = float(row["y"])
        linked_ids = [int(linked) for linked in row["linked"].split(',') if linked != '']
        nodes_data[node_id] = {"x": x, "y": y, "linked": linked_ids, "type": row["type"]}

# Function to calculate the distance between two nodes using Pythagoras Theorem
def calculate_distance(node1, node2):
    x1, y1 = node1["x"], node1["y"]
    x2, y2 = node2["x"], node2["y"]
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

# First range 
x_min, y_min = 70, 100
x_max, y_max = 220, 320

# Initialize total distance for (70,100) and (220,320) range
total_distance1 = 0

# Iterate through all nodes and find the distance to their linked node within the range
for node_id, node_info in nodes_data.items():
    if x_min <= node_info["x"] <= x_max and y_min <= node_info["y"] <= y_max:
        for linked_node_id in node_info["linked"]:
            linked_node_info = nodes_data.get(linked_node_id)
            if linked_node_info and x_min <= linked_node_info["x"] <= x_max and y_min <= linked_node_info["y"] <= y_max:
                distance = calculate_distance(node_info, linked_node_info)
                total_distance1 += distance

print(f"Total distance to visit all the nodes within (70,100) and (220,320) via boat: {total_distance1}")

# Range of nodes that Branch off of Node 62
x_min, y_min = 220, 100
x_max, y_max = 420, 600

# List to store nodes within the range
nodes_within_range = []

# Read the CSV dataset and check if each node's coordinates are within the range
with open('water_data.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        node = int(row['Node'])
        x = float(row['x'])
        y = float(row['y'])
        if x_min <= x <= x_max and y_min <= y <= y_max:
            nodes_within_range.append(node)

# Define the range of coordinates
x_min, y_min = 220, 100
x_max, y_max = 420, 600

# Initialize total distance
total_distance2 = 0

# Iterate through all nodes and find the distance to their linked node within the range
for node_id, node_info in nodes_data.items():
    if x_min <= node_info["x"] <= x_max and y_min <= node_info["y"] <= y_max:
        for linked_node_id in node_info["linked"]:
            linked_node_info = nodes_data.get(linked_node_id)
            if linked_node_info and x_min <= linked_node_info["x"] <= x_max and y_min <= linked_node_info["y"] <= y_max:
                distance = calculate_distance(node_info, linked_node_info)
                total_distance2 += distance

print(f"Total distance to visit all the nodes within (220,100) and (420, 600) via boat: {total_distance2}")

# Range of nodes that Branch off of Last area
x_min, y_min = 420, 80
x_max, y_max = 580, 600

# List to store nodes within the range
nodes_within_range = []

with open('water_data.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        node = int(row['Node'])
        x = float(row['x'])
        y = float(row['y'])
        if x_min <= x <= x_max and y_min <= y <= y_max:
            nodes_within_range.append(node)

# Define the range of coordinates
x_min, y_min = 420, 80
x_max, y_max = 580, 600

# Initialize total distance
total_distance3 = 0

# Iterate through all nodes and find the distance to their linked node within the range
for node_id, node_info in nodes_data.items():
    if x_min <= node_info["x"] <= x_max and y_min <= node_info["y"] <= y_max:
        for linked_node_id in node_info["linked"]:
            linked_node_info = nodes_data.get(linked_node_id)
            if linked_node_info and x_min <= linked_node_info["x"] <= x_max and y_min <= linked_node_info["y"] <= y_max:
                distance = calculate_distance(node_info, linked_node_info)
                total_distance3 += distance

print(f"Total distance to visit all the nodes within (420, 80) and (580, 600) via boat: {total_distance3}")

node1 = nodes_data[62]
node2 = nodes_data[50]

# Using Pythagoras Theorem calculate the road distance
distance = math.sqrt((node2["x"] - node1["x"])**2 + (node2["y"] - node1["y"])**2)
print("Road distance from Node 62 to Katherine:", distance)

#Total time  travelled on water
total_water_distance = (total_distance1 + total_distance2 + total_distance3)/32
print(f"Travel time via boat {total_water_distance} hours")

# Time to travel on the road
drive_time = distance / 60
print(f"Travel time via road {drive_time} hours")
