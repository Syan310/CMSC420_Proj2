
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


def getHeight(node):
    if not node:
        return 0
    return node.height

def getBalance(node):
    if not node:
        return 0
    return getHeight(node.leftchild) - getHeight(node.rightchild)

def leftRotate(z):
    y = z.rightchild
    T2 = y.leftchild
    
    # Perform rotation
    y.leftchild = z
    z.rightchild = T2
    
    # Update heights
    z.height = 1 + max(getHeight(z.leftchild), getHeight(z.rightchild))
    y.height = 1 + max(getHeight(y.leftchild), getHeight(y.rightchild))
    
    # Return the new root
    return y

def rightRotate(y):
    x = y.leftchild
    T2 = x.rightchild
    
    # Perform rotation
    x.rightchild = y
    y.leftchild = T2
    
    # Update heights
    y.height = 1 + max(getHeight(y.leftchild), getHeight(y.rightchild))
    x.height = 1 + max(getHeight(x.leftchild), getHeight(x.rightchild))
    
    # Return the new root
    return x

def insert(node, key, word):
    # Perform standard BST insert
    if not node:
        return Node(key, word)
    
    if key < node.key:
        node.leftchild = insert(node.leftchild, key, word)
    else:
        node.rightchild = insert(node.rightchild, key, word)

    # Update the height of the ancestor node
    node.height = 1 + max(getHeight(node.leftchild), getHeight(node.rightchild))
    
    # Get the balance factor to check whether it became unbalanced
    balance = getBalance(node)
    
    # Balance the node
    # Left Left
    if balance > 1 and key < node.leftchild.key:
        return rightRotate(node)
    
    # Right Right
    if balance < -1 and key > node.rightchild.key:
        return leftRotate(node)
    
    # Left Right
    if balance > 1 and key > node.leftchild.key:
        node.leftchild = leftRotate(node.leftchild)
        return rightRotate(node)
    
    # Right Left
    if balance < -1 and key < node.rightchild.key:
        node.rightchild = rightRotate(node.rightchild)
        return leftRotate(node)
    
    return node



def inorderTraversal(node):
    """
    Perform an inorder traversal of the tree rooted at node, 
    returning a list of nodes in sorted order.
    """
    result = []
    if node:
        result.extend(inorderTraversal(node.leftchild))
        result.append((node.key, node.word))
        result.extend(inorderTraversal(node.rightchild))
    return result

def sortedListToBST(arr, start, end):
    """
    Convert a sorted list of key-word pairs to a balanced binary search tree.
    """
    # base case
    if start > end:
        return None
    
    # Get the middle element and make it root
    mid = (start + end) // 2
    root = Node(arr[mid][0], arr[mid][1])
    
    # Recursively build the left and right subtrees
    root.leftchild = sortedListToBST(arr, start, mid-1)
    root.rightchild = sortedListToBST(arr, mid+1, end)
    
    return root

# bulkInsert
# The parameter items should be a list of pairs of the form [key,word] where key is an integer and word is a string.
# For the tree rooted at root, first insert all of the [key,word] pairs as if the tree were a standard BST, with no balancing.
# Then do a preorder traversal of the [key,word] pairs and use this traversal to build a new tree using AVL insertion.
# Return the root
def bulkInsert(root, items):
    """
    Perform bulk insertion of key-word pairs into the AVL tree rooted at root.
    """
    # Insert items into the tree without balancing
    for key, word in items:
        root = insert(root, key, word)
    
    # Retrieve nodes in sorted order using inorder traversal
    sorted_nodes = inorderTraversal(root)
    
    # Build a balanced tree from the sorted nodes
    return sortedListToBST(sorted_nodes, 0, len(sorted_nodes)-1)

# bulkDelete
# The parameter keys should be a list of keys.
# For the tree rooted at root, first tag all the corresponding nodes (however you like),
# Then do a preorder traversal of the [key,word] pairs, ignoring the tagged nodes,
# and use this traversal to build a new tree using AVL insertion.
# Return the root.
def bulkDelete(root, keys):
    """
    Delete nodes with keys in the provided list from the tree rooted at root,
    then rebuild the tree in a balanced manner.
    """
    # Mark nodes for deletion and retrieve nodes in sorted order
    sorted_nodes = inorderTraversal(root, set(keys))
    
    # Build a balanced tree from the sorted nodes
    return sortedListToBST(sorted_nodes, 0, len(sorted_nodes)-1)

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
    """
    Search for a node with key search_key in the tree rooted at root,
    returning a JSON string containing the path of keys and the word.
    """
    path, word = searchHelper(root, search_key, [])
    
    # Convert the path and word to a JSON string
    result = path + [word]
    return json.dumps(result, indent=2)

def searchHelper(node, search_key, path):
    """
    Helper function for search, recursively searches for the key,
    updating the path as it descends the tree.
    """
    # Base case: node is None, key not found
    if node is None:
        return path, None
    
    # Key found
    if node.key == search_key:
        path.append(node.key)
        return path, node.word
    
    # Key is less than node's key, search left subtree
    elif search_key < node.key:
        path.append(node.key)
        return searchHelper(node.leftchild, search_key, path)
    
    # Key is greater than node's key, search right subtree
    else:
        path.append(node.key)
        return searchHelper(node.rightchild, search_key, path)

# replace
# For the tree rooted at root, replace the word corresponding to the key search_key by replacement_word.
# The search_key is guaranteed to be in the tree.
# Return the root
def replace(root, search_key, replacement_word):
    """
    Replace the word of the node with key search_key in the tree rooted at root
    with replacement_word.
    """
    node = findNode(root, search_key)
    if node:
        node.word = replacement_word
    return root

def findNode(node, search_key):
    """
    Find and return the node with key search_key in the tree rooted at node.
    """
    # Base case: node is None, key not found
    if node is None:
        return None
    
    # Key found
    if node.key == search_key:
        return node
    
    # Key is less than node's key, search left subtree
    elif search_key < node.key:
        return findNode(node.leftchild, search_key)
    
    # Key is greater than node's key, search right subtree
    else:
        return findNode(node.rightchild, search_key)
