#from __future__ import print_function

import re
import ast
import sys

import pytest

from astprint import as_code


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


def assert_ast_equal(test, expected):
    assert ast.dump(test) == ast.dump(expected)


def check_transformation(source):
    source = unshift(source)
    tree = ast.parse(source)
    #print(ast.dump(tree))
    new_source = as_code(tree)
    new_tree = ast.parse(new_source)

    # Comparing the ASTs to avoid differences in code formatting
    # popping up as errors.
    assert_ast_equal(tree, new_tree)


def skip_if_py2():
    if sys.version_info < (3, 0, 0):
        pytest.skip()


def test_str():
    if sys.version_info < (3, 0, 0):
        src = """
            a = 'abcd'
            b = u'defg'
            """
    else:
        src = """
            a = 'abcd'
            b = b'defg'
            """
    check_transformation(src)


def test_dict():
    check_transformation(
        """
        a = {'g': 'd'}
        a = {1: True, e: False}
        """)


def test_tuple_assign():
    check_transformation(
        """
        (a, b) = (1, 2)
        """)

def test_multi_assign():
    check_transformation(
        """
        a = b = 1
        """)

def test_augmented_assign():
    check_transformation(
        """
        a += 2
        """)

def test_del():
    check_transformation(
        """
        del a[0]
        del x, r
        """)

def test_import():
    check_transformation(
        """
        from math import pi as PI
        from math import sqrt
        import math
        """)

def test_function_simple():
    check_transformation(
        """
        def func(x, a=1):
            return x + a
        """)

def test_function_decorator():
    check_transformation(
        """
        @dec1
        @dec2
        def func(x, a=1):
            return x + a
        """)

def test_function_varargs():
    check_transformation(
        """
        def func(x, y, *args, **kwds):
            return x + y
        """)


def test_global():
    check_transformation(
        """
        def func(x, y, *args, **kwds):
            global a
            global c, d
        """)


def test_nonlocal():
    skip_if_py2()
    check_transformation(
        """
        def func(x, y, *args, **kwds):
            nonlocal a
            nonlocal c, d
        """)


def test_call():
    check_transformation(
        """
        func(1)
        func(1, 2)
        func(a, b, c=3)
        func(a, *args)
        func(b, *args, **kwds)
        """)


def test_attribute():
    check_transformation(
        """
        foo.bar()
        """)


def test_for():
    check_transformation(
        """
        for i, j in range(10):
            do_stuff()
            break
            continue
        """)

def test_while():
    check_transformation(
        """
        while r > 0:
            do_stuff()
            break
            continue
        """)

def test_if_else():
    check_transformation(
        """
        if a:
            sutff()

        if (b and c):
            foo()
        else:
            bar()

        if (c and d):
            foo()
        elif a:
            bar()
        else:
            blah()
        """)

def test_body_else():
    check_transformation(
        """
        for i in range(5):
            test(i)
        else:
            do_stuff()
        """)

def test_ternary_if_else():
    check_transformation(
        """
        a = do_this() if e + 5 else do_that()
        """)

def test_class_def():
    check_transformation(
        """
        class A:
            pass
        class A(B):
            pass
        class A(B, C):
            pass
        """)


def test_print():
    if sys.version_info < (3, 0, 0):
        src = """
            print 1
            """
    else:
        src = """
            print(1)
            """
    check_transformation(src)


def test_class_def_extended():
    skip_if_py2()
    check_transformation(
        """
        class A(metaclass=D):
            pass
        class A(*args, **kwds):
            pass
        """)
