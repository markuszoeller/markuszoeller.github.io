
.. post::
   :tags: template
   :title: Template for all posts

.. spelling::
   foo



======================
Template for all posts
======================

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
   * - 2017-11-02
     - The first release



General advice
==============

* the complete URL must not be longer than 78 chars
* the initial release date is in the URL
* post directory is part of the URL (make it searchable, don't be fancy)
* aim for less than 15h per post, otherwise the releases will become unstable
* the spelling check is done frequently and at the very end
* add the release date only if confident enough
* start with a brain dump, refine from there
* consider touch screens (mobile phones). CSS hover text magic doesn't work



Structure
=========

#. title
#. abstract
#. table of contents
#. change history table
#. TL;DR (if applicable)
#. use case
#. content
#. summary / conclusion
#. references
#. appendix

This is only the first level. Add another level if necessary. Let 2 levels
be the maximum.

Each section is a permalink and therefore a published resource. That means,
don't change once published permalinks (aka altering sections).


.. code-block:: rst
   :linenos:
   :emphasize-lines: 0

   =====
   title
   =====

   section
   =======

   sub-section
   -----------

   **paragraph header**



Table of contents
=================

Every post has a table of contents. The sections link back to the
table of contents. This makes jumps back and forth easy.

.. code-block:: rst
   :linenos:
   :emphasize-lines: 0

    .. contents::
        :local:
        :backlinks: top



Categories and labels
=====================

There are 3 categories:

* books
* conferences
* openstack

Categories are more coarse grained than labels. Having no category is fine,
it's then seen as being miscellaneous until a category evolves over time.

Add labels as you see fit. Check the existing ones. Use one to three labels.

.. code-block:: rst
   :linenos:
   :emphasize-lines: 0

    .. post:: 25 Aug, 2017
       :category: openstack
       :tags: nova, scheduling, cpu-architecture
       :title: OpenStack Nova Scheduling based on CPU architecture


Code examples
=============

* blocks always with line numbers
* emphasize lines to set focus
* use the proper highlighting language [#pygments]_

Text
----

The config option ``key2`` has value ``value2``.

.. code-block:: rst
   :linenos:
   :emphasize-lines: 0

   The config option ``key2`` has value ``value2``.


Blocks
------

.. code-block:: python
   :linenos:
   :emphasize-lines: 0

   print("hello blog")

.. code-block:: rst
   :linenos:
   :emphasize-lines: 0

   .. code-block:: python
      :linenos:
      :emphasize-lines: 0

      print("hello blog")

Files
-----

.. literalinclude:: example.ini
   :language: ini
   :linenos:
   :emphasize-lines: 5

.. code-block:: rst
   :linenos:
   :emphasize-lines: 0

    .. literalinclude:: example.ini
       :language: ini
       :linenos:
       :emphasize-lines: 5



Text format
===========

Use **strongly emphasized** to make a point.

.. code-block:: rst
   :linenos:
   :emphasize-lines: 0

   Use **strongly emphasized** to make a point.


----

Use *proper names* for people companies and software.
For example, *Kubernetes*.

.. code-block:: rst
   :linenos:
   :emphasize-lines: 0

   Use *proper names* for people companies and software.
   For example, *Kubernetes*.

----

Use an `inline quote` for inline referencing an external source
(like books) or small direct quotes of cited sources.

.. code-block:: rst
   :linenos:
   :emphasize-lines: 0

   Use an `inline quote` for inline referencing an external source
   (like books) or small direct quotes of cited sources.


----

    Use a block quote for multi line
    direct quotes of cited resources.

.. code-block:: rst
   :linenos:
   :emphasize-lines: 0

       Use a block quote for multi line
       direct quotes of cited resources.



Images
======

Favor vector graphics (``.svg``) over raster maps (``.png``).
Always do a scaling of the images (``:height:`` or ``:width:`` or ``:scale:``),
this enables the "click on the thumbnail to show the full image" logic.

.. image:: drawing_TOelDqK.svg
   :height: 150px
   :alt: Example drawing with Inkscape.


.. code-block:: rst
  :linenos:
  :emphasize-lines: 0

  .. image:: drawing_TOelDqK.svg
     :height: 150px
     :alt: Example drawing with Inkscape.

.. important::

   All images of all posts will be copied to ``_images``. This means
   unique image names are needed to avoid collisions. Use the script
   to generate unique (enough) identifiers.



Spelling
========

Use the spelling directive if it is only needed for one post:

.. code-block:: rst
   :linenos:
   :emphasize-lines: 0

   .. spelling::

      foo

or extend the `spelling_wordlist.txt`.

In either case, take care of upper and lower case, singular and plural.



References and links
====================

External
--------

"External" is everything outside of this blog.
Reference to it with auto-numbered footnotes [#footnotes]_


.. code-block:: rst
   :linenos:
   :emphasize-lines: 0

   Reference to it with auto-numbered footnotes [#footnotes]_

Internal
--------

"Internal" is everything inside of this blog.
For example the :ref:`about` page.

.. code-block:: rst
   :linenos:
   :emphasize-lines: 0

   For example the :ref:`about` page.



Lists
=====

Numbered lists for ordered items:

#. first do this,
#. then you can do that,
#. lastly you do another thing.

.. code-block:: rst
   :linenos:
   :emphasize-lines: 0

   Numbered lists for ordered items:

   #. first do this,
   #. then you can do that,
   #. lastly you do another thing.


----

Bullet lists for (unordered) items:

* a hat
* a walking stick
* an umbrella

.. code-block:: rst
   :linenos:
   :emphasize-lines: 0

   Bullet lists for (unordered) items:

   * a hat
   * a walking stick
   * an umbrella



Highlighted info boxes
======================

.. todo::

    Reminder for the author to do this here before publishing.

.. code-block:: rst
   :linenos:
   :emphasize-lines: 0

   .. todo::

       Reminder for the author to do this here before publishing.

----

.. admonition:: Feedback needed

    Use this for actively asking for feedback from the reader.

.. code-block:: rst
   :linenos:
   :emphasize-lines: 0

   .. admonition:: Feedback needed

       Use this for actively asking for feedback from the reader.


----

.. note::

    This is a "mild" highlight. No biggie if the reader misses it.

.. code-block:: rst
   :linenos:
   :emphasize-lines: 0

   .. note::

       This is a "mild" highlight. No biggie if the reader misses it.



----

.. tip::

    This gives advice to the reader.

.. code-block:: rst
   :linenos:
   :emphasize-lines: 0

   .. tip::

       This gives advice to the reader.


----


.. warning::

    Don't do this. This is a common mistake.


.. code-block:: rst
   :linenos:
   :emphasize-lines: 0

   .. warning::

       Don't do this. This is a common mistake.


----

.. important::

    Do this (really) / Be aware of this (really).


.. code-block:: rst
   :linenos:
   :emphasize-lines: 0

   .. important::

       Do this (really) / Be aware of this (really).


Change history
==============

The publish date is the very first entry. Append another entry below the
previous one when:

* the structure got changed
* a paragraph got added or removed
* content got altered which changed the meaning of something

In general, think twice before changing a published post. If a big change
would be necessary, maybe a follow up post is the better choice. If so,
cross-reference each other.

**No addition** needed when:

* typo fix
* small format change (bold, italics, ...)

.. code-block:: rst
   :linenos:
   :emphasize-lines: 7-8

    .. list-table:: Change history:
       :widths: 1 5
       :header-rows: 1

       * - Date
         - Change description
       * - 2017-11-02
         - The first release



References
==========

.. [#pygments] http://pygments.org/

.. [#footnotes] http://www.sphinx-doc.org/en/stable/rest.html#footnotes
