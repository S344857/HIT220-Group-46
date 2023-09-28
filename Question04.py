# Class to represent the nodes in the Trie
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

# Function to insert a word into the Trie
def insert_word(root, word):
    node = root
    for char in word:
        if char not in node.children:
            node.children[char] = TrieNode()
        node = node.children[char]
    node.is_end_of_word = True

# Function to create the Trie
def build_trie(words):
    root = TrieNode()
    for word in words:
        insert_word(root, word)
    return root

# Encoding individual characters implementing ASCII value represented in 8-bit binary
def encode_char(char):
    return format(ord(char), '08b')

# Encodes the full word by traversing the Trie
def encode_word(root, word):
    node = root
    encoded_word = ""
    for char in word:
        if char in node.children:
            encoded_word += encode_char(char)
            node = node.children[char]
        else:
            # Handle characters not found in the Trie
            encoded_word += encode_char('*')  # Encode as a special character
            break
    return encoded_word

# Function that takes the root 
def code_string(trie_root, word):
    encoded_word = encode_word(trie_root, word)
    return encoded_word

# Implementation
river_names = ["DalyRiver", "PineCreek"]
trie_root = build_trie(river_names)

word_to_encode = "DalyRiver"
encoded_string = code_string(trie_root, word_to_encode)
print(f"Encoded string for '{word_to_encode}': {encoded_string}")

word_to_encode = "PineCreek"
encoded_string = code_string(trie_root, word_to_encode)
print(f"Encoded string for '{word_to_encode}': {encoded_string}")
