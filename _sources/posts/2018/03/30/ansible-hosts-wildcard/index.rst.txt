
.. post:: Mar 30, 2018
   :tags: ansible, quick-tips
   :title: Quick Tip: Ansible target hosts with wildcard

.. spelling::
   foo



===============================================
Quick Tip: *Ansible* target hosts with wildcard
===============================================


This is a short quick tip about *Ansible*. TL;DR: it's possible to use a
wildcard in the target hosts specifier. This became useful to me when I
dynamically created the inventory based on *Ansible* facts.

.. list-table:: Change history:
   :widths: 1 5
   :header-rows: 1

   * - Date
     - Change description
   * - 2018-03-30
     - The first release

My scenario was, that I wanted to **document the installation procedure**
of a tool I wrote. I needed to document that for at least CentOS and Ubuntu.
That tool depends on operating system packages, which are named differently
for Ubuntu and CentOS. To avoid that the documentation goes out of sync
with reality, I decided to write *Ansible* code, which can be executed and
therefore **tested continuously**, and include that code in my documentation.

To test that, I had a local *Vagrant* environment and wanted to ensure that
it works on Ubuntu 16.04 and CentOS 7.4 for the start.
As I expected that this will grow over time with **different distributions**
and **each distribution with a set of major-minor releases**, I wanted to
avoid to control the *Ansible* targets with an inventory file and also don't
bind them to host names. So I decided to use the ``gather_facts`` option,
to read specifics about the hosts, and **dynamically group** them based on
distribution, major release number, minor release number.

When doing that,
I discovered that the facts gather the major release number and the full
release number, which is ``16.04`` for Ubuntu, but ``7.4.1708`` for CentOS.


.. code-block:: bash
   :linenos:
   :emphasize-lines: 6,8

   [root@centos ~]# ansible localhost -m setup | grep ansible_distri
           "ansible_distribution": "CentOS",
           "ansible_distribution_file_parsed": true,
           "ansible_distribution_file_path": "/etc/redhat-release",
           "ansible_distribution_file_variety": "RedHat",
           "ansible_distribution_major_version": "7",
           "ansible_distribution_release": "Core",
           "ansible_distribution_version": "7.4.1708",


My expectation was, that I somehow get ``7.4``, without the patch level,
but I couldn't find a way. I also wanted to avoid to do string split magic
in *Ansible*.

As I was worried that I have to change the playbook when the patch level
changes when updating the CentOS 7 *Vagrant Box* I wanted to have a way
to ignore the patch level. And apparently, *Ansible* can do that with a
**wildcard** ``*`` **in the target hosts specifier**. I ended up with this:

.. code-block:: yaml
   :linenos:
   :emphasize-lines: 9,10,17

   ---

   - hosts: all
     become: true
     gather_facts: true

     tasks:
       - name: "Group the servers by operating system and version."
         group_by:
           key: os_{{ ansible_distribution }}_{{ ansible_distribution_version }}

   - hosts: os_Ubuntu_16.04
     become: true
     tasks:
       - include: ubuntu_1604_install_tasks.yml

   - hosts: os_CentOS_7.4*
     become: true
     tasks:
       - include: centos_74_install_tasks.yml


The specifier ``os_CentOS_7.4*`` accepts, that the actual key is
``os_CentOS_7.4.1708``, which solves my problem perfectly.

For my user documentation with *Sphinx* I could then do this:

.. code-block:: rst
   :linenos:
   :emphasize-lines: 0

   Below are examples of *Ansible tasks*, which show the operating system
   dependencies which must be fulfilled.

   Ubuntu 16.04
   ------------

   .. literalinclude:: ubuntu_1604_install_tasks.yml
      :language: yaml


   CentOS 7.4
   ----------

   .. literalinclude:: centos_74_install_tasks.yml
      :language: yaml


This enables me to only **document working examples**, which can easily
be changed. Either by adding a new target, or removing a target which
reached its end of life or support level.

For details about *Sphinx* you can read my previous post
:ref:`project-docs-rst-markup-sphinx`.
I thought this might be worth sharing.
