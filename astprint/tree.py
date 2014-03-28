import sys
import ast


def as_tree(node, indent="  "):
    """
    Returns an eval-able string representing a node tree.

    The result is the same as given by `ast.dump()`, except that the elements of the tree
    are put on separate lines and indented with `indent`s
    so that the whole tree is more human-readable.
    """
    visitor = ASTPrinter(indent)
    visitor.visit(node)
    return visitor.dumps()


class ASTPrinter(ast.NodeVisitor):

    def __init__(self, indent):
        self.result = []
        self.indentation = 0
        self.indent_with = indent

    def dumps(self):
        return "".join(self.result)

    def write(self, text):
        self.result.append(text)

    def generic_visit(self, node):

        if isinstance(node, list):
            nodestart = "["
            nodeend = "]"
            children = [("", child) for child in node]
        else:
            nodestart = type(node).__name__ + "("
            nodeend = ")"
            children = sorted(
                [(attr + "=", getattr(node, attr)) for attr in node._fields if hasattr(node, attr)])

        if len(children) > 1:
            self.indentation += 1

        self.write(nodestart)
        for i, pair in enumerate(children):
            attr, child = pair
            if len(children) > 1:
                self.write("\n" + self.indent_with * self.indentation)
            if isinstance(child, (ast.AST, list)):
                self.write(attr)
                self.visit(child)
            else:
                self.write(attr + repr(child))

            if i != len(children) - 1:
                self.write(",")
        self.write(nodeend)

        if len(children) > 1:
            self.indentation -= 1
