
.. post::
   :tags: template
   :category: monitoring
   :title: Elastic Stack (formerly ELK) - Elasticsearch

.. spelling::
   tokenized



==============================================
Elastic Stack (formerly ELK) - *Elasticsearch*
==============================================

Each post should start with one paragraph which is an abstract of the post.
This paragraph should be enough for a reader to decide if they want to
read the post or not. It is best to keep this paragraph short and simple.
100 words or less is the limit, as this abstract is used as excerpt in the
list on the landing page and in the feed readers. This upper limit
of 100 words is also the amount of content someone should be able to read
in less than 20 seconds. Additionally, it fits on one small mobile screen.

https://www.elastic.co/webinars/getting-started-elasticsearch?elektra=ELKvideo

Maybe use http://jsonlines.org/on_the_web/ for the example logs

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

.. |es| replace:: *Elasticsearch*

Brain dump
==========

This is the first part of a multi-part series about the
*Elastic Stack* (formerly the *ELK* stack). This stack
consists of 3 parts:

* storing data with |es|
* ingesting data with *Logstash* (and/or *Beats*)
* visualizing data with *Kibana*

This post will focus on the first part, |es|.


It uses a schema-less, flexible data model, which means you
can use your current data as-is and don't have to transform
it into another schema so that |es| can deal with it.

This post will focus on the *log analytics* part and
won't delve into metrics analytics or other use cases.

We will also not talk about the *x-pack* plugins,
which would add more functionality.

The platform support matrix is at:
https://www.elastic.co/support/matrix

We will use this setup:

* OS: Ubuntu 16.04
* JVM: IcedTea OpenJDK
* |es|: 6.1


Terms:
------

document
    One single, unstructured entry in |es| which gets
    tokenized into its parts.


Actions
-------

* ``match`` (``OR``'ed; see ``_score``)
* ``match_phrase``
* ``must`` and ``must_not``
* ``AND``'ed with multiple *clauses*
* ``should`` orders by score
* querying and filtering are different
* understand the *analysis* for tokenized documents
* aggregations with ``aggs`` (and e.g. ``avg``)
* partial update with  ``POST`` to ``_update`` API
* replacement with plain ``POST`` API on index



Download the compressed project source archive file, decompress it,
change to the ``env`` directory, start the *Vagrant* setup and use
*Ansible* to set configure |es| on that virtualized environment:

.. code-block:: bash
   :linenos:
   :emphasize-lines: 0

   [markus@local]$ untar -xcv project.tar.gz
   [markus@local]$ cd env
   [markus@local]$ vagrant up
   [markus@local]$ ansible-playbook playbook.yml


Your output should look similar to this:

.. code-block:: text
   :linenos:
   :emphasize-lines: 0

   TASK [Check if Elasticsearch is up an running.] *******************************
   Wednesday 03 January 2018  17:15:23 +0100 (0:00:01.189)       0:00:45.358 *****
   FAILED - RETRYING: Check if Elasticsearch is up an running. (5 retries left).
   FAILED - RETRYING: Check if Elasticsearch is up an running. (4 retries left).
   ok: [es1 -> localhost]

   PLAY RECAP ********************************************************************
   es1                        : ok=21   changed=17   unreachable=0    failed=0


After the setup by the *Ansible playbook*, we can interact with |es|
via ``curl`` on our local machine:

.. code-block:: bash
   :linenos:
   :emphasize-lines: 0

   [markus@local]$ curl 192.168.78.11:9200
   {
     "name" : "hMDFApt",
     "cluster_name" : "elasticsearch",
     "cluster_uuid" : "kEM4Oz-PQQ-98ZgdOxGOdw",
     "version" : {
       "number" : "6.1.1",
       "build_hash" : "bd92e7f",
       "build_date" : "2017-12-17T20:23:25.338Z",
       "build_snapshot" : false,
       "lucene_version" : "7.1.0",
       "minimum_wire_compatibility_version" : "5.6.0",
       "minimum_index_compatibility_version" : "5.0.0"
     },
     "tagline" : "You Know, for Search"
   }




questions
---------

* Q: Horizontal scale out of |es| instances?




References
==========

.. [#pygments] http://pygments.org/

.. [#footnotes] http://www.sphinx-doc.org/en/stable/rest.html#footnotes
