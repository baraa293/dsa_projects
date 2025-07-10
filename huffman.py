"""
Purpose:
    This program reconstructs a binary tree from its preorder and inorder
    traversals, prints its postorder traversal, and uses the resulting tree
    to decode a Huffman-encoded binary string. The decoding process involves
    traversing the tree based on num values ('0' for left, '1' for right) and
    recording the values at leaf nodes.
"""

class BinaryTree:
    """
    Represents a node in a binary tree used for Huffman decoding.

    Each node stores a value and references to its left and right children.
    Leaf nodes represent actual values used in the decoded_sequence output.
    """
    def __init__(self, value):
        """
        Initializes a BinaryTree node.

        Parameters:
        value (int): The integer value of the node.
        """        
        self._value = value
        self._left = None
        self._right = None

def build_tree(preorder, inorder):
    """
    Constructs a binary tree from preorder and inorder traversal lists.

    Parameters:
        preorder (list): Preorder traversal of the tree as a list of integers.
        inorder (list): Inorder traversal of the tree as a list of integers.

    Returns:
        BinaryTree: Root node of the constructed binary tree.
    """

    if not preorder or not inorder:
        return None
    root_val = preorder[0]
    root = BinaryTree(root_val)
    mid_index = inorder.index(root_val)
    root._left = build_tree(preorder[1:1+mid_index], inorder[:mid_index])
    root._right = build_tree(preorder[1+mid_index:], inorder[mid_index+1:])
    return root

def postorder_traversal(root):
    """
    Computes the postorder traversal of the binary tree.

    Parameters:
        root (BinaryTree): The root of the binary tree.

    Returns:
        list: A list of integers representing the postorder traversal.
    """
    if root is None:
        return []
    return (postorder_traversal(root._left) + 
            postorder_traversal(root._right) + 
            [root._value])

def read_input_file():
    """
    Prompts the user for a file name and reads Huffman data from the file.

    Returns:
    tuple: A tuple containing preorder list, inorder list, 
    and the encoded binary string.
    """
    fname = input("Input file: ")
    file = open(fname,"r")
    preorder = []
    for i in file.readline().split():
        preorder.append(int(i))
    inorder = []
    for j in file.readline().split():
        inorder.append(int(j))
    
    binary_string = file.readline().strip()
    file.close()
    return preorder, inorder, binary_string

def decode_huffman(binary_string, root):
    """
    Decodes a Huffman-encoded binary string using a binary tree.

    Parameters:
        binary_string (str): A string of '0's and '1's 
        representing encoded data.

        root (BinaryTree): The root of the decoding binary tree.

    Returns:
        str: A string of decoded_sequence leaf values concatenated together.
    """
    decoded_sequence = ""
    node = root
    for num in binary_string:
        if num == "0":
            node = node._left
        else:
            node = node._right
        if node and not node._left and not node._right:
            decoded_sequence += str(node._value)
            node = root
    return decoded_sequence

def main():
    """
    Coordinates reading input, building the tree, 
    printing postorder, and decoding.
    """
    preorder, inorder, binary_string = read_input_file()
    root = build_tree(preorder, inorder)
    post_order_concat = ""
    for i in postorder_traversal(root):
        post_order_concat += str(i) + " "
    print(post_order_concat)
    print(decode_huffman(binary_string, root))

main()
