
.. post:: 19 Jan, 2018
   :tags: ansible, quick-tips
   :title: Quick Tip: Ansible commands as non-root user with environment variables

.. spelling::
   foo



=========================================================================
Quick Tip: *Ansible* commands as non-root user with environment variables
=========================================================================


This is a short quick tip. When executing *Ansible* playbooks, you might
need to execute a task as another user than the one you established the
connection with. This post shows an example how to do it and deal with
the environment variables.



.. list-table:: Change history:
   :widths: 1 5
   :header-rows: 1

   * - Date
     - Change description
   * - 2018-01-19
     - The first release

While working on my previous post :ref:`elastic-stack-elk-elasticsearch`
I had the need to run a task as another user and with specific environment
variables set. It took me surprisingly long to figure out a way to do
it, so here it is:


.. literalinclude:: playbook.yml
   :language: yaml
   :linenos:
   :emphasize-lines: 8,12,41-44

The most important part is ``sudo -E -u`` [#mansudo]_:

* For ``-E``, the man page says:

  .. code-block:: text

     The -E (preserve environment) option indicates to the security
     policy that the user wishes to preserve their existing environment
     variables. [...]

* For ``-u``, the man page says:

  .. code-block:: text

     The -u (user) option causes sudo to run the specified
     command as a user other than root. [...]

As you already guessed, the environment variables get set for the ``root``
user and the context switch with ``sudo`` preserves these variables for
the other user. The started binary ``./bin/elasticsearch`` uses these
environment variables to populate placeholders in a not shown config file.
I've shown it here with *Elasticsearch* specifics, but there are other
situations where you and I might need this in the future.

.. warning::

   Although this gets the job done, it feels somehow wrong and probably
   any of the other options listed at [#ansunprev]_ are more appropriate.
   I didn't yet had the time to wrap my head around the impact of
   the solutions proposed there.


References
==========

.. [#mansudo] https://linux.die.net/man/8/sudo

.. [#ansunprev] https://docs.ansible.com/ansible/latest/become.html#becoming-an-unprivileged-user

