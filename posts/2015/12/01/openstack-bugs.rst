

.. post:: 01 Dec, 2015
   :category: openstack
   :tags: bugs
   :title: OpenStack's Bug Management

.. |tracker-name| replace:: *Launchpad*

==========================
OpenStack's Bug Management
==========================

This post intends to give you enough background to play an active part in
working with bugs in *OpenStack*. This includes an understanding of the
basic life cycle a bug goes through and in which state you can contribute
in which way. It also clarifies some possible misunderstandings and gives a
few best practices. In general, the bugs of a project (like *Nova*, *Cinder*,
*Neutron* and others) can be found in our issue tracker |tracker-name|. The
lists of bugs are available at ``https://bugs.launchpad.net/<projectname>`` for
example ``https://bugs.launchpad.net/nova`` for the *Nova* project.

.. contents::
    :local:
    :backlinks: top

Change history:

==========  =================================================================
Date        Change description
==========  =================================================================
2015-12-01  The first release
2016-03-05  Added a change history
==========  =================================================================


Overview of the Life Cycle
==========================

This is the most basic (and slightly simplified) life cycle of a bug:

.. blockdiag::
   :desctable:

   blockdiag {

      // layout the diagram
      orientation = portrait

      // The nodes and their transitions
      "New" -> "Triaged" -> "In Progress";
      "New" -> "Confirmed" -> "In Progress";
      "In Progress" -> "Fix Committed" -> "Fix Released";
      "New" -> "Won't Fix";
      "New" -> "Opinion";
      "New" -> "Invalid";
      "New" -> "Incomplete";

      // create sub sets of the nodes with special meaning
      group {
          label = "Open States";
          color = "LightYellow";
          "New"; "Incomplete"; "Triaged"; "In Progress"; "Confirmed";
      }
      group {
          label = "Rejected States";
          color = "LightPink";
          orientation = portrait
          "Won't Fix"; "Opinion"; "Invalid";
      }
      group {
          label = "Accepted States";
          color = "LightGreen";
          orientation = portrait  // prevents an ugly layout of the lines...
          "Fix Committed"; "Fix Released";
      }

      // Appearance and description of the nodes
      "New" [
        description = "The bug was just created and no one has looked
                       at it yet",
        color="yellow"];
      "Incomplete" [
        description = "The bug is waiting on input from the reporter
                       (other issue trackers name this status *NEEDINFO*)",
        color="yellow"];
      "Confirmed" [
        description = "The bug was reproduced or confirmed as a genuine bug
                       from someone other than the reporter",
        color = "yellow"];
      "Triaged" [
        description = "The bug comments contain a full analysis on how to
                       properly fix the issue",
        color = "yellow"];
      "In Progress" [
        description = "The assignee of the bug is working on a fix",
        color = "yellow"];
      "Fix Committed" [
        description = "The branch containing the fix was merged into master",
        color = "green"];
      "Fix Released" [
        description = "The fix is included in the proposed/* branch, a past
                       milestone or a past release",
        color="green"];
      "Invalid" [
        description = "This is not a bug, could be a feature request",
        color = "red"];
      "Opinion" [
        description = "This is a valid issue, but it is the way it should be",
        color = "red"];
      "Won't Fix" [
        description = "This is a valid issue, but we don't intend to fix that",
        color = "red"];
   }

The purpose of an issue tracker is to improve the quality of the project. An
improvement has happened when the bug is in an "Accepted Status" like
``Fix Committed`` or ``Fix Released``.

A bug ending up in any of the "Rejected States" (``Won't Fix``, ``Opinion`` or
``Invalid``) -- which may happen for a variety of reasons including that the
proposed bug is actually a result of operator error or is out of scope --
arguably hasn't directly improved the project. But it could suggest or make it
clear that a concept is not as intuitive or well documented as it should be.

The "Open States" (``New``, ``Incomplete``, ``Triaged``, ``Confirmed`` and
``In Progress``) call for ongoing effort of one or many contributors.


Reporting a New Bug
===================

When reporting a bug please provide at least the minimal information necessary
to enable another contributor to understand **why** you think that this is an
issue. We have a lot of contributors, each one with a different background,
with a specific set of knowledge and with a different depth in OpenStack. It
is unlikely that everyone understands instantly **why** an incident or workflow
didn't pass your expectation.

A possible template, which helps others to understand you, could be::

    Description
    ===========
    Some prose which explains more in detail what this bug report is
    about. If the headline of this report is descriptive enough,
    skip this section.

    Steps to reproduce
    ==================
    A chronological list of steps which will bring off the
    issue you noticed:
    * I did X
    * then I did Y
    * then I did Z
    A list of openstack client commands would be the most
    descriptive example.

    Expected result
    ===============
    After the execution of the steps above, what should have
    happened if the issue wasn't present?

    Actual result
    =============
    What happened instead of the expected result?
    How did the issue look like?

    Environment
    ===========
    1. Exact version of OpenStack you are running. See the following
       list for all releases: http://docs.openstack.org/releases/
       For the current stable release "Liberty" it is:
       http://docs.openstack.org/releases/releases/liberty.html

        If this is from a distro please provide
            $ dpkg -l | grep <projectname>
            or
            $ rpm -ql | grep <projectname>
        If this is from git, please provide
            $ git log -1

    2. Which storage type did you use?
       (For example: Ceph, LVM, GPFS, ...)

    3. Which networking type did you use?
       (For example: nova-network, Neutron with OpenVSwitch, ...)

    Logs
    ====

    The tool *sosreport* has support for some OpenStack projects.
    It's worth having a look at it. For example, if you want to collect
    the logs of a compute node you would execute:

        $ sudo sosreport -o openstack_nova --batch

    on that compute node. Attach the logs to this bug report.



For a more detailed rationale why this information is necessary read the
`Bug Filing Recommendations
<https://wiki.openstack.org/wiki/BugFilingRecommendations>`_ from the
*OpenStack* wiki.

Tooling Support
---------------

When you report a bug you will face some typical issue which can be solved
with appropriate tooling support. Below are the situations you will most
likely encounter in your role as bug reporter.

**Q:** *I want to paste logs or console commands or config files in my bug*
*report, what do I use?*

    **A:** Try `pastebin <http://paste.openstack.org/>`_. It's easy to read and
    provides a lot of preconfigured highlightings. Just reference from your
    bug description to the pastebin link.

**Q:** *I want to show a console session (where possibly timing is relevant).*
*How do I link to that in my bug report?*

    **A:** Try `showterm <http://showterm.io/>`_. It records your console
    session and replays it with all input and output in the exact timing it
    happened. Just reference from your bug description to the *showterm* link.

Security
--------

If you have found a bug which shows a vulnerability and could therefore be
a threat to the security of OpenStack, please contact the `Vulnerability
Management Team <https://security.openstack.org/vmt-process.html>`_.
Also, when you report the bug, ensure that you mark the bug as a *security*
bug. This bug will then be *private* and only accessible to you and the
*Vulnerability Management Team*. This stalls the exploit of this vulnerability
and gives the team more time to react appropriately.

Status and Contributor Responsibility
=====================================

We can distinguish among multiple roles in the bug process. A contributor
can have more than one role:

* **reporter**: Discovered the bug and created the entry in |tracker-name|.
* **triager**: Checks new bugs for validity and makes a presorting
  (see `Tags`_). They are also encouraged to take part in:

  * solving inconsistencies (see `Status and Fields`_)
  * and cleanup (the projects define their own rules for that).

* **bug-supervisor**: Is aware of the "big picture" of the bugs and sets the
  importance of this bug related to the overall bugs.
* **assignee**: Responsible for developing a patch for this bug.
* **release mgmt.**: An (automated) entity which tracks the committed fix of a
  bug.

The following table should be read like:

    *"The bug has the status [...] and in the role of a/an [...], I am*
    *supposed to work with this bug if there is an 'x'."*:

+---------------+----------+---------+------------+----------+--------------+
|               | reporter | triager | supervisor | assignee | release-mgmt |
+---------------+----------+---------+------------+----------+--------------+
| New           |          |    x    |            |          |              |
+---------------+----------+---------+------------+----------+--------------+
| Incomplete    |    x     |         |            |          |              |
+---------------+----------+---------+------------+----------+--------------+
| Triaged       |          |         |    x       |          |              |
+---------------+----------+---------+------------+----------+--------------+
| Confirmed     |          |         |    x       |          |              |
+---------------+----------+---------+------------+----------+--------------+
| In Progress   |          |         |            |    x     |              |
+---------------+----------+---------+------------+----------+--------------+
| Fix Committed |          |         |            |          |    x         |
+---------------+----------+---------+------------+----------+--------------+
| Fix Released  |          |         |            |          |    x         |
+---------------+----------+---------+------------+----------+--------------+
| Won't Fix     |    x     |         |            |          |              |
+---------------+----------+---------+------------+----------+--------------+
| Opinion       |    x     |         |            |          |              |
+---------------+----------+---------+------------+----------+--------------+
| Invalid       |    x     |         |            |          |              |
+---------------+----------+---------+------------+----------+--------------+

Examples:

#. If you are the bug reporter and you get a notification that the state of the
   bug is ``Incomplete``, please read the comments of the bug and provide the
   requested necessary information. After that, set the status back to ``New``.
#. If you see a ``New`` bug and could reproduce the issue, you can set the state
   to ``Confirmed``.
#. If you see a ``New`` bug and know where the issue has its root cause,
   label the bug with one or more of the *tags* (see `Tags`_)
#. If you are the assignee of a bug, you're expected to provide a patch in a
   reasonably timely manner. If you think you're incorrectly assigned, move
   the bug state back to the most recent valid state and remove yourself as
   assignee, so another person can take it.
#. If you are the bug reporter and the state of the bug is ``Won't Fix`` or
   ``Opinion`` or ``Invalid``, please read the rationale of the contributor who
   set the the bug to this state. If you don't agree with the provided
   rationale, it's fine to set the status to ``New`` again and explain why
   you don't agree.
#. If you are a bug-supervisor, please ensure that ``Triaged`` and
   ``Confirmed`` bugs are prioritized.

Status and Fields
=================

|tracker-name| provides a lot of fields for a bug entry. This makes the
sorting and querying of bugs easier and is the base for release management.
Not every combination of bug status and bug fields makes sense. As a
guideline, read the following table as

    *"The bug has the status [...]. A bug in this status should have the*
    *fields [...] set. I should be in the role of a [...] to set*
    *these fields."*:

+---------------+------------------------------------+-------------------+
| Status        | Fields which should be set         | Contributor Role  |
+===============+====================================+===================+
| New           | title, description, tags, affects  | reporter, triager |
+---------------+------------------------------------+-------------------+
| Incomplete    | title, description, tags, affects  | reporter          |
+---------------+------------------------------------+-------------------+
|               | title, description, tags, affects  |                   |
| Triaged       | Importance                         | bug-supervisor    |
+---------------+------------------------------------+-------------------+
|               | title, description, tags, affects  |                   |
| Confirmed     | Importance                         | bug-supervisor    |
+---------------+------------------------------------+-------------------+
|               | title, description, tags, affects  |                   |
| In Progress   | Importance, Assigned to            | assignee          |
+---------------+------------------------------------+-------------------+
|               | title, description, tags, affects  |                   |
| Fix Committed | Importance, Assigned to            | N/A               |
+---------------+------------------------------------+-------------------+
|               | title, description, tags, affects  |                   |
| Fix Released  | Importance, Assigned to, Milestone | release mgmt.     |
+---------------+------------------------------------+-------------------+
| Won't Fix     | N/A                                | N/A               |
+---------------+------------------------------------+-------------------+
| Opinion       | N/A                                | N/A               |
+---------------+------------------------------------+-------------------+
| Invalid       | N/A                                | N/A               |
+---------------+------------------------------------+-------------------+

.. note::

   Only the bug-supervisor sets the importance of a bug. The bug-supervisors
   are the core reviewers and a group of volunteers. In other words, usually
   you are not supposed to set ``Importance`` or ``Milestone``.

Status Transitions Details
==========================

As a bug is moved along the process to being fixed, some bug state transitions
can lead to confusion to contributors. The following are examples of how some
of these common state transitions and how they should be handled.


.. blockdiag::

   blockdiag {
      New -> Incomplete;
      Incomplete -> New;
   }

If there is not enough information provided, contributors switch the bug from
``New`` to ``Incomplete`` and ask the reporters for more details. When the
reporters provide that information, they switch the status back to ``New``.

.. blockdiag::

   blockdiag {
      New -> "Fix Committed";
      Incomplete -> "Fix Committed";
      Triaged -> "Fix Committed";
      Confirmed -> "Fix Committed";
   }

Sometimes a bug is reported and the issue is solved by another patch which
wasn't aware of the specific bug. It's totally acceptable to set this bug to
``Fix Committed`` and link to the patch which solved it. This reduces the
monitoring effort for bugs in "Open States" whereby other bugs can get more
focus.

.. blockdiag::

   blockdiag {
      New -> "Confirmed";
   }

The issue was reproduced by someone other than the reporter. You don't need
to be in the role of a "bug-supervisor" to do that. Every contributor is
encouraged to do so.

.. blockdiag::

   blockdiag {
      "In Progress" -> "Confirmed", "New", "Triaged";
   }

Sometimes an issue is assigned and set to ``In Progress`` but there is no
progress in a long time for a variety of reasons, for example:

* the review for that issue was abandoned
* the was no review for that issue
* the review was "left alone" with a ``-1``

To enable other contributors to work on that issue, remove the assigne and
set the status to the last known before it was set to ``In Progress``. Every
project will handle that policy in a somewhat different way.

Contributions
=============

There are several key tasks with regards to bugs that anyone can do:

#. Tag ``New`` bugs with the project specific tags (see `Tags`_).
#. Confirm new bugs: When a bug is filed, it is set to the ``New`` status.
   A ``New`` bug can be marked ``Confirmed`` once it has been reproduced
   and is thus confirmed as genuine.
#. Solve inconsistencies: Make sure bugs are Confirmed, and if assigned
   that they are marked ``In Progress`` (see `Status and Fields`_)
#. Check ``Incomplete`` bugs: See if information that caused them to be
   marked ``Incomplete`` has been provided, determine if more information is
   required and provide reminders to the bug reporter if they haven't
   responded after 2-4 weeks.
#. Check stale ``In Progress`` bugs: Work with assignee of bugs to determine
   if the bug is still being worked on, if not, unassign them and mark them
   back to the last known state.

Tags
====

|tracker-name| provides *Tags*. They are a way to label bugs with certain
keywords to enable better sorting in one or more categories. Because some of
the projects are so huge and span multiple layers, services and components,
it is impossible to be an expert in each of those areas. The tagging of a bug
enables contributors to create a query for bugs to which they can contribute
their expertise. Each project has its own set of tags and an overview can be
found in the `wiki <https://wiki.openstack.org/wiki/Bug_Tags>`_.

Best Practices
==============

**Discussions in the issue tracker**:

The longer the discussion gets and the more contributors take part, the more
complicated it will get to understand who is talking to whom about what. If
you want to answer on a comment from another contributor, try to use this as
the first line in your answer::

    @<name> in reply to comment #<N>:

This makes it also easier in notification e-mails to spot that a reaction is
necessary. Unfortunately |tracker-name| doesn't support this in an automated
way.

Conclusion
==========

This post should have given you an overview how the bug management in OpenStack
is (usually) done. Although this will differ from project to project it should
give you a good start. There are ongoing efforts to move away from *Launchpad*
to another platform, but I'm confident that the overall way how to deal with
bugs won't be differ too much to what is described in this post.

.. note:: The content of this post was initially intended to be part of the
  official docs of *OpenStack* but there was no project which had the right
  scope for that. See `the nova review <https://review.openstack.org/187571>`_
  and `the infra-manual review <https://review.openstack.org/192232>`_
  for more details.