import json
from typing import List, Tuple

# DO NOT MODIFY!
class Node():
    def __init__(self, key: int, word: str, leftchild=None, rightchild=None):
        self.key = key
        self.word = word
        self.leftchild = leftchild
        self.rightchild = rightchild
        self.height = 1  # added height property to Node

# DO NOT MODIFY!
def dump(root: Node) -> str:
    def _to_dict(node) -> dict:
        return {
            "key": node.key,
            "word": node.word,
            "l": (_to_dict(node.leftchild) if node.leftchild is not None else None),
            "r": (_to_dict(node.rightchild) if node.rightchild is not None else None)
        }
    if root is None:
        dict_repr = {}
    else:
        dict_repr = _to_dict(root)
    return json.dumps(dict_repr, indent=2)

# Helper Methods

def height(node):
    if not node:
        return 0
    return node.height

def update_height(node):
    if node:
        node.height = 1 + max(height(node.leftchild), height(node.rightchild))

def balance_factor(node):
    return height(node.leftchild) - height(node.rightchild)

def left_rotate(x):
    y = x.rightchild
    x.rightchild = y.leftchild
    y.leftchild = x
    update_height(x)
    update_height(y)
    return y

def right_rotate(y):
    x = y.leftchild
    y.leftchild = x.rightchild
    x.rightchild = y
    update_height(y)
    update_height(x)
    return x

def balance(node):
    if balance_factor(node) > 1:
        if balance_factor(node.leftchild) < 0:
            node.leftchild = left_rotate(node.leftchild)
        node = right_rotate(node)
    elif balance_factor(node) < -1:
        if balance_factor(node.rightchild) > 0:
            node.rightchild = right_rotate(node.rightchild)
        node = left_rotate(node)
    else:
        update_height(node)
    return node

# Main Methods

def insert(root, key, word):
    if not root:
        return Node(key, word)
    
    if key < root.key:
        root.leftchild = insert(root.leftchild, key, word)
    else:
        root.rightchild = insert(root.rightchild, key, word)
    
    return balance(root)

def bulkInsert(root, items: List[Tuple[int, str]]) -> Node:
    nodes_in_order = []
    
    # Extract all nodes from existing tree
    inorder_traversal(root, nodes_in_order)
    
    # Add new nodes from items
    nodes_in_order.extend(items)
    
    # Sort nodes by key
    nodes_in_order.sort(key=lambda x: x[0])
    
    # Build a new balanced AVL tree
    return construct_avl_tree(nodes_in_order)

def inorder_traversal(root, nodes_list):
    if not root:
        return
    inorder_traversal(root.leftchild, nodes_list)
    nodes_list.append((root.key, root.word))
    inorder_traversal(root.rightchild, nodes_list)

def construct_avl_tree(nodes_list):
    if not nodes_list:
        return None
    mid_idx = len(nodes_list) // 2
    key, word = nodes_list[mid_idx]
    root = Node(key, word, None, None)
    root.leftchild = construct_avl_tree(nodes_list[:mid_idx])
    root.rightchild = construct_avl_tree(nodes_list[mid_idx+1:])
    return root

def bulkDelete(root, keys: List[int]) -> Node:
    keys_set = set(keys)
    nodes_in_order = []
    inorder_traversal_filtered(root, nodes_in_order, keys_set)
    new_root = None
    for key, word in nodes_in_order:
        new_root = insert(new_root, key, word)
    return new_root

def search(root, search_key: int) -> str:
    path = []
    current = root
    while current:
        path.append(current.key)
        if current.key == search_key:
            return json.dumps(path + [current.word], indent=2)
        elif current.key < search_key:
            current = current.rightchild
        else:
            current = current.leftchild
    return json.dumps(None, indent=2)

def replace(root, search_key: int, replacement_word: str) -> Node:
    if not root:
        return None
    if root.key == search_key:
        root.word = replacement_word
    elif root.key < search_key:
        root.rightchild = replace(root.rightchild, search_key, replacement_word)
    else:
        root.leftchild = replace(root.leftchild, search_key, replacement_word)
    return root
