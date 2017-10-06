
.. todo:: date, tags and title

.. post::
   :tags: template
   :title: etcd - a distributed key-value store


.. spelling::
   etcd
   

====
etcd
====

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

https://github.com/andrewrothstein/ansible-etcd-cluster

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


unsorted stuff
==============

* 3 VMs (set up with Vagrant and Ansible)
* clustered etcd on those VMs
* have a distributed python app which listens to etcd keys
* access applications with haproxy (on one node; HA of HAProxy comes later)
* update key (feature toggle) with Ansible
* the app should watch for that change
* show changed behavior after the value change in etcd
* (optional) with distributed lock management
* (optional) use a non-string value / binary blob
* (optional) revisions of value changes: https://coreos.com/etcd/docs/latest/dev-guide/interacting_v3.html#watch-historical-changes-of-keys
