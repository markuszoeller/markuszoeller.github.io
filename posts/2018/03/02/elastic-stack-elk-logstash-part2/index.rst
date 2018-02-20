

.. Mar 02, 2018

.. post::
   :tags: logging, elasticstack
   :category: monitoring
   :title: Elastic Stack (formerly ELK) - Logstash (Part 2)

.. spelling::
   tokenized


.. |es| replace:: *Elasticsearch*
.. |ls| replace:: *Logstash*
.. |fb| replace:: *Filebeat*
.. |ki| replace:: *Kibana*


==================================================
Elastic Stack (formerly ELK) - *Logstash* (Part 2)
==================================================

This is a follow-up to the previous post
:ref:`elastic-stack-elk-logstash-part1`.
We continue were we left of the last time, and dive right into it.
No intro, no explanation of concepts or terms, only configuration of
|ls| pipelines.


.. contents::
    :local:
    :backlinks: top


.. list-table:: Change history:
   :widths: 1 5
   :header-rows: 1

   * - Date
     - Change description
   * - 2018-03-02
     - The first release


To get most out of this post, it's advisable to read the two previous posts
in this series:

#. :ref:`elastic-stack-elk-elasticsearch`
#. :ref:`elastic-stack-elk-logstash-part1`

If you already know that content, here we go.



Output our example log to |es|
==============================

Create a new pipeline configuration file named
``/etc/logstash/conf.d/elasticsearch.conf`` and add the content below:

.. code-block:: text
   :linenos:
   :emphasize-lines: 0

   input {
     file {
       id => "my-app2-id-in"
       path => "/var/log/app2/source.log"
     }
   }

   output {
     elasticsearch {
       id => "my-app2-id-out"
       hosts => ["http://es1:9200"]
       index => "app2"
     }
   }


Add some log entries to our log file:

.. code-block:: bash
   :linenos:
   :emphasize-lines: 0

   $ echo $(date -Is) >> /var/log/app2/source.log


Query |es| if the new index got created:

.. code-block:: bash
   :linenos:
   :emphasize-lines: 0

   $ curl es1:9200/_cat/indices?format=yaml


The response we get:

.. code-block:: yaml
   :linenos:
   :emphasize-lines: 4,8

   ---
   - health: "yellow"
     status: "open"
     index: "app2"
     uuid: "hL-CbpmmTm2I_aKryzqj-A"
     pri: "5"
     rep: "1"
     docs.count: "2"
     docs.deleted: "0"
     store.size: "11kb"
     pri.store.size: "11kb"


Query |es| for the documents for the index ``app2``:

.. code-block:: bash
   :linenos:
   :emphasize-lines: 0

   $ curl -s es1:9200/app2/_search? | jq


The response we get:

.. code-block:: json
   :linenos:
   :emphasize-lines: 15,20-24

   {
     "took": 1,
     "timed_out": false,
     "_shards": {
       "total": 5,
       "successful": 5,
       "skipped": 0,
       "failed": 0
     },
     "hits": {
       "total": 2,
       "max_score": 1,
       "hits": [
         {
           "_index": "app2",
           "_type": "doc",
           "_id": "YhO3r2EBDLUsSt4lTcKT",
           "_score": 1,
           "_source": {
             "path": "/var/log/app2/source.log",
             "host": "ls1",
             "@version": "1",
             "@timestamp": "2018-02-19T20:18:00.592Z",
             "message": "2018-02-19T20:18:00+00:00"
           }
         },
         {
           "_index": "app2",
           "_type": "doc",
           "_id": "YRO2r2EBDLUsSt4l88J0",
           "_score": 1,
           "_source": {
             "message": "2018-02-19T20:17:36+00:00",
             "path": "/var/log/app2/source.log",
             "@timestamp": "2018-02-19T20:17:37.420Z",
             "host": "ls1",
             "@version": "1"
           }
         }
       ]
     }
   }


|ls| did its job to encapsulate our messages into new JSON objects with
meta data and to forward this JSON object to |es|. To be precise,
the ``elasticsearch`` output plugin did the job. The index also got
created like specified in the config file.

So far, we've used fairly useless data for the log entries. The next
section will use more realistic one.


A more realistic logging data
=============================

Writing the current timestamp into a file was just a vehicle to
have unique log entries, which makes it easier to follow.
Let's create more realistic logging data. This will show us a nice
problem we will solve in the sections after this one.

Create a *Python* script ``example.py`` on server ``ls1`` which logs
into a file:

.. literalinclude:: example-app/example.py
   :language: python
   :linenos:
   :emphasize-lines: 9

The highlighted line is the important one. This line ensures that our
log record data [#pylogrecord]_ will be stored in a file, which will
be the the data source for |ls|.

Create a new pipeline file in ``/etc/logstash/conf.d/es-app3.conf``:

.. code-block:: json
   :linenos:
   :emphasize-lines: 4

   input {
     file {
       id => "my-app3-id-in"
       path => "/var/log/app3/source.log"
     }
   }

   output {
     elasticsearch {
       id => "my-app3-id-out"
       hosts => ["http://es1:9200"]
       index => "app3"
     }
   }


Execute the example app:

.. code-block:: bash
   :linenos:
   :emphasize-lines: 0

   $ vagrant ssh ls1
   $ cd /opt/app3
   $ chmod +x example.py
   $ ./example.py

This creates these entries in ``/var/log/app3/source.log``:

.. code-block:: text
   :linenos:
   :emphasize-lines: 0

   2018-02-20 20:40:25,121 | INFO | 2654 | 140522357225216 | example | main | 18 | Started the application.
   2018-02-20 20:40:25,121 | DEBUG | 2654 | 140522357225216 | example | do_something | 14 | I did something!


Query |es| for the documents for the index ``app3``:

.. code-block:: bash
   :linenos:
   :emphasize-lines: 0

   $ curl -s es1:9200/app3/_search? | jq


The response we get looks like below. I trimmed it down by using ``[...]``
where I removed portions:

.. code-block:: json
   :linenos:
   :emphasize-lines: 11,21

   {
     [...],
     "hits": {
       "total": 2,
       "max_score": 1,
       "hits": [
         {
           [...],
           "_source": {
             "@version": "1",
             "message": "2018-02-20 20:40:25,121 | DEBUG | 2654 | 140522357225216 | example | do_something | 14 | I did something!",
             "@timestamp": "2018-02-20T20:40:36.961Z",
             "path": "/var/log/app3/source.log",
             "host": "ls1"
           }
         },
         {
           [...],
           "_source": {
             "@version": "1",
             "message": "2018-02-20 20:40:25,121 | INFO | 2654 | 140522357225216 | example | main | 18 | Started the application.",
             "@timestamp": "2018-02-20T20:40:36.960Z",
             "path": "/var/log/app3/source.log",
             "host": "ls1"
           }
         },
       ]
     }
   }

Given the knowledge from before, this is the expected outcome.

Assumed we have thousands of log entries like this for a big application
with tons of functions and classes and modules and log levels and threads:
How do we reasonably **query only the log messages** we care about in
a specific scenario?

We could use the builtin query DSL of |es| [#esquery]_ to do searches on the
``message`` value only. This would feel like a ``grep`` and will probably
bring good results at first:

.. code-block:: bash
   :linenos:
   :emphasize-lines: 5

   $ curl -s 'es1:9200/app3/_search' -H 'Content-Type: application/json' -d'
   {
       "query": {
           "match" : {
               "message" : "DEBUG"
           }
       }
   }
   ' | jq


The response we get:

.. code-block:: json
   :linenos:
   :emphasize-lines: 11

   {
     [...]
     "hits": {
       "total": 1,
       "max_score": 0.2876821,
       "hits": [
         {
           [...]
           "_source": {
             "@version": "1",
             "message": "2018-02-20 20:40:25,121 | DEBUG | 2654 | 140522357225216 | example | do_something | 14 | I did something!",
             "@timestamp": "2018-02-20T20:40:36.961Z",
             "path": "/var/log/app3/source.log",
             "host": "ls1"
           }
         }
       ]
     }
   }

The query we provided to |es| matched one of our logging entries.

This is already pretty cool, but maybe we can split the very long
logging message into something more meaningful, which can then
be easier queried.


Parse logging data by delimiter
===============================

.. todo:: dissect



Parse logging data by patterns
==============================

.. todo:: grok



JSON newline delimiter logging
==============================

.. todo:: maybe json newline is a reasonable thing to output when
          working with |es|


A filter to update the timestamp
================================

.. todo:: Use a filter to transform



Store syslog too
================

.. todo:: syslog pattern


Summary
=======

Do I need to install a |ls| server on every application server to gather
my logs?
Nope, |fb| to the rescue. That's an insight I got while writing
this post. So I'll take a quick look at |fb| next, before finishing
this series with |ki|.



References
==========

.. [#pylogrecord] https://docs.python.org/2/library/logging.html#logrecord-attributes

.. [#esquery] https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl.html