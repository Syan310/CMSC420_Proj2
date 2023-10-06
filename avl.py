import json
from typing import List

# DO NOT MODIFY!
class Node():
    def  __init__(self,
                  key       : int,
                  word      : str,
                  leftchild,
                  rightchild):
        self.key        = key
        self.word      = word
        self.leftchild  = leftchild
        self.rightchild = rightchild

# DO NOT MODIFY!
def dump(root: Node) -> str:
    def _to_dict(node) -> dict:
        return {
            "key": node.key,
            "word": node.word,
            "l": (_to_dict(node.leftchild) if node.leftchild is not None else None),
            "r": (_to_dict(node.rightchild) if node.rightchild is not None else None)
        }
    if root == None:
        dict_repr = {}
    else:
        dict_repr = _to_dict(root)
    return json.dumps(dict_repr,indent = 2)


def height(node):
    if not node:
        return 0
    return max(height(node.leftchild), height(node.rightchild)) + 1

def balance_factor(node):
    return height(node.leftchild) - height(node.rightchild)

def left_rotate(x):
    y = x.rightchild
    x.rightchild = y.leftchild
    y.leftchild = x
    return y

def right_rotate(y):
    x = y.leftchild
    y.leftchild = x.rightchild
    x.rightchild = y
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
    return node

def insert(root, key, word):
    if not root:
        return Node(key, word, None, None)
    
    # Standard BST insert
    if key < root.key:
        root.leftchild = insert(root.leftchild, key, word)
    else:
        root.rightchild = insert(root.rightchild, key, word)
    
    # Balance the node again
    return balance(root)



def insert_without_balance(root, key, word):
    if not root:
        return Node(key, word, None, None)
    
    if key < root.key:
        root.leftchild = insert_without_balance(root.leftchild, key, word)
    else:
        root.rightchild = insert_without_balance(root.rightchild, key, word)
    
    return root

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

# bulkInsert
# The parameter items should be a list of pairs of the form [key,word] where key is an integer and word is a string.
# For the tree rooted at root, first insert all of the [key,word] pairs as if the tree were a standard BST, with no balancing.
# Then do a preorder traversal of the [key,word] pairs and use this traversal to build a new tree using AVL insertion.
# Return the root
def bulkInsert(root, items):
    # Step 1: Standard BST insert without balancing
    for item in items:
        key, word = item
        root = insert_without_balance(root, key, word)
    
    # Step 2: Extract all nodes in order
    nodes_in_order = []
    inorder_traversal(root, nodes_in_order)
    
    # Step 3: Construct a new balanced AVL tree
    root = construct_avl_tree(nodes_in_order)
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
def bulkDelete(root, keys):
    keys_set = set(keys)  # for O(1) lookup
    
    # Step 1: Extract all nodes not in keys_set in order
    nodes_in_order = []
    inorder_traversal_filtered(root, nodes_in_order, keys_set)
    
    # Step 2: Construct a new balanced AVL tree
    root = construct_avl_tree(nodes_in_order)
    return root




def inorderTraversal(node, delete_keys):
    """
    Perform an inorder traversal of the tree rooted at node, 
    returning a list of nodes (not in delete_keys) in sorted order.
    """
    result = []
    if node:
        result.extend(inorderTraversal(node.leftchild, delete_keys))
        if node.key not in delete_keys:
            result.append((node.key, node.word))
        result.extend(inorderTraversal(node.rightchild, delete_keys))
    return result


# search
# For the tree rooted at root, calculate the list of keys on the path from the root to the search_key,
# including the search key, and the word associated with the search_key.
# Return the json stringified list [key1,key2,...,keylast,word] with indent=2.
# If the search_key is not in the tree return a word of None.
def search(root, search_key):
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
def replace(root, search_key, replacement_word):
    if not root:
        return None
    if root.key == search_key:
        root.word = replacement_word
    elif root.key < search_key:
        root.rightchild = replace(root.rightchild, search_key, replacement_word)
    else:
        root.leftchild = replace(root.leftchild, search_key, replacement_word)
    return root


