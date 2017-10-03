
.. post:: 29 Sep, 2017
   :tags: logrotate, logging
   :title: Basics about Logrotate

.. spelling::
   Rackspace
   Xenial
   wildcards
   logrotation

======================
Basics about logrotate
======================

Ever lost a host because one of the services on that host used all
available disk space with its logs? *logrotate* is a common tool
which truncates your logs to make sure this won't happen anymore.
This post is a short *how-to*.

.. contents::
    :local:
    :backlinks: top


.. list-table:: Change history:
   :widths: 1 5
   :header-rows: 1

   * - Date
     - Change description
   * - 2017-09-29
     - The first release

Use Case
========

Like described in the abstract before, almost every software supports a
way to log its internal actions to log files. Mostly with different
types of severities like *critical*, *error*, *warning*, *info* and *debug*.
The most verbose one, *debug*, can sometimes create so many log entries in
the designated log file, that this file uses all of the available disk space
of the host. We had this recently with the software *Zuul*, a project
gating system developed for the OpenStack Project [1]_. In general, log
rotation is recommended practice by the *OpenSCAP Security Guide* [2]_
and good background information is available at Rackspace [3]_.

Installation
============

This post explains a manual setup on:

* Ubuntu 16.04 Xenial release
* on *IBM Z s390x* platform (it's the same for x86, though)

An automatized way is available with the *Ansible* role
*openstack/ansible-role-logrotate* [4]_, but that won't be discussed
further here.

Let's check the available packages:

.. code-block:: text

    root@zuul:~# apt-cache policy logrotate
    logrotate:
      Installed: (none)
      Candidate: 3.8.7-2ubuntu2.16.04.1
      Version table:
         3.8.7-2ubuntu2.16.04.1 500
            500 http://ports.ubuntu.com/ubuntu-ports xenial-updates/main s390x Packages
         3.8.7-2ubuntu2 500
            500 http://ports.ubuntu.com/ubuntu-ports xenial/main s390x Packages

We install the package:

.. code-block:: text

    root@zuul:~# apt install -y logrotate

And lastly double-check the version of *logrotate*:

.. code-block:: text

    root@zuul:~# logrotate --version
    logrotate 3.8.7


Configuration
=============

We want the configuration to achieve these goals:

#. keep the last 4 rotated logs before purging the oldest logs
#. rotate the logs every week
#. compress the old, rotated log files to save disk space
#. if there is no log file, be cool and keep calm
#. if the log file is empty, do nothing

This policy should be applied to all files in a specific directory. As
we mentioned the *Zuul* software before, we configure it for this
service which logs everything into ``/var/log/zuul``.

Create the logrotate config file ``zuul-logs`` in the directory
``/etc/logrotate.d/``:

.. code-block:: text

    root@zuul:~# cat /etc/logrotate.d/zuul-logs
    /var/log/zuul/*.log {
        rotate 4
        weekly
        compress
        missingok
        notifempty
      }

The name of the file is arbitrarily chosen, you can choose whatever you like.
You'll notice that the five goals are reflected in the configuration. More
possibilities are described at [5]_. You also see that we can use wildcards
``*`` in the path, which is handy when a service creates multiple log files,
like *Zuul* does.

Dry-Run
=======

After we configured *logrotate*, we can do a dry-run, to see
what would or wouldn't change, if *logrotate* would run normally.
Your output might look similar to this:

.. code-block:: text
   :emphasize-lines: 1,7,13,14,19,21

    root@zuul:~# logrotate -d /etc/logrotate.conf
    reading config file /etc/logrotate.conf
    including /etc/logrotate.d
    reading config file apt
    reading config file dpkg
    reading config file rsyslog
    reading config file zuul-logs

    Handling 9 logs

    [...]

    rotating pattern: /var/log/zuul/*.log  weekly (4 rotations)
    empty log files are not rotated, old logs are removed
    switching euid to 0 and egid to 112
    considering log /var/log/zuul/gearman-debug.log
      log needs rotating
    considering log /var/log/zuul/gearman.log
      log does not need rotating
    considering log /var/log/zuul/merger-debug.log
      log needs rotating
    considering log /var/log/zuul/server-debug.log
      log needs rotating
    considering log /var/log/zuul/server.log
      log needs rotating

    [...]

Unnecessary clutter in the output got stripped away with ``[...]`` and the
interesting lines are highlighted. If you see errors in your output,
see the section :ref:`issues` below.


Rotate manually
===============

We don't want to wait for a week until the first logrotate gets done
automatically. Therefore we do an (optional) manual logrotate to see
how it would look like every week. Let's check the log files **before**
logrotate got enforced for a first run:

.. code-block:: text
   :emphasize-lines: 7

    root@zuul:~# ls -lh /var/log/zuul
    total 4.1G
    -rw-r--r-- 1 zuul zuul 463M Aug  4 13:02 gearman-debug.log
    -rw-r--r-- 1 zuul zuul    0 Jul 13 12:49 gearman.log
    -rw-r--r-- 1 zuul zuul 4.9M Aug  4 12:55 merger-debug.log
    -rw-r--r-- 1 zuul zuul 1.5K Aug  2 04:24 merger.log
    -rw-r--r-- 1 zuul zuul 3.5G Aug  4 13:02 server-debug.log
    -rw-r--r-- 1 zuul zuul 100M Aug  4 13:02 server.log

*Zuul* produced multiple log files, the most interesting one in this
example is the ``server-debug.log`` which uses 3.5G of disk space.

The overall system disk space **before** we do the logrotate:

.. code-block:: text
   :emphasize-lines: 5

    root@zuul:~# df -h
    Filesystem      Size  Used Avail Use% Mounted on
    udev            4.0G     0  4.0G   0% /dev
    tmpfs           806M   87M  719M  11% /run
    /dev/vda1        29G  6.4G   21G  24% /
    tmpfs           4.0G     0  4.0G   0% /dev/shm
    tmpfs           5.0M     0  5.0M   0% /run/lock
    tmpfs           4.0G     0  4.0G   0% /sys/fs/cgroup


Start one **manual logrotation** to see that things work out:

.. code-block:: text

    root@zuul:~# # this can take a minute
    root@zuul:~# logrotate -f /etc/logrotate.d/zuul-logs

The ``-f`` parameter forces a logrotation although the criteria are not
met. You have to specify the configuration file you want to apply here.

Let's look at the log files **after** logrotate got enforced for a first run:

.. code-block:: text

    root@zuul:~# ls -lh /var/log/zuul
    total 322M
    -rw-r--r-- 1 zuul zuul  28K Aug  4 13:14 gearman-debug.log
    -rw-r--r-- 1 zuul zuul  16M Aug  4 13:12 gearman-debug.log.1.gz
    -rw-r--r-- 1 zuul zuul    0 Jul 13 12:49 gearman.log
    -rw-r--r-- 1 zuul zuul 544K Aug  4 12:55 merger-debug.log.1.gz
    -rw-r--r-- 1 zuul zuul  411 Aug  2 04:24 merger.log.1.gz
    -rw-r--r-- 1 zuul zuul 445K Aug  4 13:14 server-debug.log
    -rw-r--r-- 1 zuul zuul 300M Aug  4 13:12 server-debug.log.1.gz
    -rw-r--r-- 1 zuul zuul 3.7K Aug  4 13:14 server.log
    -rw-r--r-- 1 zuul zuul 5.4M Aug  4 13:12 server.log.1.gz

You see the compressed files which end with ``*.gz``. The number gets
incremented with each logrotation. That means:

* the higher the number the older the compressed logs
* the lower the number the younger the compressed logs

As an example, ``server.log.2.gz`` is older than ``server.log.1.gz``.
Please note that these compressed archives get **renamed** when a new
logrotation happens.

The compression reduced the file ``server-debug.log`` from 3.5G to 300M.
This is also reflected in the overall system disk space:

.. code-block:: text
   :emphasize-lines: 5

    root@zuul:~# df -h
    Filesystem      Size  Used Avail Use% Mounted on
    udev            4.0G     0  4.0G   0% /dev
    tmpfs           806M   87M  719M  11% /run
    /dev/vda1        29G  2.8G   25G  11% /
    tmpfs           4.0G     0  4.0G   0% /dev/shm
    tmpfs           5.0M     0  5.0M   0% /run/lock
    tmpfs           4.0G     0  4.0G   0% /sys/fs/cgroup


Rotate continuously
===================

The manual rotation we did before was only to demo the result. We
can rely on the *cronjob* for logrotate which gets set up at during package
install and runs daily:

.. code-block:: text
   :emphasize-lines: 15

    root@zuul:~# cat /etc/cron.daily/logrotate
    #!/bin/sh

    # Clean non existent log file entries from status file
    cd /var/lib/logrotate
    test -e status || touch status
    head -1 status > status.clean
    sed 's/"//g' status | while read logfile date
    do
        [ -e "$logfile" ] && echo "\"$logfile\" $date"
    done >> status.clean
    mv status.clean status

    test -x /usr/sbin/logrotate || exit 0
    /usr/sbin/logrotate /etc/logrotate.conf

The ``/etc/logrotate.conf`` reads all configuration files in
``/etc/logrotate.d/*``. That's the place where we put our config
file from the beginning.

Logrotate also saves its status in a file:

.. code-block:: text

    root@zuul:~# cat /var/lib/logrotate/status
    logrotate state -- version 2
    "/var/log/zuul/server.log" 2017-8-4-13:12:8
    "/var/log/zuul/gearman-debug.log" 2017-8-4-13:12:8
    "/var/log/zuul/server-debug.log" 2017-8-4-13:12:8
    "/var/log/zuul/gearman.log" 2017-8-4-13:0:0
    "/var/log/zuul/merger-debug.log" 2017-8-4-13:12:8


.. _issues:

Known issues
============

The ``logrotate -d`` dry-run might show this:

.. code-block:: text

    root@zuul:~# logrotate -d /etc/logrotate.conf
    reading config file /etc/logrotate.conf
    error: /etc/logrotate.conf:7 unknown group 'syslog'
    removing last 0 log configs

Apparently there is an issue with the (non-)existence of the group
``syslog`` which is the default owning group in the logrotate config:

.. code-block:: text

    root@zuul:~# cat /etc/logrotate.conf | grep syslog
    # use the syslog group by default, since this is the owning group
    # of /var/log/syslog.
    su root syslog

But that user/group doesn't exist in plain Ubuntu 16.04, which
is a confirmed Ubuntu upstream bug [6]_. According to this bug report,
the user/group gets created when *rsyslog* is installed. This is currently
not the case:

.. code-block:: text

    root@zuul:~# ll /var/log/ | grep syslog

Let's install *rsyslog* (which creates the ``syslog`` user/group which
is expected by logrotate):

.. code-block:: text

    root@zuul:~# apt install rsyslog
    [...]
    root@zuul:~# ll /var/log/syslog
    -rw-r----- 1 syslog adm 65999 Aug 15 07:45 /var/log/syslog

After that, the expected group is available and logrotate can do its work.


Conclusion
==========
This post showed you how you can use *logrotate* to prevent log files
from growing too big. Depending on your logging strategy you might also
want to look into tools like *elasticsearch*, *logstash*, *rsyslog* and
*journalctl*.


References
==========

.. [1] https://docs.openstack.org/infra/system-config/zuul.html

.. [2] https://static.open-scap.org/ssg-guides/ssg-ubuntu1604-guide-default.html#xccdf_org.ssgproject.content_group_log_rotation

.. [3] https://support.rackspace.com/how-to/understanding-logrotate-utility/

.. [4] https://github.com/openstack/ansible-role-logrotate

.. [5] https://linux.die.net/man/8/logrotate

.. [6] https://bugs.launchpad.net/ubuntu/+source/logrotate/+bug/1644996
