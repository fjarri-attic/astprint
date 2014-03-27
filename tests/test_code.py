#from __future__ import print_function

import re
import ast
import sys

import pytest

from astprint import as_code


SNIPPETS = [
    ("tuple_assign",
    """
    (a, b) = (1, 2)
    """),

    ("multi_assign",
    """
    a = b = 1
    """),

    ("function_simple",
    """
    def func(x, a=1):
        return x + a
    """),

    ("function_decorator",
    """
    @dec1
    @dec2
    def func(x, a=1):
        return x + a
    """),

    ("function_varargs",
    """
    def func(x, y, *args, **kwds):
        return x + y
    """),

    ("for_else",
    """
    for i in range(5):
        test(i)
    else:
        do_stuff()
    """),

    ("ternary_if_else",
    """
    a = do_this() if e + 5 else do_that()
    """),
]

if sys.version_info < (3, 0, 0):
    SNIPPETS += [
        ("print",
        """
        print 1
        """),
    ]
else:
    SNIPPETS += [
        ("print",
        """
        print(1)
        """),
    ]


SNIPPET_SOURCES = [src for _, src in SNIPPETS]
SNIPPET_IDS = [id for id, _ in SNIPPETS]


def unshift(source):
    ''' Shift source to the left - so that it starts with zero indentation
    '''
    source = source.rstrip("\n ").lstrip("\n")
    indent = re.match(r"([ \t])*", source).group(0)
    lines = source.split("\n")
    shifted_lines = []
    for line in lines:
        line = line.rstrip()
        if len(line) > 0:
            if not line.startswith(indent):
                raise ValueError("Inconsistent indent at line " + repr(line))
            shifted_lines.append(line[len(indent):])
        else:
            shifted_lines.append(line)
    return "\n".join(shifted_lines)


@pytest.mark.parametrize('source', SNIPPET_SOURCES, ids=SNIPPET_IDS)
def test_transformation(source):
    source = unshift(source)
    tree = ast.parse(source)
    #print(ast.dump(tree))
    new_source = as_code(tree)
    assert source == new_source
