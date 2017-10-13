
.. todo:: date, tags and title

.. post::
   :tags: monitoring
   :title: Monitoring with Prometheus


.. specific terms I use quite often

.. |ans| replace:: *Ansible*
.. |prom| replace:: *Prometheus*
.. |graf| replace:: *Grafana*
.. |vagr| replace:: *Vagrant*
.. |vb| replace:: *VirtualBox*


==========================
Monitoring with Prometheus
==========================

One of the worst calls you can get as developer, is one from the user
who complains that the service is slow or -- even worse -- doesn't
respond anymore. A user should **never know before you**, that your
service doesn't behave in its parameters anymore. One of the common
causes for service degradation or interruption is still the failure
or exhaustion of your basic infrastructure resources. This post gives you an
intro how you can monitor your basic resources with |prom|. It shows
the setup with |ans| and the data visualization with |graf|.


.. contents::
    :local:
    :backlinks: top

.. todo:: date

.. list-table:: Change history:
   :widths: 1 5
   :header-rows: 1

   * - Date
     - Change description
   * - 2017-10-27
     - The first release

Use Case
========

Monitoring is a way of collecting and storing data (so called *metrics*)
so that you can extrapolate a trend out of the historic view, to give
you insights if preemptive actions are necessary to keep your promised
*Service Level Agreements* (SLAs).

This post will focus on the monitoring aspect of the resources your
service can consume. Specifically I'll go into details of monitoring:

* CPU
* memory
* disk space

For example, if you don't use *logrotation*, it's easy to consume all
disk space and become unserviceable. A bug in the thread handling can
also slow down your CPUs. And a good old memory leak is never out of fashion.

I cannot stress enough that having historic data is very valuable. A singel
point in time observation is not enough. The show case here will use a specific
setup, which is explained below.


Setup Overview
==============

Our end result will look like this:

.. todo::
   rename the servers and all code to "monitoring" and "app-server-N".
   Don't forget to redo the screenshots with the correct names.

.. image:: topology.svg
   :alt: The topology of our demo setup.
   :target: /_images/topology.svg

We will have 3 servers:
  * one monitoring server
  * two application server

The application server will have small applications which consume different
types of resources. This will demonstrate the influence on the collected
metrics, which are stored on the monitoring server within |prom|. The
code we use to do that is below:

**Consume CPU**

.. literalinclude:: eat_cpu.py
   :caption: file: eat_cpu.py :download:`(download) <eat_cpu.py>`
   :name: eat_cpu
   :language: python
   :linenos:

**Consume Memory**

.. literalinclude:: eat_memory.py
   :caption: file: eat_memory.py :download:`(download) <eat_memory.py>`
   :name: eat_memory
   :language: python
   :linenos:

**Consume Disk Space**

.. literalinclude:: eat_disk.py
   :caption: file: eat_disk.py :download:`(download) <eat_disk.py>`
   :name: eat_disk
   :language: python
   :linenos:

We will deploy those demo applications to the application servers
and trigger them after the monitoring is establish. More on that later.

Server Provisioning
===================

To create the servers described before, I'll utilize |vagr| with |vb| as
hypervisor. I use the term *provisioning* in the sense of creating the
servers and configuring the basic infra support functions (which includes
the monitoring). The configuration is done with |ans|. There are multiple
files included in this operation, they get explained piece by piece below.
The short version of the actions you have to trigger is:

.. code-block:: bash
   :caption: All you need to do in your console
   :linenos:

   $ vagrant up                                    # create the server
   $ ansible-playbook -i hosts.ini playbook.yml    # install monitoring
   $ firefox http://192.168.100.10:3000/           # or any other browser

But more on that later, when the necessary parts are explained.

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

.. literalinclude:: prometheus.yml
   :caption: file: prometheus.yml :download:`(download) <prometheus.yml>`
   :name: prometheus-config
   :language: yaml
   :linenos:
   :emphasize-lines: 1

.. important::
   In newer versions of Prometheus, ``target_groups`` got replaced by
   ``static_configs`` [promstatic]_ .

I'm going to use more and more
Ansible examples in this blog, as this is my tool of choice for such
tasks. Doing such things with the shell looks smaller and easier at first,
but the more nodes you have, the more *Ansible* comes in handy.


After this is done, we will use this hosts file for *Ansible*:

.. literalinclude:: hosts.ini
   :caption: file: hosts.ini :download:`(download) <hosts.ini>`
   :name: hostsfile
   :language: ini
   :linenos:
   :emphasize-lines: 1

.. warning::
  Don't store passwords like that when using *Ansible*. Use the
  *Ansible Vault* feature [ansivault]_ for that.

It's this *Ansible* playbook:

.. literalinclude:: playbook.yml
   :caption: file: playbook.yml :download:`(download) <playbook.yml>`
   :name: playbook
   :language: yaml
   :linenos:
   :emphasize-lines: 1
   :lines: 3-19



.. note::
   It's perfectly fine to start *Ansible* playbooks like I did here.
   For example, when you transition from shell scripts. At some point in
   time you should very strongly consider to encapsulated logic into
   *Ansible roles* [ansiroles]_.

Now execute the playbook locally (not in any of the VMs):

.. code-block:: bash
   :linenos:

   $ ansible-playbook -i hosts.ini playbook.yml


.. note:: It's possible to use Vagrant's Ansible provisioner directly
 in the Vagrantfile, but to have a more realistic scenario here,
 I separated these steps.

After the playbooks is executed
open the prometheus server UI at http://192.168.100.10:9090/status .
You should see that all the expected targets are listend and in state ``UP``
like in this image:

.. image:: prometheus-targets-status.png
   :target: /_images/prometheus-targets-status.png
   :alt: Prometheus status page with the expected outcome.

.. todo:: double-check the naming of the servers here, I might have renamed
   them at some point.

At http://192.168.100.10:9090/graph you can start using the Prometheus
query language [promq]_ to create graphs based on the metrics the
Prometheus server scrapes from the targets in an interval. For example,
you can query the available disk space from the nodes by using
``node_filesystem_free{mountpoint='/'}``:

* ``node_filesystem_free``: This is the metric you're interested in
* ``{mountpoint='/'}``: This is a constraint you can specify

.. image:: prometheus-graph.png
   :target: /_images/prometheus-graph.png
   :alt: Prometheus graph page with a query for free disk space

You'll notice very quickly that this gets ugly. For example, the metric
is in bytes, and you cannot transform it to a human readable unit. Let's
use *Grafana* to visualize that in a sensible way.

The Ansible playbook also installed and configured the Grafana service,
which is accessible at http://192.168.100.10:3000/ .

Sign in as username ``admin`` and password ``admin``.


Conclusion
==========

This post showed how to monitor operating system metrics with
*Grafana*, *Prometheus* und *Prometheus Node Exporter*. The deployment
of the software happened with *Ansible*, after the server provisioning
was done with *Vagrant* and *VirtualBox*. We deployed the necessary
software by using the packaged versions from *Ubuntu*. Unfortunately,
it got decided that *Grafana* won't be in release *17.10* and newer [grafdrop]_.
This is a good chance to show in another post, how we can create
*Ansible Roles* to encapsulate the logic of getting the newest *Grafana*
source code, building it, and deploying it. This also enables us to
to make use of the much nicer API [grafds]_ and UI.

Those node metrics aren't the only metrics you can collect. There is a
variety of different exporters [promex]_ which help you to keep the overview.
You can also instrument your own application to emit metrics. That's something
I will show in another post.


References
==========


.. todo:: 
   make numbers out of these references and order them accordingly
   when the post is finalized.


.. [promstatic] https://github.com/prometheus/prometheus/issues/1706

.. [promq] https://prometheus.io/docs/querying/basics/

.. [ansivault] http://docs.ansible.com/ansible/latest/playbooks_vault.html

.. [grafds] http://docs.grafana.org/http_api/data_source/

.. [ansiroles] http://docs.ansible.com/ansible/latest/playbooks_reuse_roles.html

.. [grafdrop] https://answers.launchpad.net/ubuntu/+source/grafana/+question/658771

.. [promex] https://prometheus.io/docs/instrumenting/exporters/
