from typing import List, Tuple
from enum import IntEnum
from base64 import urlsafe_b64encode
import json

ACCEPTED_NONALNUMS = ['_', '-']
def is_valid_char(c: str):
    return (c.isalnum()) or (c in ACCEPTED_NONALNUMS)

counter = 0
def reset_id():
    global counter
    counter = 0

def get_id() -> int:
    global counter
    ret = counter
    counter += 1
    return ret

class TokenType(IntEnum):
    NODE = 0
    LITERAL = 1
    BRACK_L = 2
    BRACK_R = 3

class Token:
    def __init__(self, type: TokenType, label: str):
        self.type = type
        self.label = label

    def __repr__(self) -> str:
        if self.label == "":
            return self.type.name
        return self.type.name + f"({self.label})"

class TreeNode:
    """ A data structure to represent a node in a tree. """
    def __init__(self, label: str):
        if not isinstance(label, str):
            raise ValueError(f"TreeNode.__init__: Expected string as label, was given: {label} which has type {type(label)}")
        # if len(label) == 0:
        #     raise ValueError("TreeNode.__init__: Expected nonzero-length string as label")
        self.children: List['TreeNode'] = []
        self.parent = None
        self.label = label
        self._id = get_id()

        if len(self.label) == 0:
            self.label = "_"

    def add_child(self, child: 'TreeNode'):
        if not isinstance(child, TreeNode):
            raise ValueError("TreeNode.add_child: Expected TreeNode as argument")
        self.children.append(child)
        self.children[-1].parent = self

    def add_children(self, children: List['TreeNode']):
        for child in children:
            self.add_child(child)

    def get_depth(self):
        if len(self.children) == 0:
            return 1
        max_child_depth = max([child.get_depth() for child in self.children])
        return max_child_depth + 1

    def get_size(self):
        """ Returns number of nodes in the tree, including the node itself """
        if len(self.children) == 0:
            return 1
        return sum([child.get_size() for child in self.children]) + 1

    @staticmethod
    def from_treestring(treestr: str) -> 'TreeNode':
        """ Initialises a TreeNode from a string, generated by the `__repr__()` of TreeNode. """
        # 1. Tokenise
        label = ""
        tokens: List[Token] = []
        i = 0
        while i < len(treestr):
            c = treestr[i]
            match c:
                case '(':
                    tokens.append(Token(TokenType.BRACK_L, ""))
                case ')':
                    tokens.append(Token(TokenType.BRACK_R, ""))
                case ' ':
                    i += 1
                    continue
                case '\'':
                    # Parse string
                    j = i + 1
                    while j < len(treestr):
                        c = treestr[j]
                        if c == '\'':
                            break
                        j += 1
                    if j == len(treestr):
                        raise ValueError(f"Token Error: Unterminated string.")
                    
                    literal = treestr[i+1:j]
                    tokens.append(Token(TokenType.LITERAL, literal))
                    i = j
                case _:
                    if is_valid_char(c):
                        j = i + 1
                        while j < len(treestr):
                            c = treestr[j]
                            if not (c.isalnum() or (c in ACCEPTED_NONALNUMS)):
                                break
                            j += 1
                        label = treestr[i:j]
                        tokens.append(Token(TokenType.NODE, label))
                        i = j - 1
                    else:
                        raise ValueError(f"Token Error: Unexpected character {c} in treestr.")
            i += 1

        # 2. Build Tree
        root = TreeNode("ROOT")
        parent = root
        for token in tokens:
            match token.type:
                case TokenType.NODE:
                    child = TreeNode(token.label)
                    parent.add_child(child)
                case TokenType.LITERAL:
                    child = TreeNode(token.label)
                    parent.add_child(child)
                case TokenType.BRACK_L:
                    # Parent would be the most recent node
                    if len(parent.children) == 0:
                        raise RuntimeError("Expected a node before left bracket.")
                    parent = parent.children[-1]
                case TokenType.BRACK_R:
                    if parent == root:
                        raise ValueError("Cannot go up from ROOT.")
                    parent = parent.parent
        return root

    def get_nodes(self) -> List['TreeNode']:
        """ Returns a list of all nodes in this tree. """
        if len(self.children) == 0:
            return [self]
        ret = []
        ret.append(self)
        for child in self.children:
            ret += child.get_nodes()
        return ret

    def _get_mermaidstrs(self) -> Tuple[List[str], List[str]]:
        """ Returns the ID strings and link strings for the MermaidJS code """
        idstrings = []
        links = []
        for node in self.get_nodes():
            idstrings.append(f"id{node._id}([{node.label}])")
            for child in node.children:
                links.append(f"id{node._id}-->id{child._id}")
        return idstrings, links
        
    def get_mermaid_code(self) -> str:
        """ Returns neat MermaidJS code that would generate the result in `render()`. """
        idstrs, linkstrs = self._get_mermaidstrs()
        ret = "flowchart TD\n" + "\n".join([f"\t{idstr}" for idstr in idstrs]) + "\n" + "\n".join([f"\t{linkstr}" for linkstr in linkstrs])
        return ret

    def _get_encoded_state(self) -> str:
        idstrs, linkstrs = self._get_mermaidstrs()

        mermaid_state = {
            "code": self.get_mermaid_code(),
            "mermaid": { "theme": "default" },
            "autoSync": True,
            "updateDiagram": True,
            }

        json_encoded = json.dumps(mermaid_state).encode('ascii')
        return urlsafe_b64encode(json_encoded).decode('ascii')

    def get_link(self) -> str:
        """ Returns a link to a MermaidJS-generated diagram of the tree. """
        url = "https://mermaid.ink/img/base64:" + self._get_encoded_state()
        return url

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

def main(treestr: str):
    tree = TreeNode.from_treestring(treestr)
    print(tree.get_mermaid_code())
    print(tree.get_link())

if __name__ == "__main__":
    from sys import argv
    if len(argv) != 2:
        print("Usage: treemaker.py [tree string]")
        exit(1)
    main(argv[1])
