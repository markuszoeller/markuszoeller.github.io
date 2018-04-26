
.. post:: Apr 27, 2018
   :tags: apt, packaging, ubuntu
   :title: Ubuntu with Debian Sid APT repository

.. spelling::
   foo


.. |l| replace:: *libguestfs*


=========================================
*Ubuntu* with *Debian Sid* APT repository
=========================================

Ubuntu is great in my opinion, and of the reasons for it is its use of
recent versions for the packages in their APT repositories. But what if
you need a package in an even more recent version and cannot wait for the
next release? The Debian Sid release, the unstable development version, has
those newer packages and they can be used in an Ubuntu with the help of
APT package pinning and this post shows the things you need to know for that.


.. contents::
    :local:
    :backlinks: top


.. list-table:: Change history:
   :widths: 1 5
   :header-rows: 1

   * - Date
     - Change description
   * - 2018-04-27
     - The first release



Use Case
========

The specific case I had, was the usage of the great tool |l| [#libgfs]_,
which is very useful when dealing with virtual machine disk images.
Unfortunately, when I tried to work with it on the s390x architecture,
I've discovered a bug, which was already reported upstream [#bugisa]_.
Luckily, there was also already a patch series provided on the mailing list
of |l| [#patchml]_ and the last commit, needed to fix the bug,
was also already merged [#commitx86]_ and available with version 1.37.22
of |l|.

My problem was, Ubuntu 16.04 packaged |l| in version 1.34
and Ubuntu 18.04 packaged it in version 1.36. Both were too old and
didn't contain any backports. As Ubuntu is based on Debian, I checked
their repositories and found the needed version 1.38 of |l|
in their unstable development release named Sid [#sid]_.

From the multiple options I had:

* use Debian Sid as host
* build |l| from source
* wait for CentOS 7.5 which has |l| 1.36 but with backports
* wait for Ubuntu 18.10 (in the hope it has the fixes/backports)
* use Ubuntu 18.04 and add the Debian Sid repositories

proved only the last one successful for me and the next sections show
the needed actions for this.



Add the Debian Sid repository
=============================

Install the needed packages and add the keys and the Debian Sid repo itself:

.. code-block:: bash
   :linenos:
   :emphasize-lines: 0

   $ apt update
   $ apt install -y software-properties-common \
   debian-archive-keyring \
   dirmngr
   $ apt-key adv --keyserver keyserver.ubuntu.com \
   --recv-keys 8B48AD6246925553
   $ apt-key adv --keyserver keyserver.ubuntu.com \
   --recv-keys 7638D0442B90D010
   $ add-apt-repository "deb http://ftp.de.debian.org/debian sid main"

If you don't use the ``apt-key`` command before adding the repository,
you'll see this error message:

.. code-block:: text
   :linenos:
   :emphasize-lines: 0

   Err:3 http://ftp.de.debian.org/debian sid InRelease
     The following signatures couldn't be verified because the
     public key is not available:
     NO_PUBKEY 8B48AD6246925553
     NO_PUBKEY 7638D0442B90D010
   E: The repository 'http://ftp.de.debian.org/debian sid InRelease'
   is not signed.
   N: Updating from such a repository can't be done securely,
   and is therefore disabled by default.

After the Sid release is added to the repository list, we need to deal
with the fact that we have the same packages in different versions in
different repositories, which can confuse APT a little.


Pin the |l| related packages
============================

The APT package preferences can be tuned with *preference* files. This
is also called **package pinning**. In my case, I was only interested in
getting the newest |l| packages.


Create the file ``/etc/apt/preferences.d/libguestfs.pref`` with this content:

.. code-block:: text
   :linenos:
   :emphasize-lines: 0

   # workaround for bug:
   # https://bugs.launchpad.net/ubuntu/+source/libguestfs/+bug/1766534
   #
   # Note: 2 blank lines are required between entries
   Package: *
   Pin: release a=bionic
   Pin-Priority: 500


   Package: *
   Pin: origin "ftp.de.debian.org"
   Pin-Priority: 300


   # Pattern includes 'python-guestfs' and 'libguestfs-tools' and similarily
   # named dependencies:
   Package: *guestfs*
   Pin: origin "ftp.de.debian.org"
   Pin-Priority: 700


The ``Pin-Priority`` is the key. The higher the value, the more likely
the matching packages get installed. The lower the value, the less likely
it is that they get installed. The priority ``500`` is the default priority.
If the pattern matches on multiple repositories and the priority is the same,
the newest package gets installed.

The preferences file above can be read as:

* All packages (``*``) from the ``bionic`` release have the (default)
  priority of ``500``.
* All packages (``*``) which originate from the ``ftp.de.debian.org``
  repository server, have a low priority of ``300``.
* All packages, which have ``guestfs`` in their name and originate
  from the ``ftp.de.debian.org`` repository server, have the high priority
  of ``700``.

This means, that every time you do an ``apt install <package-name>``,
this list gets checked to figure out which repository to use. You can
check the impact of that configuration with the command
``apt-cache policy <package-name>``, as shown in the next section.


Check with ``apt-cache policy``
===============================

The command ``apt-cache policy <package-name>`` is a good way to determine
what package would be installed from which repository, in case you trigger
the install with ``apt-get install <package-name>``.

Let's check how this looks with a common package, e.g. ``nano``:

.. code-block:: bash
   :linenos:
   :emphasize-lines: 0

   $ apt-cache policy nano
   nano:
     Installed: (none)
     Candidate: 2.9.3-2
     Version table:
        2.9.5-1 300
           300 http://ftp.de.debian.org/debian sid/main s390x Packages
        2.9.3-2 500
           500 http://ports.ubuntu.com/ubuntu-ports bionic/main s390x Packages

The package is **in both repositories**, the newer one with version
``2.9.5-1`` is in Debian Sid and gets the priority ``300``, but the older
one in Ubuntu with version ``2.9.3-2`` has a higher priority of ``500``
and is therefore the install candidate.

Let's try the package I'm interested in, ``libguestfs-tools``, which matches
the pattern described in the preferences file from before:

.. code-block:: bash
   :linenos:
   :emphasize-lines: 0

   $ apt-cache policy libguestfs-tools
   libguestfs-tools:
     Installed: (none)
     Candidate: 1:1.38.0-4
     Version table:
        1:1.38.0-4 700
           300 http://ftp.de.debian.org/debian sid/main s390x Packages
        1:1.36.13-1ubuntu3 500
           500 http://ports.ubuntu.com/ubuntu-ports bionic/universe s390x Packages

The package is in both repositories, the newer one is in Debian Sid,
and it has the higher priority because its name matches the pattern we
specified in the preferences file, and is therefore the install candidate
with a priority of ``700``.


Conclusion
==========

With all the things from above, I was able to get the packages (and their
dependencies) in a version current enough to get the job done.


It is also possible to enforce downgrades of a package or avoid an
installation at all. The man page [#prefs]_ has the details you need to
determine how to fulfill your use case.

Doing that in a multi-purpose host which needs to be kept updated, brings
the risk that you potentially make that system unstable and less predictable.
Doing that in a single-purpose immutable host, e.g. packaged as Docker image,
might be a good enough band-aid until a new Ubuntu release comes out which
contains the package in the version you need.



References
==========

.. [#libgfs] http://libguestfs.org/
.. [#bugisa] https://bugzilla.redhat.com/show_bug.cgi?id=1376547
.. [#patchml] https://www.redhat.com/archives/libguestfs/2017-May/msg00066.html
.. [#commitx86] https://github.com/libguestfs/libguestfs/commit/5b60dd4eff02f48d344bcdad0d4bad4676ca9168
.. [#sid] https://packages.debian.org/sid/s390x/libguestfs0/download
.. [#prefs] https://linux.die.net/man/5/apt_preferences