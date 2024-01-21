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

    def test_from_treestring(self):
        treestrs = [
            "A(A1(A11 A12(A121 A122 A123)) A2 A3(A31 A32 A33) A4)",
            "A(A1(A11 A12) A2 A3(A31) A4)",
            "A(A1(A11 A12) A2 A3(A31) A4 A5(A51 A52 A53(A531 A532(A5321) A533) A54) A6)"
            ]

        for treestr in treestrs:
            self.assertEqual(TreeNode.from_treestring(treestr).__repr__(), treestr)

    def test_depth(self):
        test_tuples = [
            ("A(A1(A11 A12(A121 A122 A123)) A2 A3(A31 A32 A33) A4)", 4),
            ("A(A1(A11 A12) A2 A3(A31) A4)", 3),
            ("A(A1(A11 A12) A2 A3(A31) A4 A5(A51 A52 A53(A531 A532(A5321) A533) A54) A6)", 5),
            ("A(B(C(D(E(F(G(H(I(J(K(L(M(N(O(P(Q(R(S))))))))))))))))) Z Y)", 19)
            ]

        for test_tuple in test_tuples:
            tree = TreeNode.from_treestring(test_tuple[0])
            expected_depth = test_tuple[1]
            self.assertEqual(tree.get_depth(), expected_depth)
