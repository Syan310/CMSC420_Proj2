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

# insert
# For the tree rooted at root, insert the given key,word pair and then balance as per AVL trees.
# The key is guaranteed to not be in the tree.
# Return the root.

def insert(root, key, word):
    if not root:
        return Node(key, word)
    
    if key < root.key:
        root.leftchild = insert(root.leftchild, key, word)
    else:
        root.rightchild = insert(root.rightchild, key, word)
    
    return balance(root)

# bulkInsert
# The parameter items should be a list of pairs of the form [key,word] where key is an integer and word is a string.
# For the tree rooted at root, first insert all of the [key,word] pairs as if the tree were a standard BST, with no balancing.
# Then do a preorder traversal of the [key,word] pairs and use this traversal to build a new tree using AVL insertion.
# Return the root
def bulkInsert(root, items: List[Tuple[int, str]]) -> Node:
    for key, word in items:
        root = insert(root, key, word)
    return root

def inorder_traversal_filtered(root, nodes_list, exclude_keys):
    if not root:
        return
    inorder_traversal_filtered(root.leftchild, nodes_list, exclude_keys)
    if root.key not in exclude_keys:
        nodes_list.append((root.key, root.word))
    inorder_traversal_filtered(root.rightchild, nodes_list, exclude_keys)

# bulkDelete
# The parameter keys should be a list of keys.
# For the tree rooted at root, first tag all the corresponding nodes (however you like),
# Then do a preorder traversal of the [key,word] pairs, ignoring the tagged nodes,
# and use this traversal to build a new tree using AVL insertion.
# Return the root.
def bulkDelete(root, keys: List[int]) -> Node:
    keys_set = set(keys)
    nodes_in_order = []
    inorder_traversal_filtered(root, nodes_in_order, keys_set)
    new_root = None
    for key, word in nodes_in_order:
        new_root = insert(new_root, key, word)
    return new_root

# search
# For the tree rooted at root, calculate the list of keys on the path from the root to the search_key,
# including the search key, and the word associated with the search_key.
# Return the json stringified list [key1,key2,...,keylast,word] with indent=2.
# If the search_key is not in the tree return a word of None.
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

# replace
# For the tree rooted at root, replace the word corresponding to the key search_key by replacement_word.
# The search_key is guaranteed to be in the tree.
# Return the root
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
