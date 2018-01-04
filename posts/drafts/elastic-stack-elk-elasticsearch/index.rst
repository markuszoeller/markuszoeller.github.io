
.. post::
   :tags: template
   :category: monitoring
   :title: Elastic Stack (formerly ELK) - Elasticsearch

.. spelling::
   tokenized

.. |es| replace:: *Elasticsearch*



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


Intro
=====

This is the first part of a multi-part series about the
*Elastic Stack* (formerly the **ELK stack**). This stack
consists of 3 parts:

* **storing data** with |es|
* **ingesting data** with *Logstash* (and/or *Beats*)
* **visualizing data** with *Kibana*

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


.. _sec-env:

Set up the environment
======================

To reproduce the steps in this post, you need to have installed locally:

* *Vagrant* [#vagrinst]_
* *Ansible* [#ansinst]_
* *VirtualBox* [#vbinst]_

After these prerequisites are fulfilled:

#. download the compressed
   :download:`project source files <elastic-stack-elk-elasticsearch.tar.gz>`.
#. extract the archive
#. change to the ``env`` directory
#. start the *Vagrant* setup
#. use *Ansible* to configure the environment

.. code-block:: bash
   :linenos:
   :emphasize-lines: 0

   $ wget http://www.markusz.io/_downloads/elastic-stack-elk-elasticsearch.tar.gz
   $ tar -zxvf elastic-stack-elk-elasticsearch.tar.gz
   $ cd env
   $ vagrant up
   $ ansible-playbook playbook.yml


Your (truncated) output should look similar to this:

.. code-block:: text
   :linenos:
   :emphasize-lines: 0

   [...]

   PLAY RECAP ********************************************************************
   app1                       : ok=10   changed=6    unreachable=0    failed=0
   app2                       : ok=10   changed=6    unreachable=0    failed=0
   es1                        : ok=21   changed=17   unreachable=0    failed=0

   Thursday 04 January 2018  16:29:04 +0100 (0:00:01.319)       0:02:06.741 ******
   ===============================================================================
   Install python package manager. ---------------------------------------- 50.79s
   Install JAVA runtime. -------------------------------------------------- 24.73s
   Check if Elasticsearch is up an running. ------------------------------- 11.50s
   Wait for SSH to be ready. ---------------------------------------------- 10.36s
   Download file with checksum check. -------------------------------------- 9.31s
   Install app requirements. ----------------------------------------------- 4.87s
   Ensure system package cache is updated. --------------------------------- 4.46s
   Unarchive the elasticsearch archive. ------------------------------------ 1.43s
   Run example app. -------------------------------------------------------- 1.32s
   Run elasticsearch as daemon. -------------------------------------------- 1.22s
   Add our servers to the hosts file. -------------------------------------- 0.99s
   Deploy example app to servers. ------------------------------------------ 0.88s
   Ping each other via DNS names. ------------------------------------------ 0.77s
   Gather some facts for later. -------------------------------------------- 0.62s
   Creating user for Elasticsearch group. ---------------------------------- 0.37s
   Create a group for Elasticsearch. --------------------------------------- 0.32s
   Disable all swapping. --------------------------------------------------- 0.32s
   Create logging directory. ----------------------------------------------- 0.31s
   Set maximum number of memory map areas (permanently). ------------------- 0.29s
   Set number of open file descriptors (permanently). ---------------------- 0.28s


.. note::

   After you decided that you don't need this environment anymore,
   you can remove it with ``vagrant destroy -f``


This created an environment which looks like this:

.. image:: images/elasticsearch-env-nF4AMyX.svg
   :scale: 100 %
   :alt: *Vagrant* environment with virtual machines.

* one central logging server ``es1``
* two application servers ``app1`` and ``app2``
* *Ubuntu 16.04* as operating system
* Java *Open JDK* in version 8
* |es| in version 6.1

While the setup goes on for a minute or two, let's have a look at
a few basic terms and concepts of |es|.



Terms and Concepts
==================

Let's start with an overview of the basic concepts [#concepts]_.
I'll explain the details after this image:

.. image:: images/elasticsearch-concepts-YfYunTY.svg
   :scale: 100 %
   :alt: The basic terms and concepts in |es|

The main entity we're interested in is the **Document**. This is the
schema-less entity we want to store in |es|. In our case, as this post
focuses on centralized logging, this is one single log entry.

|es| stores *Documents* in an **Index** and every *Index* can store multiple
*Documents*. The *Index* is the entity which provides the ability to search
*Document* objects.

Each |es| service is considered a **Node**. This *Node* is not necessarily
bound to one hardware server or virtual machine. Each *Node* is in other
words, an |es| instance. Each one can have 0 to N *Index* objects to
scale out the management of *Document* objects.

For further horizontal scale out, each *Node* can be part of a **Cluster**.
Each *Cluster* consists of 1 to N *Node* objects. A single-node setup is
still a *Cluster* (with only 1 *Node*). There are *master nodes* in a
cluster, which determine how information gets replicated, but I won't
dive into it in this post.

As described before, an *Index* is the (abstract) entity which stores
our documents. To be precise, an *Index* consists of **Shards**. These
*Shard* objects are *Index* objects themselves and can therefore store
*Documents*. This concept enables splitting out the *Documents* into
smaller segments. One *Shard* is in fact the *Lucene Index* [#lucene]_,
the search engine encapsulated by |es|. Such *shards* can be called
**primary shards**.

The *Shard* objects can be replicated (copied) into so called **Replica**
entities (or **replica shards**). A set of *Replica* objects are collected
in a **Replication Group**. Those *replica shards* enable
*High Availability (HA)* and *Data Recovery (DR)*. Hopefully I can
dive deeper into these capabilities in a later post.

After these basic terms and concepts are described, let's finally
interact with |es| in our environment.



Basic Interaction with |es|
===========================

After the setup by the *Ansible playbook*, we can interact with the
**REST API** of |es| via ``curl`` on our local machine. Port ``9200`` is
the default:

.. code-block:: bash
   :linenos:
   :emphasize-lines: 3,4,7,11

   $ curl 192.168.78.11:9200
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

This JSON response shows a few things of the previous section:

* ``name``: The name of the *Node*. I used the default, which randomly
  generates a unique one. This is configurable.
* ``cluster_name``: The name of the *Cluster* this *Node* is in.
  Again, I used the default name.
* ``number``: The version of the |es| *Node*.
* ``lucene_version``: The version of the search engine
  encapsulated by |es|.

The REST API has some useful common options [#commonapi]_:

* ``pretty=true``: to beautify the JSON output
* ``format=yaml``: use YAML instead of JSON as output
* ``error_trace=true`` to show a more verbose error trace
* ``filter_path=<values>`` to reduce the response

We will use some of these later.



Health Check
------------

Let's do a basic health check of our single-node cluster.
We use ``format=yaml`` to have an output which is easier to read:

.. code-block:: bash
   :linenos:
   :emphasize-lines: 0

   $ curl 192.168.78.11:9200/_cat/health?format=yaml

The output, formatted as YAML:

.. code-block:: bash
   :linenos:
   :emphasize-lines: 5

   ---
   - epoch: "1514998054"
     timestamp: "16:47:34"
     cluster: "elasticsearch"
     status: "green"
     node.total: "1"
     node.data: "1"
     shards: "0"
     pri: "0"
     relo: "0"
     init: "0"
     unassign: "0"
     pending_tasks: "0"
     max_task_wait_time: "-"
     active_shards_percent: "100.0%"

|es| uses a traffic light system with *green*, *yellow* and *red*.
As the ``status`` is ``green``, we're good, the node works fine.



List Nodes
----------

Any real live production system which uses |es| will most likely have
a cluster with multiple nodes in it. In those setups it might come
in handy to list all nodes:

.. code-block:: bash
   :linenos:
   :emphasize-lines: 3,11,12

   $ curl 192.168.78.11:9200/_cat/nodes?format=yaml

The output, formatted as YAML:

.. code-block:: yaml
   :linenos:
   :emphasize-lines: 2,10,11

   ---
   - ip: "192.168.78.11"
     heap.percent: "6"
     ram.percent: "63"
     cpu: "0"
     load_1m: "0.00"
     load_5m: "0.00"
     load_15m: "0.00"
     node.role: "mdi"
     master: "*"
     name: "hMDFApt"

Remember, we have a single-node system, so only this one should
get listed:

* ``ip``: as described in the previous section :ref:`sec-env`
* ``master``: this node is a *master node* in this *cluster*.
  I'll dive deeper into that in a later post.
* ``name``: the name of this *node*

If the cluster would contain more nodes, they would be shown here
with YAML list style (see *Block Sequence* at [#yamllist]_).



Minimal Example
---------------

Let's create a very small document:

.. code-block:: bash
   :linenos:
   :emphasize-lines: 0

    $ curl -X PUT '192.168.78.11:9200/my-index/my-type/1?pretty' \
    -H 'Content-Type: application/json' \
    -d '{
        "my_document" : "my document content"
    }'

This HTTP PUT call does multiple things:

* it creates an *Index* called ``my-index``
* it creates a *Type* in that *Index*, called ``my-type``
* it adds the *Document* (the JSON for parameter ``-d``) to that *Index*
* it assigns the ID ``1`` to that document
* it increments the version number of that created (or updated) *Document*
* it specifies, that the HTTP response should be ``pretty`` json

It becomes more clear when we look at the HTTP response:

.. code-block:: json
   :linenos:
   :emphasize-lines: 0

   {
     "_index" : "my-index",
     "_type" : "my-type",
     "_id" : "1",
     "_version" : 1,
     "result" : "created",
     "_shards" : {
       "total" : 2,
       "successful" : 1,
       "failed" : 0
     },
     "_seq_no" : 0,
     "_primary_term" : 1
   }

Before going into more detail, let's query this document with another
REST API call:

.. code-block:: bash
   :linenos:
   :emphasize-lines: 0

   $ curl -X GET '192.168.78.11:9200/my-index/my-type/1?pretty'

This call gives us this JSON response:

.. code-block:: json
   :linenos:
   :emphasize-lines: 8

   {
     "_index" : "my-index",
     "_type" : "my-type",
     "_id" : "1",
     "_version" : 1,
     "found" : true,
     "_source" : {
       "my_document" : "my document content"
     }
   }

These are the basic steps to store and retrieve documents in |es|.

.. note::

   For centralized logging, where log entries are considered immutable, the
   versioning support is rather uninteresting. In case you got curious,
   take a look at [#esversion]_.

It's also worth nothing that the automatic index creation can be
disabled if you see the need for it [#esindexdis]_.
You're also every time allowed to create your indices
beforehand [#esindexcreate]_:



List Indices
------------

Now that we have an (automatically created) index, we can query it:

.. code-block:: bash
   :linenos:
   :emphasize-lines: 0

   $ curl -X GET 192.168.78.11:9200/_cat/indices?format=yaml

Again, we use the ``format=yaml`` simply to have a more readable output:

.. code-block:: yaml
   :linenos:
   :emphasize-lines: 4

   ---
   - health: "yellow"
     status: "open"
     index: "my-index"
     uuid: "u4WB1ztWT1GVXGOI0OoJnQ"
     pri: "5"
     rep: "1"
     docs.count: "1"
     docs.deleted: "0"
     store.size: "4.5kb"
     pri.store.size: "4.5kb"

Now that we know the basic interaction with |es|, let's use it as
a centralized logging server in the next section.



Logging to |es|
===============

Custom logger


Basic CRUDL operations
======================

.. code-block:: bash
   :linenos:
   :emphasize-lines: 0

    [markus@local]$ curl -X GET 192.168.78.11:9200/app/_search?pretty=true
    {
      "took" : 1,
      "timed_out" : false,
      "_shards" : {
        "total" : 5,
        "successful" : 5,
        "skipped" : 0,
        "failed" : 0
      },
      "hits" : {
        "total" : 3,
        "max_score" : 1.0,
        "hits" : [
          {
            "_index" : "app",
            "_type" : "logs",
            "_id" : "KpBcvWAB78EA2Ko2WrB2",
            "_score" : 1.0,
            "_source" : {
              "timestamp" : "foo",
              "message" : "bar",
              "module" : "app",
              "level" : "INFO"
            }
          },
          {
            "_index" : "app",
            "_type" : "logs",
            "_id" : "K5BgvWAB78EA2Ko2Q7B-",
            "_score" : 1.0,
            "_source" : {
              "timestamp" : "foo",
              "message" : "info message",
              "module" : "app",
              "level" : "INFO"
            }
          },
          {
            "_index" : "app",
            "_type" : "logs",
            "_id" : "LJBhvWAB78EA2Ko2k7Dy",
            "_score" : 1.0,
            "_source" : {
              "timestamp" : "foo",
              "message" : "info message",
              "module" : "app",
              "level" : "INFO"
            }
          }
        ]
      }
    }


Conclusion
==========

Logging to the HTTP address itself doesn't make sense. We will
use *Logstash* in the next post which does that for us.


questions
---------

* Q: Horizontal scale out of |es| instances?




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


References
==========

.. [#vagrinst] https://www.vagrantup.com/docs/installation/

.. [#ansinst] http://docs.ansible.com/ansible/latest/intro_installation.html

.. [#vbinst] https://www.virtualbox.org/wiki/Downloads

.. [#concepts] https://www.elastic.co/guide/en/elasticsearch/reference/6.1/_basic_concepts.html

.. [#lucene] https://lucene.apache.org/

.. [#commonapi] https://www.elastic.co/guide/en/elasticsearch/reference/6.1/common-options.html

.. [#yamllist] http://www.yaml.org/spec/1.2/spec.html#id2797382

.. [#esversion] https://www.elastic.co/guide/en/elasticsearch/reference/6.1/docs-index\_.html#index-versioning

.. [#esindexdis] https://www.elastic.co/guide/en/elasticsearch/reference/6.1/docs-index\_.html#index-creation

.. [#esindexcreate] https://www.elastic.co/guide/en/elasticsearch/reference/6.1/indices-create-index.html