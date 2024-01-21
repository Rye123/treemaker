# treemaker

A Python library to generate a MermaidJS visualisation of an arbitrary tree.

## Usage (Command-line)
```bash
python3 treemaker.py [treestr]
```
- `treestr` is a *tree string* surrounded by double quotes. A tree string, in this case, is a space-separated string of labels for each node, where the child of each tree node is contained within parentheses.
  - For instance, for a tree node A with two children B and C, the tree string will be "A(B C)". For a tree node A with a child A1 and A2, where child A1 has three children A11, A12, A13, the tree string will be "A(A1(A11 A12 A13) A2)".

This will return a `mermaid.ink` link for the generated diagram.


