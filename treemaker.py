from typing import List

class TreeNode:
    """ A data structure to represent a node in a tree. """
    def __init__(self, label: str):
        if not isinstance(label, str):
            raise ValueError(f"TreeNode.__init__: Expected string as label, was given: {label} which has type {type(label)}")
        if len(label) == 0:
            raise ValueError("TreeNode.__init__: Expected nonzero-length string as label")
        self.children: List['TreeNode'] = []
        self.parent = None
        self.label = label

    def add_child(self, child: 'TreeNode'):
        if not isinstance(child, TreeNode):
            raise ValueError("TreeNode.add_child: Expected TreeNode as argument")
        self.children.append(child)
        self.children[-1].parent = self

    def add_children(self, children: List['TreeNode']):
        for child in children:
            self.add_child(child)

    @staticmethod
    def from_treestring(treestr: str) -> 'TreeNode':
        """ Initialises a TreeNode from a string, generated by the `__repr__()` of TreeNode. """
        cur_label = ""
        root = None
        cur_node = None
        for i in range(len(treestr)):
            char = treestr[i]
            match char:
                case ' ':
                    # Add the label to the current node
                    if len(cur_label) != 0:
                        cur_node.add_child(TreeNode(cur_label))
                        cur_label = ""
                case '(':
                    # Add a new node to the current node, and set that node as the current node, updating the parent
                    if cur_node is None:
                        # No current node, hence this is the root
                        cur_node = TreeNode(cur_label)
                        root = cur_node
                    else:
                        cur_node.add_child(TreeNode(cur_label))
                        child = cur_node.children[-1]
                        cur_node = child
                    cur_label = ""
                case ')':
                    if len(cur_label) != 0:
                        # Add a new node to the current node
                        cur_node.add_child(TreeNode(cur_label))
                        
                    # Return to the parent
                    cur_node = cur_node.parent
                    cur_label = ""
                case _:
                    if not char.isalnum():
                        raise ValueError(f"TreeNode.from_treestring: Unexpected character {char} in treestring.")
                    cur_label += char
        return root

    def __repr__(self) -> str:
        """
        Prints the treenode and its children.
        - A tree consisting of node A with children A1, A2, A3 will be printed as 'A(A1 A2 A3)'
        - A tree consisting of node A with child A1, which has two children A11 and A12 will be printed as 'A(A1(A11 A12))'.
        """
        if len(self.children) == 0:
            return self.label
        
        children_str = "("
        for child in self.children:
            children_str += child.__repr__() + " "
        children_str = children_str.strip() + ")"
        return self.label + children_str
        
