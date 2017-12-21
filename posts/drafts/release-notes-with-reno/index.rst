

.. post::
   :tags: release-management
   :title: Release Notes with reno


=========================
Release Notes with *reno*
=========================

*"What features merged since the last release?"* --
*"Did we introduce something which might break a deployment?"* --
*"Let me grep through the commit history to check what happened."*
Remember sentences like these when you're about to release? If you
like this fire-fighting mode, ignore this post. If you want to have a
more relaxed release, this post will show you how to use a tool called
*reno* to manage your release notes.



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

Below is the shortest end-to-end example I can think of. The steps are:

#. Install the needed software
#. Create a git repository
#. Create a release note with *reno*
#. Commit the release note to the repo
#. Create a report out of all committed release notes

I trimmed some of the unnecessary output with *[...]*:

.. code-block:: bash
   :linenos:
   :emphasize-lines: 0

    $ apt-get install -y git                     # reno operates on git repos
    $ git init                                   # initialize a git repo
    $ git config user.name "John Doe"            # configure git repo (1/2)
    $ git config user.email "jd@example.com"     # configure git repo (2/2)
    $ apt-get install -y python-pip              # we will install reno with pip
    $ pip install reno                           # install reno from PyPi
    $ reno new my-first-release-note             # create a release note
    Created new notes file in releasenotes/notes/my-first-release-note-21b284249cec129c.yaml
    $ git add -A                                 # Add the release note to the repo
    $ git commit -m "Add my first release note"  # commit the release note
    $
    $ reno list                                  # list the release notes
    scanning ./releasenotes/notes (branch=*current* earliest_version=None)
    including entire branch history
    21b284249cec129c: adding releasenotes/notes/my-first-release-note-21b284249cec129c.yaml from 0.0.0
    0.0.0
        releasenotes/notes/my-first-release-note-21b284249cec129c.yaml (01a57fb590b9145fbc6bd24bb924c8f62396bf22)
    $
    $ reno report                                # create a report
    scanning ./releasenotes/notes (branch=*current* earliest_version=None)
    including entire branch history
    21b284249cec129c: adding releasenotes/notes/my-first-release-note-21b284249cec129c.yaml from 0.0.0
    =============
    Release Notes
    =============

    0.0.0
    =====

    Prelude
    -------

    .. releasenotes/notes/my-first-release-note-[...]

    Replace this text with content [...]

    New Features
    ------------

    .. releasenotes/notes/my-first-release-note-[...]

    - List new features here, or remove this section. [...]


    Known Issues
    ------------

    .. releasenotes/notes/my-first-release-note-[...]

    - List known issues here, or remove this section. [...]


    Upgrade Notes
    -------------

    .. releasenotes/notes/my-first-release-note-[...]

    - List upgrade notes here, or remove this section. [...]


    Deprecation Notes
    -----------------

    .. releasenotes/notes/my-first-release-note-[...]

    - List deprecations notes here, or remove this section. [...]


    Critical Issues
    ---------------

    .. releasenotes/notes/my-first-release-note-[...]

    - Add critical notes here, or remove this section. [...]


    Security Issues
    ---------------

    .. releasenotes/notes/my-first-release-note-[...]

    - Add security notes here, or remove this section. [...]


    Bug Fixes
    ---------

    .. releasenotes/notes/my-first-release-note-[...]

    - Add normal bug fixes here, or remove this section. [...]


    Other Notes
    -----------

    .. releasenotes/notes/my-first-release-note-[...]

    - Add other notes here, or remove this section. [...]


Things you notice from this example are:

* *reno* creates its release notes in a directory ``releasenotes`` under
  the root directory of your project.
* A release note is a ``YAML`` file which uses a combination of the
  name you provided and a hash-like text. This ensures uniqueness in
  file names.
* The default template which our release note is based on used
  embedded *restructured text* for the markup of our prose.
* The report combines all of our release notes (only one so far) into
  something you can use in a release letter.
* The report also lists a version number (``0.0.0`` in this example)
  which can be influenced with *git tagging*.

.. note::
   Most of the content in this post is based on [#reno]_.

The next sections will dive deeper into specific questions on how to
use reno in your (most likely code driven) project.



Use Case
========

It got developed to fit the needs
of the *OpenStack* upstream development, but it can be used in any other
project as well.

.. todo:: describe the use case here



Benefits
========

* The release notes can be reviewed like code.
* The release note is part of the code change which makes the release note
  necessary.
* Backports to stable branches already contain the release note.
* Merge conflicts to the common release letter are next to impossible
* Have a (customizable) template of release specific sections which are
  the most important ones for your users
* A *Sphinx document generator* plugin is available.



Alternatives
============

Alternatives could be:

* Make the release note part of the git commit message.
* Only use files with a naming convention and parse them separately.
* Use the git notes feature.



Content
=======

.. todo:: add stuff here

Conclusion
==========

.. todo:: explain more here and reference to it [1]_

References
==========

.. [1] www.google.com

.. [#reno] https://docs.openstack.org/reno/latest/

