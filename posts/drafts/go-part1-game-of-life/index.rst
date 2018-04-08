
.. post::
   :tags: golang
   :title: Learning GO (part 1) - Conway's Game of Life

.. spelling::
   foo



============================================
Learning GO (part 1) - Conway's Game of Life
============================================

Each post should start with one paragraph which is an abstract of the post.
This paragraph should be enough for a reader to decide if they want to
read the post or not. It is best to keep this paragraph short and simple.
100 words or less is the limit, as this abstract is used as excerpt in the
list on the landing page and in the feed readers. This upper limit
of 100 words is also the amount of content someone should be able to read
in less than 20 seconds. Additionally, it fits on one small mobile screen.

.. contents::
    :local:
    :backlinks: top

.. todo:: date of the change history

.. list-table:: Change history:
   :widths: 1 5
   :header-rows: 1

   * - Date
     - Change description
   * - 2018-04-13
     - The first release



::

    mkdir -p $GOPATH/src/github.com/markuszoeller/cgol


::

    $ go test
    $ go fmt


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



.. literalinclude:: cells.go
   :language: go
   :linenos:
   :emphasize-lines: 0


.. literalinclude:: cells_test.go
   :language: go
   :linenos:
   :emphasize-lines: 0
