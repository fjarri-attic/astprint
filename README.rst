AST printing
============

Build status
------------

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

Printing a tree
~~~~~~~~~~~~~~~

::

    astprint.as_tree(node)

Returns a string with the ``ast.AST`` node pretty printed as a tree.
When ``eval()``'ed (with all the members of ``ast`` in the namespace), gives back the ``node``.

::

    >>> import ast
    >>> from astprint import as_tree
    >>> node =
    >>> ast.dump(node)
    ...
    >>> as_tree(node)
    ...

Printing code
~~~~~~~~~~~~~

::

    astprint.as_code(node)

Returns a string with the ``ast.AST`` node pretty printed as a code snippet.
When ``ast.parse()``'ed, gives back the ``node``.

::

    >>> import ast
    >>> from astprint import as_code
    >>> code = """
    ...
    ... """
    >>> node = ast.parse(code)
    >>> as_code(node)
    ...
