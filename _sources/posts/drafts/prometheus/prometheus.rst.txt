
.. todo:: date, tags and title

.. post::
   :tags: monitoring
   :title: Monitoring with Prometheus


==========
Prometheus
==========




Brain dump
==========

Save this file:

.. literalinclude:: Vagrantfile
   :caption: file: Vagrantfile :download:`(download) <Vagrantfile>`
   :name: vagrantfile
   :language: ruby
   :linenos:
   :emphasize-lines: 1

Do a ``vagrant up``.


This is how we configure the prometheus server:

.. literalinclude:: prometheus.yml.j2
   :caption: file: prometheus.yml :download:`(download) <prometheus.yml.j2>`
   :name: prometheus-config
   :language: yaml
   :linenos:
   :emphasize-lines: 1

Below are two choices of how to deploy and configure the software.
*Ansible* and the traditional *shell*. I'm going to use more and more
Ansible examples in this blog, as this is my tool of choice for such
tasks. The shell way looks smaller and easier at first, but the more
nodes you have, the more Ansible comes in handy.


.. switch between ansible and shell =======================================

.. tabs::

   .. tab:: The Ansible way

      After this is done, we will use this hosts file for *Ansible*:

      .. literalinclude:: hosts.ini
         :caption: file: hosts.ini :download:`(download) <hosts.ini>`
         :name: hostsfile
         :language: ini
         :linenos:
         :emphasize-lines: 1

      It's this *Ansible* playbook:

      .. literalinclude:: playbook.yml
         :caption: file: playbook.yml :download:`(download) <playbook.yml>`
         :name: playbook
         :language: yaml
         :linenos:
         :emphasize-lines: 1


      Now execute the playbook locally (not in any of the VMs):

      .. code-block:: bash
         :linenos:

         $ ansible-playbook -i hosts.ini playbook.yml


      .. note:: It's possible to use Vagrant's Ansible provisioner directly
         in the Vagrantfile, but to have a more realistic scenario here,
         I separated these steps.

   .. tab:: The shell way

      .. literalinclude:: prometheus-server.sh
         :caption: file: prometheus-server.sh :download:`(download) <prometheus-server.sh>`
         :name: prometheus-server
         :language: bash
         :linenos:
         :emphasize-lines: 1



Open the prometheus server UI at 192.168.100.10 (port?)


----

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

vagrant + ansible in multi node in U1604

Use Case
========

.. todo:: describe the use case here

sub-title
=========

.. todo:: explain more here and reference to it [1]_

References
==========

.. [1] www.google.com
