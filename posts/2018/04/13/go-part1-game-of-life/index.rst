
.. post:: Apr 13, 2018
   :tags: golang
   :title: Learning Go (part 1) - Conway's Game of Life


.. spelling::

   boolean
   neighbours
   underpopulation
   XUnit


.. |g| replace:: *Go*


=============================================
Learning |g| (part 1) - Conway's Game of Life
=============================================

The |g| programming language is currently fashionable, and it's been four
years since the last time I started to learn a new programming language,
Python. My goal in the next few months is it to learn enough |g| to read
the *Kubernetes* code base comfortably, simply because I'm interested in
that project and how they solved their problems. As a starting problem for
this multi-part series, I've chosen *Conway's Game of Life* [#cgol]_, as
these rules are simple to understand but more complex than a *hello world*.


.. contents::
    :local:
    :backlinks: top


.. list-table:: Change history:
   :widths: 1 5
   :header-rows: 1

   * - Date
     - Change description
   * - 2018-04-13
     - The first release


.. note::

   As this is a learning endeavor, there will be mistakes.
   Don't confuse the code below with any kind of actual recommendation.


Installing the latest |g| runtime
=================================

The installation of the |g| runtime [#goinstall]_ is coded in the following
*Ansible* playbook:

.. literalinclude:: provisioning_playbook.yml
   :language: yaml
   :linenos:
   :lines: 1-44

This is only one way of doing it, and it's not necessary to have the
latest greatest for the code below.


Setting up the project
======================

We need a unique package name for our code, to avoid import clashes [#imp]_.
The recommendation for code which will live on *Github* looks like this:

.. code-block:: bash
   :linenos:
   :emphasize-lines: 0

   $ mkdir -p $GOPATH/src/github.com/markuszoeller/cgol

Later, when we build the source code, it will be added to the ``pkg``
directory, and we get this structure:

.. code-block:: bash
   :linenos:
   :emphasize-lines: 0

   root@golang:~/go# tree
   .
   |-- pkg
   |   `-- linux_amd64
   |       `-- github.com
   |           `-- markuszoeller
   |               `-- cgol.a
   `-- src
       `-- github.com
           `-- markuszoeller
               `-- cgol
                   |-- cells.go
                   `-- cells_test.go

One interesting thing to notice is, that the test code lives in the very
same directory of the functional code, and |g| ignores that test code
when building the source.





Writing the functional code
===========================

Before we dive into the code, here's a short recap of the rules of
*Conway's Game of Life*, straight from *Wikipedia* [#cgol]_:

    Any live cell with fewer than two live neighbours dies, as if caused by
    underpopulation. Any live cell with two or three live neighbours lives
    on to the next generation. Any live cell with more than three live
    neighbours dies, as if by overpopulation. Any dead cell with exactly
    three live neighbours becomes a live cell, as if by reproduction.

I've decided to go with the simplest solution I could think of,
a two-dimensional array of boolean values which represent the cells
in my world. A ``true`` value is a cell which is alive, a ``false`` value
is a cell which is dead:

.. literalinclude:: cells.go
   :language: go
   :linenos:
   :emphasize-lines: 0

A few things to notice here:

* ``world = [10][10]bool`` was an attempt to reset all values to ``false``
  for the tests, but I couldn't make it work, so I took the dummy approach
  by iterating over all rows and columns of my world.
* ``row := 0`` shows the shorthand for variable definition and
  value assignment. It's equivalent to ``var row int = 0``.
* I didn't find a built-in way to convert the boolean value to an Integer
  value, so ``count += int(getCell(row-1, col-1))`` didn't work, therefore
  I used those ugly conditionals. |g| doesn't seem to have a ternary operator
  or any other way to do that in one line.
* Declaring ``bool`` as a return type of a function didn't allow me to
  return ``nil`` (the "nothing" of |g|), so I used ``false`` at the end.
* ``!(alive)`` shows an example of boolean negation. In Python it would
  look like ``not alive``.



Writing the unit tests
======================

Let's test what we have so far:

.. literalinclude:: cells_test.go
   :language: go
   :linenos:
   :emphasize-lines: 0

Things to notice are:

* ``t *testing.T`` is the one parameter every test function needs to
  accept to have access to the built-in testing framework. I'm not quite
  sure how to read it, but I guess it means we accept a reference to the
  class ``T`` in package ``testing`` and store it in variable ``t``.
* I didn't find a built-in way of executing code before and after every
  test function, like ``setup`` and ``teardown``, which are known from
  other XUnit testing frameworks. Honestly, this was quite odd to me.
  This forced me to reset the world with ``resetWorld()`` in each test
  method. Very odd.
* Other XUnit frameworks I used in the past usually had assertion methods
  like ``assertEqual`` or ``assertTrue``. |g| doesn't have that. Nothing
  stops you to implement that yourself as convenience methods, but I was
  very surprised to not find it built-in.


Format, test and build the project
==================================

Finally, we can check that our code is formatted like expected with
``go fmt``, then we execute the tests with ``go test`` and at last
we build the project with ``go build``:

.. code-block:: bash
   :linenos:

   $ go fmt
   $ go test
   $ go build

The ``go fmt`` command, which seems to be the authoritative source of how
the source code should be formatted, replaced all my spaces by tabs.
Frankly, I thought the whole fight about tabs versus spaces for formatting
source code was over and the usage of spaces won. Apparently I was wrong.
But I wasted too many hours of my life discussing that, so I just accept
it that |g| decided to do it this way.



Summary and next steps
======================

This post showed only how to write basic library code in a very basic way.
In the next post of this series, I'd like to add a CLI which imports the
library, takes some user input and then displays some generations of the
cells, according the rules we specified.

Learning more about the object oriented side of |g| is definitely also
something on my plate. Note sure if will be already in the next post of this
series, as I expect it to be a bit more complex.




References
==========

.. [#cgol] https://en.wikipedia.org/wiki/Conway's_Game_of_Life

.. [#goinstall] https://golang.org/doc/install

.. [#imp] https://golang.org/doc/code.html#ImportPaths
