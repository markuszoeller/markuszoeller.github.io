
.. todo:: date, tags and title

.. post::
   :tags: template
   :title: title


=====
Title
=====

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

unsorted stuff
==============


There is an APT package available::

    $ apt-cache policy logrotate
    logrotate:
      Installed: (none)
      Candidate: 3.8.7-2ubuntu2.16.04.1
      Version table:
         3.8.7-2ubuntu2.16.04.1 500
            500 http://ports.ubuntu.com/ubuntu-ports xenial-updates/main s390x Packages
         3.8.7-2ubuntu2 500
            500 http://ports.ubuntu.com/ubuntu-ports xenial/main s390x Packages

Log rotation is recommended by the OpenSCAP Security Guide
https://static.open-scap.org/ssg-guides/ssg-ubuntu1604-guide-default.html#xccdf_org.ssgproject.content_group_log_rotation

Good background information:
https://support.rackspace.com/how-to/understanding-logrotate-utility/

There is a Ansible role openstack/ansible-role-logrotate:
https://github.com/openstack/ansible-role-logrotate

Installation of logrotate::

    $ sudo apt install -y logrotate
    $ logrotate --version
    logrotate 3.8.7

Create the logrotate config for the zuul services::

    $ cat /etc/logrotate.d/zuul-logs
    # mzoeller: 2017-08-04:
    # This is added manually and needs to be replaced with an Ansible approach.

    /var/log/zuul/*.log {
        rotate 4
        weekly
        compress
        missingok
        notifempty
      }


Log files before logrotate got enforced for a first run::

    $ sudo ls -lh /var/log/zuul
    total 4.1G
    -rw-r--r-- 1 zuul zuul 463M Aug  4 13:02 gearman-debug.log
    -rw-r--r-- 1 zuul zuul    0 Jul 13 12:49 gearman.log
    -rw-r--r-- 1 zuul zuul 4.9M Aug  4 12:55 merger-debug.log
    -rw-r--r-- 1 zuul zuul 1.5K Aug  2 04:24 merger.log
    -rw-r--r-- 1 zuul zuul 3.5G Aug  4 13:02 server-debug.log
    -rw-r--r-- 1 zuul zuul 100M Aug  4 13:02 server.log


The overall system disk space (before)::

    $ df -h
    Filesystem      Size  Used Avail Use% Mounted on
    udev            4.0G     0  4.0G   0% /dev
    tmpfs           806M   87M  719M  11% /run
    /dev/vda1        29G  6.4G   21G  24% /
    tmpfs           4.0G     0  4.0G   0% /dev/shm
    tmpfs           5.0M     0  5.0M   0% /run/lock
    tmpfs           4.0G     0  4.0G   0% /sys/fs/cgroup


Start one logrotation manually to see that things work out::

    # this can take a minute
    $ sudo logrotate -f /etc/logrotate.d/zuul-logs



Log files after logrotate got enforced for a first run::

    $ sudo ls -lh /var/log/zuul
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


The overall system disk space (after)::

    $ df -h
    Filesystem      Size  Used Avail Use% Mounted on
    udev            4.0G     0  4.0G   0% /dev
    tmpfs           806M   87M  719M  11% /run
    /dev/vda1        29G  2.8G   25G  11% /
    tmpfs           4.0G     0  4.0G   0% /dev/shm
    tmpfs           5.0M     0  5.0M   0% /run/lock
    tmpfs           4.0G     0  4.0G   0% /sys/fs/cgroup


The cronjob for logrotate gets set up at during package install and runs daily::

    -rwxr-xr-x 1 root root 372 Mar 22 10:18 /etc/cron.daily/logrotate*
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

The status of logrotate gets stored at::

    root@zuul:~# cat /var/lib/logrotate/status
    logrotate state -- version 2
    "/var/log/zuul/server.log" 2017-8-4-13:12:8
    "/var/log/zuul/gearman-debug.log" 2017-8-4-13:12:8
    "/var/log/zuul/server-debug.log" 2017-8-4-13:12:8
    "/var/log/zuul/gearman.log" 2017-8-4-13:0:0
    "/var/log/zuul/merger-debug.log" 2017-8-4-13:12:8

After more research I found the logrotate -d parameter which
is a dry-run of logrotate. It showed this::

    root@zuul:~# logrotate -d /etc/logrotate.conf
    reading config file /etc/logrotate.conf
    error: /etc/logrotate.conf:7 unknown group 'syslog'
    removing last 0 log configs

Apparently there is an issue with the group syslog which is the default
in logrotates config::

    root@zuul:~# cat /etc/logrotate.conf | grep syslog
    # use the syslog group by default, since this is the owning group
    # of /var/log/syslog.
    su root syslog

That user/group doesn't exist in plain Ubuntu 16.04, which
is a confirmed Ubuntu upstream bug:
https://bugs.launchpad.net/ubuntu/+source/logrotate/+bug/1644996

According to this bug report, the user/group gets created when rsyslog
is installed. This is currently not the case::

    root@zuul:~# ll /var/log/ | grep syslog

Let's install rsyslog (which creates the syslog user/group which
is expected by logrotate)::

    root@zuul:~# apt install rsyslog
    [...]
    root@zuul:~#
    root@zuul:~#
    root@zuul:~# ll /var/log/syslog
    -rw-r----- 1 syslog adm 65999 Aug 15 07:45 /var/log/syslog

After installing rsyslog which creates the syslog group/user,
we do a try-run of logrotate again and see more actions::

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



References
==========

.. [1] www.google.com
