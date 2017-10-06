
.. todo:: date, tags and title

.. post::
   :tags: template
   :title: How to add Prometheus monitoring instrumentation to your application


.. spelling::
   async


====================================================================
How to add Prometheus monitoring instrumentation to your application
====================================================================

brain dump
==========

https://prometheus.io/docs/instrumenting/clientlibs/

* write a small app with multithreading / pools / stuff to monitor
* add prometheus instrumentation to your app
* monitor those instrumented app metrics
* do weird stuff with the app's API to influence the metrics
  * thread pool bug?
  * async job duration?
  * logged in users?
  * current transactions?

* display that funny stuff


-----



.. todo:: abstract

.. contents::
    :local:
    :backlinks: top

.. todo:: date

.. list-table:: Change history:
   :widths: 1 5
   :header-rows: 1

   * - Date
     - Change description
   * - YYYY-MM-DD
     - The first release

TL;DR
=====

.. todo:: short conclusion here

Use Case
========

.. todo:: describe the use case here

sub-title
=========

.. todo:: explain more here and reference to it [1]_

References
==========

.. [1] www.google.com
