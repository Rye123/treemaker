from typing import List

class TreeNode:
    def __init__(self, label: str):
        self.children: List['TreeNode'] = []
        self.label = label

    def add_child(self, child: 'TreeNode'):
        if not isinstance(child, TreeNode):
            raise ValueError("TreeNode.add_child: Expected TreeNode as argument")
        self.children.append(child)

    def add_children(self, children: List['TreeNode']):
        for child in children:
            self.add_child(child)

    def __repr__(self) -> str:
        if len(self.children) == 0:
            return self.label
        
        children_str = "("
        for child in self.children:
            children_str += child.__repr__() + " "
        children_str = children_str.strip() + ")"
        return self.label + children_str
        
