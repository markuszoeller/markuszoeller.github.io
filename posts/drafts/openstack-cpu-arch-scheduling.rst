

.. post::
   :tags: openstack, nova, scheduling, cpu-architecture
   :title: OpenStack Nova Scheduling based on CPU architecture


===================================================
OpenStack Nova Scheduling based on CPU architecture
===================================================



.. contents::
    :local:
    :backlinks: top

Change history:

==========  =================================================================
Date        Change description
==========  =================================================================
2017-??-??  The first release
==========  =================================================================

TL;DR
=====

Use ``hw_architecture`` instead of ``architecture``.

* OpenStack CLI::

  $ openstack image set <IMG-UUID> --property hw_architecture=s390x

* Ansible module *os_image*::

    - name: "Upload bootable s390x guest image into Glance."
      os_image:
        name: ubuntu_s390x
        filename: /tmp/ubuntu_s390x_disk.img
        container_format: bare
        disk_format: raw
        properties:
          hw_architecture: s390x

..

If that TL;DR doesn't make sense to you, below is the longer version.

Use Case
========
Let's assume you have set up an OpenStack cloud with compute nodes
of different CPU architectures. For example, some Intel x86 compute nodes,
some IBM Z s390x compute nodes (and maybe some IBM POWER ppc64 compute
nodes). Those architectures need guest images which were built for those
architectures. All an OpenStack user sees, is the 3 different guest images

* suse_X  (SUSE guest image for Intel x86 64 bit operating system)
* ubuntu_Z  (Ubuntu guest image for IBM Z s390x 64 bit operating system)
* rhel_P  (RHEL guest image for IBM POWER ppc64 64 bit operating system)

for example. The openstack user doesn't see (and doesn't need to and shouldn't)
the details of the different compute nodes. All they want is that this
architecture specific image gets scheduled on the compute node which can
fulfil their needs.

Guest image metadata properties
===============================

The most reasonable way I know to do this, is to add Glance image metadata,
which specifies the CPU architecture of that image so that other services
can use that information. The one OpenStack service we need for that,
is the Nova scheduler service. Specifically one of its filters, the
``ImagePropertiesFilter``.

Unfortunately, the docs in Glance don't make it **that** obvious which
value you have to set. You will most likely stumble upon the metadata
property ``architecture``. The Glance docs [1]_ say this:

    *"The CPU architecture that must be supported by the hypervisor.*
    *For example, x86_64, arm, or ppc64."*

Sounds like the correct one for your use-case, right? The openstack CLI
also says to use this [2]_.

It gets a bit more confusing when you want to use the *Ansible* module
*os_image* for your *Infrastructure as Code (IaC)*. The example there
uses ``cpu_arch``:

.. code-block:: yaml
   :linenos:
   :emphasize-lines: 8

   - os_image:
       name: cirros
       container_format: bare
       disk_format: qcow2
       state: present
       filename: cirros-0.3.0-x86_64-disk.img
       properties:
         cpu_arch: x86_64
         distro: ubuntu

I'm not sure if that metadata property has any effect anywhere. It hadn't
when I tested the Nova scheduling with it.

Impact to the Nova scheduler
============================

Long story short, I don't know the history of how it happened, but the nova
scheduler filter we want to use needs the property to be named
``hw_architecture`` [4]_.

When this is applied to the image, and a user launches that image,
the nova scheduler filters out hosts which don't offer that CPU architecture.
You can see the filtering happening in the nova scheduler logs. The shortened
example below starts with 2 compute nodes, one x86 and the other s390x:


.. code-block:: text
   :linenos:
   :emphasize-lines: 2,11,12,16

   $ grep filter /var/log/nova/nova-scheduler.log
   DEBUG nova.filters [...] Starting with 2 host(s)
   DEBUG nova.scheduler.filters.retry_filter [...] Re-scheduling is disabled host_passes
   DEBUG nova.scheduler.filters.retry_filter [...] Re-scheduling is disabled host_passes
   DEBUG nova.filters [...] Filter RetryFilter returned 2 host(s)
   DEBUG nova.filters [...] Filter AvailabilityZoneFilter
   DEBUG nova.filters [...] Filter RamFilter returned 2 host(s)
   DEBUG nova.filters [...] Filter ComputeFilter returned 2 host(s)
   DEBUG nova.filters [...] Filter ComputeCapabilitiesFilter returned 2 host(s)
   DEBUG nova.scheduler.filters.image_props_filter [...]
       Instance contains properties ImageMetaProps(hw_architecture='s390x',...)
       that are not provided by the compute node
   DEBUG nova.scheduler.filters.image_props_filter [...] (cmpx1, cmpx1)
       ram: 142990MB disk: 91136MB io_ops: 0 instances: 0
       does not support requested instance_properties
   DEBUG nova.filters [...] Filter ImagePropertiesFilter returned 1 host(s)

You'll notice that the ``ImagePropertiesFilter`` removed the one compute
node which cannot fulfil the ``ImageMetaProps``. We started with 2 hosts
and at the end only one host is an eligible target host for the Instance.

References
==========

.. [1] https://docs.openstack.org/python-glanceclient/latest/cli/property-keys.html

.. [2] https://docs.openstack.org/python-openstackclient/latest/cli/command-objects/image.html#image-set

.. [3] http://docs.ansible.com/ansible/latest/os_image_module.html

.. [4] https://github.com/openstack/nova/blob/4a7502a5c9e84a8c8cef7f355d72425b26b8c379/nova/scheduler/filters/image_props_filter.py#L44


