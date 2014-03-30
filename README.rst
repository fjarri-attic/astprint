AST printing
============

.. image:: https://travis-ci.org/Manticore/astprint.png?branch=master
    :target: https://travis-ci.org/Manticore/astprint

.. image:: https://coveralls.io/repos/Manticore/astprint/badge.png?branch=master
    :target: https://coveralls.io/r/Manticore/astprint

Rationale
---------

This package strives to provide some functionality missing from the ``ast`` module of the standard library, namely the pretty printing of ``AST`` objects:

  * as a tree (essentially, the indented ``ast.dump()``);
  * as a code snippet (which would give the tree back when being fed to ``ast.parse()``).

There have been several packages containing implementations of one or both of these functions, among them:

  * `macropy <https://github.com/lihaoyi/macropy>`_ ;
  * `meta <https://github.com/srossross/Meta>`_ ;
  * `astmonkey <https://github.com/konradhalas/astmonkey>`_ (based on the code by Armin Ronacher).

Unfortunately, all of them are not currently maintained, and do not fully support the changes introduced to ``ast`` in Python 3.
The first two are also quite large and the required functionality plays a secondary role in them.

That is why this package was written.
For the ease of maintenance it aims to be highly specialized and contain only the two functions specified above.


Usage
-----

::

    astprint.as_tree(node, indent='  ')

Returns a string with the ``ast.AST`` node pretty printed as a tree.
When ``eval()``'ed (with all the members of ``ast`` in the namespace), gives back the ``node``.

::

    astprint.as_code(node, indent='    ')

Returns a string with the ``ast.AST`` node pretty printed as a code snippet.
When ``ast.parse()``'ed, gives back the ``node``.

Example
-------

::

    >>> import ast
    >>> from astprint import as_code, as_tree
    >>> code = """
    ... def func(x):
    ...     if x > 0:
    ...         return x
    ...     else:
    ...         return -x
    ... """
    >>> node = ast.parse(code)
    >>> print(as_code(node))
    def func(x):
        if x > 0:
            return x
        else:
            return (-x)
    >>> print(as_tree(node))
    Module(body=[FunctionDef(
      args=arguments(
        args=[arg(
          annotation=None,
          arg='x')],
        defaults=[],
        kw_defaults=[],
        kwarg=None,
        kwargannotation=None,
        kwonlyargs=[],
        vararg=None,
        varargannotation=None),
      body=[If(
        body=[Return(value=Name(
          ctx=Load(),
          id='x'))],
        orelse=[Return(value=UnaryOp(
          op=USub(),
          operand=Name(
            ctx=Load(),
            id='x')))],
        test=Compare(
          comparators=[Num(n=0)],
          left=Name(
            ctx=Load(),
            id='x'),
          ops=[Gt()]))],
      decorator_list=[],
      name='func',
      returns=None)])
