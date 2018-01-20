
.. post::
   :tags: logging, elasticstack
   :category: monitoring
   :title: Elastic Stack (formerly ELK) - Logstash

.. spelling::
   tokenized


.. |es| replace:: *Elasticsearch*
.. |ls| replace:: *Logstash*



=========================================
Elastic Stack (formerly ELK) - *Logstash*
=========================================

abstract

Some notes:

* Logging as a Service with *Elastic* Cloud Enterprise
* data flow pipelines (pipe to pipe to pipe)
* independent pipelines in one |ls| instance
* "beats" protocol
* "event" is the primary unit which gets sent to |ls|
* "workers" scale out the processing
* in-memory queue vs. persistent queue
* "at least once" delivery (err on the side of duplication)
* codecs serialize and deserialize
* ``json_lines`` codecs is available  # non-human
* ``dissect`` is the "smaller version" of ``grok`` (delimiter vs regex)
* *kibana* can monitor |ls| and |es|  # not sure
* |ls| has an external REST API for metrics



.. contents::
    :local:
    :backlinks: top


.. list-table:: Change history:
   :widths: 1 5
   :header-rows: 1

   * - Date
     - Change description
   * - 2018-mm-dd
     - The first release


Intro
=====

This is the second part of a multi-part series about the
*Elastic Stack* (formerly the **ELK stack**). This stack
consists of 3 parts:

* **storing data** with |es|
* **ingesting data** with |ls| (and/or *Beats*)
* **visualizing data** with *Kibana*

This post will focus on the second part, |ls|, ...



Set up the environment
======================

To reproduce the steps in this post, you need to have installed locally:

* *Vagrant* [#vagrinst]_
* *Ansible* [#ansinst]_
* *VirtualBox* [#vbinst]_

After these **prerequisites** are fulfilled:

#. download the compressed
   :download:`project source files <elastic-stack-elk-logstash.tar.gz>`.
#. extract the archive
#. change to the ``env`` directory
#. start the *Vagrant* setup
#. use *Ansible* to configure the environment

.. code-block:: bash
   :linenos:
   :emphasize-lines: 0

   $ wget http://www.markusz.io/_downloads/elastic-stack-elk-logstash.tar.gz
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


This created a **virtualized environment** which looks like this:

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

Let's start with an overview of the basic **concepts** [#concepts]_.
I'll explain the details after this image:

.. todo:: TODO


Basic Interaction with |es|
===========================

.. todo:: TODO


Summary
=======

.. todo:: TODO


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

.. [#flask] http://flask.pocoo.org/

.. [#pylog] https://docs.python.org/2/howto/logging.html#logging-basic-tutorial

.. [#pylogrot] https://docs.python.org/2/library/logging.handlers.html#logging.handlers.RotatingFileHandler

.. [#essearch] https://www.elastic.co/guide/en/elasticsearch/reference/current/search.html

.. [#rsyslog] http://www.rsyslog.com/
