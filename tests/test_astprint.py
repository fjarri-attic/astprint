#from __future__ import print_function

import re
import ast
import sys

import pytest

from astprint import as_code, as_tree


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
    node = ast.parse(source)

    # Check as_code()

    new_source = as_code(node)
    new_node = ast.parse(new_source)
    # Comparing the ASTs to avoid differences in code formatting
    # popping up as errors.
    assert_ast_equal(node, new_node)

    # Check as_tree()

    tree_dump = as_tree(node)
    new_node = eval(tree_dump, ast.__dict__)
    assert_ast_equal(node, new_node)


def skip_if_after(major, minor):
    if sys.version_info >= (major, minor):
        pytest.skip()


def skip_if_before(major, minor):
    if sys.version_info < (major, minor):
        pytest.skip()


def test_str_default():
    check_transformation(
        """
        a = 'abcd'
        """)


def test_str_unicode():
    skip_if_after(3, 0)
    check_transformation(
        """
        a = u'abcd'
        """)


def test_str_bytes():
    skip_if_before(3, 0)
    check_transformation(
        """
        a = b'abcd'
        """)


def test_name_constant():
    # NameConstant class was introduced in Py3.4 to represent some common constants
    # (Name for used before).
    check_transformation(
        """
        a = True
        b = False
        c = None
        """)


def test_dict():
    check_transformation(
        """
        a = {}
        a = {'g': 'd'}
        a = {1: 4.5, e: 1j+2}
        """)


def test_set():
    skip_if_before(2, 7)
    check_transformation(
        """
        a = {'g'}
        a = {1, True}
        """)


def test_list():
    check_transformation(
        """
        a = []
        a = [1]
        a = ['a', None]
        """)


def test_dict_comprehension():
    skip_if_before(2, 7)
    check_transformation(
        """
        a = {x:x+1 for x in range(10)}
        a = {x:'a' for x in range(10) if x > 5}
        """)


def test_set_comprehension():
    skip_if_before(2, 7)
    check_transformation(
        """
        a = {x for x in range(10)}
        a = {x for x in range(10) if x > 5}
        """)


def test_list_comprehension():
    check_transformation(
        """
        a = [x for x in range(10)]
        a = [x for x in range(10) if x > 5]
        a = (x for x in range(10) if x > 5)
        """)



def test_tuple_assign():
    check_transformation(
        """
        (a, b) = (1, 2)
        """)


def test_starred_assign():
    skip_if_before(3, 0)
    check_transformation(
        """
        a, *b = it
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


def test_unary_op():
    check_transformation(
        """
        a = -b
        b = not a
        """)


def test_slice():
    check_transformation(
        """
        a = l[:]
        a = l[1:]
        a = l[:1]
        a = l[1:3]
        a = l[::2]
        a = l[1:10:2]
        a = l[1:4,:5]
        """)


def test_yield():
    check_transformation(
        """
        def gen(x):
            for i in range(x):
                yield i
        """)


def test_yield_from():
    skip_if_before(3, 3)
    check_transformation(
        """
        def gen2(x):
            for i in range(x):
                yield from gen(i)
        """)


def test_lambda():
    check_transformation(
        """
        func = lambda x: x + 1
        func = lambda x, *args, **kwds: x + 1
        func = lambda x, a=4: x + a
        """)


def test_ellipsis():
    skip_if_before(3, 0)
    check_transformation(
        """
        a = l[1:5,2:6,...,:10]
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
        from .mod import a as b
        from ..mod import a as b
        from math import pi as PI
        from math import sqrt
        import math
        import a as b
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
    skip_if_before(3, 0)
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


def test_try():
    check_transformation(
        """
        try:
            do_stuff()
        except:
            raise

        try:
            do_stuff()
        except Exception:
            boo()
        except OtherException as a:
            hoo()
        except:
            raise

        try:
            do_stuff()
        finally:
            clean_up()

        try:
            do_stuff()
        except Exception:
            boo()
        except OtherException as a:
            hoo()
        finally:
            clean_up()
        """)


def test_raise():
    check_transformation(
        """
        try:
            do()
        except:
            raise

        raise Exception
        raise Exception(1, 2)
        """)


def test_raise_py2():
    skip_if_after(3, 0)
    check_transformation(
        """
        raise Exception, value
        raise Exception, value, traceback
        """)


def test_raise_from():
    skip_if_before(3, 0)
    check_transformation(
        """
        raise Exception() from OtherException()
        """)


def test_with():
    check_transformation(
        """
        with open('stuff'):
            do_something()
        with open('stuff') as f:
            do_something()
        """)


def test_multiple_with():
    skip_if_before(2, 7)
    check_transformation(
        """
        with open('stuff') as f, open('other_stuff') as f2:
            do_something()
        """)


def test_assert():
    check_transformation(
        """
        assert a == 1
        assert a > 1, 'error message'
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


def test_class_def_extended():
    skip_if_before(3, 0)
    check_transformation(
        """
        class A(metaclass=D):
            pass
        class A(*args, **kwds):
            pass
        """)


def test_print():
    skip_if_after(3, 0)
    check_transformation(
        """
        print 1
        print a, b
        print a, b,
        print >> stderr, c, d
        """)


def test_repr():
    skip_if_after(3, 0)
    check_transformation(
        """
        a = `b`
        """)
