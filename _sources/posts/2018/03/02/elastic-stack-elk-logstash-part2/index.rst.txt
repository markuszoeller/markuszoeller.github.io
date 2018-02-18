

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
We continue we're we left of the last time, and dive right into it.
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

.. todo:: TODO



A more realistic logging data
=============================

.. todo:: example python app with log file



Parse logging data by delimiter
===============================

.. todo:: dissect



Parse logging data by patterns
==============================

.. todo:: grok



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

