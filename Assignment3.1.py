#Part 1- Creating dictionary with nodes

class Node:
    def __init__(self, x, y, adjacent):
        self.x = x
        self.y = y
        self.adjacent = adjacent

# Creating the dictionary with nodes
nodes_data = {
    1: Node(70, 100, "headwater", [42]),
    2: Node(230, 190, "junction", [19, 35, 36]),
    3: Node(120, 255, "headwater", [42]),
    4: Node(120, 275, "headwater", [33]),
    5: Node(195, 320, "headwater", [34]),
    6: Node(225, 370, "headwater", [40]),
    7: Node(230, 420, "headwater", [40]),
    8: Node(260, 465, "headwater", [43]),
    9: Node(315, 460, "headwater", [43]),
    10: Node(325, 500, "headwater", [44]),
    11: Node(350, 495, "headwater", [44]),
    12: Node(355, 215, "headwater", [44]),
    13: Node(380, 570, "headwater", [47]),
    14: Node(360, 410, "headwater", [48]),
    15: Node(385, 390, "headwater", [48]),
    16: Node(245, 335, "headwater", [37]),
    17: Node(225, 240, "headwater", [59]),
    18: Node(240, 140, "headwater", [35]),
    19: Node(330, 185, "headwater", [2]),
    20: Node(330, 200, "headwater", [36]),
    21: Node(340, 215, "headwater", [57]),
    22: Node(365, 180, "headwater", [57]),
    23: Node(430, 180, "headwater", [58]),
    24: Node(451, 200, "headwater", [58]),
    25: Node(430, 230, "headwater", [55]),
    26: Node(451, 220, "headwater", [52]),
    27: Node(425, 260, "headwater", [51]),
    28: Node(410, 230, "headwater", [51]),
    29: Node(520, 275, "headwater", [45]),
    30: Node(570, 210, "headwater", [53]),
    31: Node(510, 120, "headwater", [54]),
    32: Node(520, 80, "headwater", [54]),
    33: Node(150, 180, "junction", [4, 34, 42]),
    34: Node(170, 210, "junction", [5, 33, 59]),
    35: Node(230, 190, "junction", [2, 18, 59]),
    36: Node(270, 250, "junction", [2, 20, 37]),
    37: Node(280, 270, "junction", [16, 36, 39]),
    38: Node(325, 335, "junction", [39, 41, 49]),
    39: Node(320, 290, "junction", [37, 38, 55]),
    40: Node(265, 360, "junction", [6, 7, 41]),
    41: Node(290, 360, "junction", [38, 40, 43]),
    42: Node(125, 100, "junction", [1, 3, 33]),
    43: Node(310, 390, "junction", [8, 9, 41]),
    44: Node(395, 450, "junction", [10, 11, 12, 47]),
    45: Node(380, 340, "junction", [29, 46, 47]),
    46: Node(380, 340, "junction", [50, 45, 49]),
    47: Node(410, 430, "junction", [44, 13, 45]),
    48: Node(350, 360, "junction", [49, 14, 15]),
    49: Node(350, 350, "junction", [48, 46, 38]),
    50: Node(425, 290, "junction", [46, 51, 52]),
    51: Node(430, 280, "junction", [50, 27, 28]),
    52: Node(450, 260, "junction", [26, 53, 50]),
    53: Node(520, 250, "junction", [54, 30, 52]),
    54: Node(540, 180, "junction", [31, 32, 53]),
    55: Node(360, 260, "junction", [56, 25, 39]),
    56: Node(370, 230, "junction", [57, 58, 55]),
    57: Node(370, 220, "junction", [21, 22, 56]),
    58: Node(380, 230, "junction", [56, 23, 24]),
    59: Node(190, 205, "junction", [34, 35, 17]),
}

# Accessing individual nodes
print(nodes_data[1].x)
print(nodes_data[2].y)
print(nodes_data[33].type)
print(nodes_data[44].adjacent)
