

.. post:: Mar 02, 2018
   :tags: logging, elasticstack
   :category: monitoring
   :title: Elastic Stack (formerly ELK) - Logstash (Part 2)

.. spelling::
   tokenized


.. |es| replace:: *Elasticsearch*
.. |ls| replace:: *Logstash*
.. |fb| replace:: *Filebeat*
.. |ki| replace:: *Kibana*
.. |lsconf| replace:: ``/etc/logstash/conf.d/example-app.conf``


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


Use a more realistic logging data
=================================

Writing the current timestamp into a file was just a vehicle to
have unique log entries, which makes it easier to follow.
Let's create more realistic logging data. This will show us nice
problems we will solve in the sections after this one.

After logging into the virtual machine ``ls1`` with ``vagrant ssh ls1``,
create a *Python* script ``example.py`` on server ``ls1`` which logs into
a file:

.. literalinclude:: example-app/example.py
   :language: python
   :linenos:
   :emphasize-lines: 9

The highlighted line is the important one. This line ensures that our
log record data [#pylogrecord]_ will be stored in a file, which will
be the the data source for |ls|.



Make sure the example app can be executed:

.. code-block:: bash
   :linenos:
   :emphasize-lines: 0

   $ chmod +x /opt/example-app/example.py
   $ mkdir -p /var/log/example-app


Create a new pipeline file in |lsconf|:

.. literalinclude:: step3-exampleapp.conf
   :language: text
   :linenos:
   :emphasize-lines: 5-6

.. warning::

   The highlighted lines here tell |ls| to forget where its last scanning
   position was for this file. This means every restart of the |ls| service
   triggers a scan of the whole file. While this allows me to use the same
   logging data throughout this post, which makes following the examples
   easier, it is most likely NOT what you want to have in a production
   environment with tons of logging data.

Restart the |ls| service to read the new config:

.. code-block:: bash
   :linenos:
   :emphasize-lines: 0

   $ systemctl restart logstash.service

Execute the example app:

.. code-block:: bash
   :linenos:
   :emphasize-lines: 0

   $ /opt/example-app/example.py


This creates these entries in ``/var/log/example-app/example.log``:

.. literalinclude:: example.log
   :language: text
   :linenos:
   :emphasize-lines: 0


Query |es| for the documents for the index ``example``:

.. code-block:: bash
   :linenos:
   :emphasize-lines: 0

   $ curl -s es1:9200/example/_search? | jq


The response looks like this:

.. literalinclude:: step3-response.json
   :language: json
   :lines: 1,13-40,42
   :linenos:
   :emphasize-lines: 10,23


.. note::

   I trimmed down the JSON responses in this post, to keep
   the focus on the important parts.

Given the knowledge from before, this is the expected outcome.

Assumed we have thousands of log entries like this for a big application
with tons of functions and classes and modules and log levels and threads:
How do we reasonably **query only the log messages** we care about in
a specific scenario?

We could use the built-in query DSL of |es| [#esquery]_ to do searches on the
``message`` value only. This would feel like a ``grep`` and will probably
bring good results at first:

.. code-block:: bash
   :linenos:
   :emphasize-lines: 5

   $ curl -s 'es1:9200/example/_search' -H 'Content-Type: application/json' -d'
   {
       "query": {
           "match" : {
               "message" : "DEBUG"
           }
       }
   }
   ' | jq


The response we get:

.. literalinclude:: step3-response-match.json
   :language: json
   :linenos:
   :lines: 1,10-27,29
   :emphasize-lines: 3,13


The query we provided to |es| matched one of our logging entries.

This is already pretty cool, but maybe we can split the very long
logging message into something more meaningful, which can then
be queried more easily.


Parse logging data by delimiter
===============================

The ``dissect`` filter plugin [#lsdissect]_ allows to transform your
log entries based on delimiters. It's a good fit for the classical log files
like the one from before.

Change the file |lsconf| to look like this:

.. literalinclude:: step4-dissect.conf
   :language: text
   :linenos:
   :emphasize-lines: 10-16

The highlighted lines are the ones which got added. No changes were
made to the other lines of the previous configuration.

The ``dissect`` filter is based on delimiter but much smarter than
your typical ``split(' ')`` method. The lines we added here in
basically takes ``message`` as input and splits it up into parts.
Everything before ``%{`` and after ``}`` gets treated as a delimiter.
In this case here, it's only a blank. Everything between ``%{`` and ``}``
is a named field. The usage of ``+`` appends the value of this field
to the field of the same name, which was declared before. We used it
here for the timestamp, ``%{time} %{+time}``. It will become more clear
when we see the result of this filter.

Delete the ``example`` index [#esdelidx]_ in |es| and restart
the |ls| service:

.. code-block:: bash
   :linenos:
   :emphasize-lines: 0

   $ curl -X DELETE es1:9200/example/
   $ systemctl restart logstash.service


.. note::

   It takes a few seconds until |ls| is up an running again and realizes
   that there are logs to deal with.

Query |es| with the index ``example``:

.. code-block:: bash
   :linenos:
   :emphasize-lines: 0

   $ curl -s es1:9200/example/_search? | jq


The JSON response we get:

.. literalinclude:: step4-response.json
   :language: json
   :linenos:
   :lines: 1,13-56,58
   :emphasize-lines: 11,32


This shows that our log entries in the log file got properly split up
into fields. Please note that the ``time`` field contains the full timestamp,
although there is a blank between date and time in the log file. This
was possible by the *"append"* syntax ``%{time} %{+time}``.

We should now be able to query |es| for those fields:

.. code-block:: bash
   :linenos:
   :emphasize-lines: 5

   $ curl -s 'es1:9200/example/_search' -H 'Content-Type: application/json' -d'
   {
       "query": {
           "match" : {
               "level" : "DEBUG"
           }
       }
   }
   ' | jq


The response we get:

.. literalinclude:: step4-response-match.json
   :language: json
   :linenos:
   :lines: 1,10-
   :emphasize-lines: 3,13

|es| did correctly find only 1 match for log entries where the ``level``
field has the value ``DEBUG``.


Three things aren't pretty yet:

* The ``message`` field is not necessary anymore, as we have all the
  information in the other fields.
* The ``@timestamp`` field doesn't match our actual timestamp, captured
  in field ``time``.
* The fields which hold numbers as values, like ``line``, ``pid`` and
  ``thread`` treat those values as strings.

The next sections will show ways to do that.


Remove unnecessary fields
=========================

The ``message`` field from above contains the full log entry, but
we don't need that anymore, as we have split that into its fields.
One way to remove that extraneous field, is the ``remove_field`` filter
option.

Change the file |lsconf| to look like this:

.. literalinclude:: step5-dissect-remove-field.conf
   :language: text
   :linenos:
   :emphasize-lines: 15

The highlighted line is the one which got added. Like before:

#. delete the index in |es|
#. restart |ls|
#. query |es|

.. code-block:: bash
   :linenos:
   :emphasize-lines: 0

   $ curl -X DELETE es1:9200/example/
   $ systemctl restart logstash.service
   $ curl -s es1:9200/example/_search? | jq


The response looks now like this:

.. literalinclude:: step5-response.json
   :language: json
   :linenos:
   :lines: 1,13-54,56
   :emphasize-lines: 0

The unnecessary ``message`` field is gone.
It looks much cleaner now. A few more things until we're happy.


Set the timestamp field
=======================

The ``date`` filter plugin [#lsdate]_ is capable of using our ``time`` field
and use it as input for the ``@timestamp`` field:

.. literalinclude:: step6-timestamp.conf
   :language: text
   :linenos:
   :emphasize-lines: 17-20

The ``time`` field served its purpose, so we remove it like shown in the
previous section. This example also shows nicely, that multiple filters
can be specified in one config, and that they get executed in the
given order.

If your log files don't use ISO8601, you can filter for other formats,
like the *Unix* time in seconds or milliseconds since epoch. Any other
format is also valid, e.g. ``"MMM dd yyyy HH:mm:ss"``. See the docs
at [#lsdate]_ for more details.

After changing the file |lsconf| to make it look like the setting
above, we repeat the steps:

#. delete the index in |es|
#. restart |ls|
#. query |es|

.. code-block:: bash
   :linenos:
   :emphasize-lines: 0

   $ curl -X DELETE es1:9200/example/
   $ systemctl restart logstash.service
   $ curl -s es1:9200/example/_search? | jq


.. literalinclude:: step6-response.json
   :language: json
   :linenos:
   :lines: 1,13-52,54
   :emphasize-lines: 0


The ``time`` field is gone and the ``@timestamp`` field uses the date and
time specified in the original log file.



Specify data type conversion
============================

The ``dissect`` filter provides the option ``convert_datatype``
which can do a conversion to integer of float numbers. We only need
conversions to ``int`` here:

.. literalinclude:: step7-convert-datatype.conf
   :language: text
   :linenos:
   :emphasize-lines: 16-20

After changing that in |lsconf|, same story like before:

.. code-block:: bash
   :linenos:
   :emphasize-lines: 0

   $ curl -X DELETE es1:9200/example/
   $ systemctl restart logstash.service
   $ curl -s es1:9200/example/_search? | jq

The JSON request contains numbers now:


.. literalinclude:: step7-response.json
   :language: json
   :linenos:
   :lines: 1,13-52,54
   :emphasize-lines: 13,14,17



This can be useful when you search for a
**range of numeric values** [#esrange]_:

.. code-block:: bash
   :linenos:
   :emphasize-lines: 5-7

   $ curl -s 'es1:9200/example/_search' -H 'Content-Type: application/json' -d'
   {
       "query": {
           "range" : {
               "line" : {
                   "gte" : 10,
                   "lte" : 15
               }
           }
       }
   }
   ' | jq

The response:

.. literalinclude:: step7-response-match.json
   :language: json
   :linenos:
   :lines: 1,10-
   :emphasize-lines: 3,17


This example isn't that impressive, admittedly, but I'm sure you get
the principle and have an idea where this might come in handy with
your log files.



Summary & Outlook
=================

This post showed how a log file with realistic data can be split into
its parts by the ``dissect`` input plugin, and brought into the
|es| service for later queries.

While writing this post, a few questions came up in my mind and maybe
you ask them yourself too:

#. What if ``dissect`` is not powerful enough for my logs?

   There is a more powerful filter, named ``grok``, which is based
   on regular expressions [#grok]_. I don't have plans to dive into
   that filter at the moment.

#. Do I need to install a |ls| server on every application server to
   gather my logs?

   Nope, |fb| to the rescue [#filebeat]_. That's an insight I got while
   writing this post. I will probably look into that at a later point in
   time, after I talked about |ki|.

#. How do I get my *syslog*, to get the bigger picture?

   There is a syslog input plugin [#syslog]_, but I couldn't get it to work
   yet, although the intro looks easy. I tried different things but have
   to table that to a follow-up post in the future.

#. Doesn't using the ``dissect`` filter create a contract on the structure
   of my log file?

   Yeah, I think so. Adding another field to the logger of your application
   will most likely break the defined mapping. The structure of log files
   doesn't change that often, I guess. I was still wondering if it may
   be reasonable to create log files with *JSON Lines* [#jsonline]_.
   This would imply that a log file is NOT supposed anymore to get read
   directly by humans, but to get used as input for a log file processing
   engine like |ls|. Not sure if this change would be welcomed by every one.
   Maybe I'll give it a try in a follow-up post.

We have enough in place to put a nice GUI on top of it. In *ELK*, this
is |ki|. The next post in this series will show this.



References
==========

.. [#pylogrecord] https://docs.python.org/2/library/logging.html#logrecord-attributes

.. [#esquery] https://www.elastic.co/guide/en/elasticsearch/reference/6.2/query-dsl.html

.. [#lsdissect] https://www.elastic.co/guide/en/logstash/6.2/plugins-filters-dissect.html

.. [#esdelidx] https://www.elastic.co/guide/en/elasticsearch/reference/6.2/indices-delete-index.html

.. [#lsdate] https://www.elastic.co/guide/en/logstash/6.2/plugins-filters-date.html

.. [#esrange] https://www.elastic.co/guide/en/elasticsearch/reference/6.2/query-dsl-range-query.html

.. [#grok] https://www.elastic.co/guide/en/logstash/6.2/plugins-filters-grok.html

.. [#filebeat] https://www.elastic.co/products/beats/filebeat

.. [#syslog] https://www.elastic.co/guide/en/logstash/6.2/plugins-inputs-syslog.html

.. [#jsonline] http://jsonlines.org/