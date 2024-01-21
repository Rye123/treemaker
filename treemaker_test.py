import unittest
from treemaker import *

class TestTreeNode(unittest.TestCase):
    def test_repr(self):
        tree = TreeNode("A")
        tree.add_child(TreeNode("A1"))
        tree.add_child(TreeNode("A2"))
        tree.add_child(TreeNode("A3"))
        tree.add_child(TreeNode("A4"))
        tree.children[0].add_child(TreeNode("A11"))
        tree.children[0].add_child(TreeNode("A12"))
        tree.children[2].add_child(TreeNode("A31"))

        self.assertEqual(tree.__repr__(), "A(A1(A11 A12) A2 A3(A31) A4)")
        tree.children[0].children[1].add_children([TreeNode("A121"), TreeNode("A122"), TreeNode("A123")])
        tree.children[2].add_children([TreeNode("A32"), TreeNode("A33")])

        self.assertEqual(tree.__repr__(), "A(A1(A11 A12(A121 A122 A123)) A2 A3(A31 A32 A33) A4)")
