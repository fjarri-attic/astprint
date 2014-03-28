from __future__ import print_function

import sys
import ast

if sys.version_info.major < 3:
    from StringIO import StringIO
else:
    from io import StringIO


class ASTPrinter(ast.NodeVisitor):

    def __init__(self, indent):
        self.out = StringIO()
        self.current_indent = ''
        self.one_indent = indent

    def dumps(self):
        self.out.seek(0)
        return self.out.read()

    def print(self, text, **kwargs):
        new_text = text.format(**kwargs)
        print(new_text, file=self.out, sep='', end='')

    def generic_visit(self, node):

        if isinstance(node, list):
            nodestart = '['
            nodeend = ']'
            children = [("", child) for child in node]
        else:
            nodestart = type(node).__name__ + '('
            nodeend = ')'
            children = sorted(
                [(attr + "=", getattr(node, attr)) for attr in node._fields if hasattr(node, attr)])

        if len(children) > 1:
            self.current_indent += self.one_indent

        self.print(nodestart)
        for i, pair in enumerate(children):
            attr, child = pair
            if len(children) > 1:
                self.print("\n" + self.current_indent)
            if isinstance(child, (ast.AST, list)):
                self.print(attr)
                self.visit(child)
            else:
                self.print("{attr}{value}", attr=attr, value=repr(child))

            if i != len(children) - 1:
                self.print(",")
        self.print(nodeend)

        if len(children) > 1:
            self.current_indent = self.current_indent[:-len(self.one_indent)]


def as_tree(node, indent='  '):
    '''
    Returns an eval-able string representing the AST.
    '''

    visitor = ASTPrinter(indent)
    visitor.visit(node)
    return visitor.dumps()
