
.. post::
   :tags: ansible, iac
   :title: Ansible Playbook Refactoring into Roles

.. spelling::
   foo



=======================================
Ansible Playbook Refactoring into Roles
=======================================

Each post should start with one paragraph which is an abstract of the post.
This paragraph should be enough for a reader to decide if they want to
read the post or not. It is best to keep this paragraph short and simple.
100 words or less is the limit, as this abstract is used as excerpt in the
list on the landing page and in the feed readers. This upper limit
of 100 words is also the amount of content someone should be able to read
in less than 20 seconds. Additionally, it fits on one small mobile screen.

.. contents::
    :local:
    :backlinks: top

.. todo:: date of the change history

.. list-table:: Change history:
   :widths: 1 5
   :header-rows: 1

   * - Date
     - Change description
   * - TODO
     - The first release

.. todo:: publishing date

In the previous post :ref:`monitoring-prometheus`, we created one playbook
which contained all the logic. This post will show how to do a refactoring of
a playbook into smaller, reusable ansible roles, which hide complexity and
provide defined interfaces.

----

.. FIXME: This is a undesirable way to use the asciinema files. I had to
   create the "_static/asciinema" directory by hand and also copy the
   asciinema source "vagrant-up.json" into that directory. This will be an
   issue when I move this post into the appropriate release directory,
   as I navigate in the directories here. Also, I have to use raw HTML,
   which is also not the best solution.
   An ideal solution would have a sphinx asciinema directive which handles
   the CSS/JS copying into the _static directory and also creates the proper
   HTML and deals with the source file itself, like this:
   .. asciinema:: vagrant-up.json
      :cols: 80
      :rows: 24

We start with this layout of our project:

.. code-block:: bash
   :linenos:
   :emphasize-lines: 0

    [markus@local]$ tree
    .
    |-- ansible.cfg
    |-- eat_cpu.py
    |-- eat_disk.py
    |-- eat_memory.py
    |-- grafana.ini
    |-- hosts.ini
    |-- infra-node-metrics.json
    |-- playbook.yml
    |-- prometheus.yml
    `-- Vagrantfile

    0 directories, 11 files


Start the virtual machines which will be our targets for the playbook later:

.. raw:: html

   <asciinema-player src="../../../_static/asciinema/asciinema_vagrant-up_c671UQ5.json" cols="120" rows="30"></asciinema-player>


Start the playbook (without any encapsulation in roles):

.. raw:: html

   <asciinema-player src="../../../_static/asciinema/asciinema_playbook_HHyJsRV.json" cols="120" rows="30"></asciinema-player>


When I start to refactor roles out of a playbook, I usually do
it by adding a new directory ``roles`` to the project. The *Ansible*
configuration file ``ansible.cfg`` [#ansconf]_ needs to be created and an
entry to the ``roles_path`` key needs to be added:

.. literalinclude:: ansible.cfg
   :language: ini
   :linenos:
   :emphasize-lines: 5

The other settings in this file make my life a little easier most of the
time, but they are not absolutely necessary.

.. note::
    Later steps can be, to put a role in a dedicated git repo only for that
    role and use it in your company only, or push it to *Ansible Galaxy*
    for reuse by others.


.. code-block:: bash
   :linenos:
   :emphasize-lines: 0

    [markus@local]$ ansible-galaxy init roles/node-exporter
    [markus@local]$ tree --dirsfirst
    .
    |-- roles
    |   `-- node-exporter
    |       |-- defaults
    |       |   `-- main.yml
    |       |-- handlers
    |       |   `-- main.yml
    |       |-- meta
    |       |   `-- main.yml
    |       |-- tasks
    |       |   `-- main.yml
    |       |-- tests
    |       |   |-- inventory
    |       |   `-- test.yml
    |       |-- vars
    |       |   `-- main.yml
    |       `-- README.md
    |-- ansible.cfg
    |-- eat_cpu.py
    |-- eat_disk.py
    |-- eat_memory.py
    |-- grafana.ini
    |-- hosts.ini
    |-- index.rst
    |-- infra-node-metrics.json
    |-- playbook.yml
    |-- prometheus.yml
    `-- Vagrantfile


The ``ansible-galaxy init`` command uses a template to create a directory for
the role and uses a naming convention for the sub-directories
and files.

.. note::

   Two directories are missing here, namely ``templates`` and ``files``.
   This is already reported [#ansidirbug]_ but not yet solved (at least
   in my version 2.3.1, installed via *pypi*).

The responsibilities of those directories of a role in short:

* ``tasks``:
  Contains the tasks which do the work like you already know from a
  normal playbook.

* ``handlers``:
  Contains handlers, which, when notified, trigger actions.

* ``defaults``
  Role specific variables, which have a default, but are intended
  to get overridden from the role user (a play in a playbook).

* ``vars``
  Role specific variables, which are **not** intended to get overridden.

* ``templates``
  With *jinja2* templated files. The ``template`` module [#templatemod]_
  searches in that directory by default.

* ``files``
  The default directory for the ``copy`` module [#copymod]_.

* ``meta``
  Meta information for this role. This is the place where you can
  define dependencies to other roles, for example.

* ``tests``
  Contains everything necessary to test this role in isolation.
  I haven't yet used this like I should. I'm going to explore this
  in another post later.

Move the node-exporter related tasks from the playbook into the file
``roles/node-exporter/tasks/main.yml``:

.. code-block:: yaml
   :linenos:
   :emphasize-lines: 0

    ---
    # tasks file for node-exporter

    - name: "Install Prometheus Node Exporter package."
      apt:
        name: prometheus-node-exporter

    - name: "Ensure the Node Exporter is started and starts at host boot."
      service:
        name: prometheus-node-exporter
        enabled: true
        state: started

    - name: "Check if the service emits metrics."
      uri:
        url: http://127.0.0.1:9100/metrics
        method: GET
        status_code: 200


Use the role in the playbook instead of the moved tasks. See this diff
to see the difference:

.. code-block:: diff
   :linenos:
   :emphasize-lines: 11-12

    --- a/playbook.yml
    +++ b/playbook.yml
    @@ -41,22 +41,9 @@
     - hosts: all  # we want the metrics of the monitoring server too
       become: true

    -  tasks:
    -    - name: "Install Prometheus Node Exporter package."
    -      apt:
    -        name: prometheus-node-exporter
    +  roles:
    +    - node-exporter

    -    - name: "Ensure the Node Exporter is started and starts at host boot."
    -      service:
    -        name: prometheus-node-exporter
    -        enabled: true
    -        state: started
    -
    -    - name: "Check if the service emits metrics."
    -      uri:
    -        url: http://127.0.0.1:9100/metrics
    -        method: GET
    -        status_code: 200


That's the basic recipe. Tasks, which build a logical unit of work,
get moved into a role. The difficulty is, to define what a *logical unit* is.
The difficulty will become more obvious in the next steps, when I create
more roles to encapsulate logic.

.. tip::

    Keep in mind that within a play, the
    **roles get executed before the tasks**,
    despite how you order it in the play.
    You can influence that with the ``include_role`` module [#includerole]_
    or the ``import_role`` module [#importrole]_,
    which let you tread roles like a task.

With this basic step, let's create another role, this time for the
*Prometheus* service:

.. code-block:: bash
   :linenos:
   :emphasize-lines: 0

    [markus@local]$ ansible-galaxy init roles/prometheus

Add the role to the playbook (see the highlighted lines below),
and move the tasks to ``roles/prometheus/tasks/main.yml`` and the
*Prometheus* related handler to ``roles/prometheus/handlers/main.yml``
and the ``prometheus.yml`` file into ``roles/prometheus/files/``.

.. code-block:: diff
   :linenos:
   :emphasize-lines: 7-8

    --- a/playbook.yml
    +++ b/playbook.yml
    @@ -52,31 +52,10 @@
     - hosts: monitoring
       become: true

    +  roles:
    +    - prometheus

       tasks:
    -    # --- Prometheus --------------------------------------------------------
    -    - name: "Install the Prometheus server."
    -      apt:
    -        name: prometheus
    -
    -    - name: "Configure the Prometheus server."
    -      copy:
    -        src: prometheus.yml
    -        dest: /etc/prometheus/prometheus.yml
    -      notify: event_restart_prometheus
    -
    -    - name: "Ensure Prometheus is started and starts at host boot."
    -      service:
    -        name: prometheus
    -        enabled: true
    -        state: started
    -
    -    - name: "Check if Prometheus is accessible."
    -      uri:
    -        url: http://127.0.0.1:9090/graph
    -        method: GET
    -        status_code: 200
    -
         # --- Grafana -----------------------------------------------------------
         - name: "Install the Grafana server."
           apt:
    @@ -139,12 +118,6 @@

       # --- After all tasks are executed (if notified) --------------------------
       handlers:
    -    - name: "Restart the Prometheus service."
    -      service:
    -        name: prometheus
    -        state: restarted
    -      listen: event_restart_prometheus
    -
         - name: "Restart the Grafana service."
           service:
             name: grafana


We do the very same to the tasks to install the *Grafana* service:


.. code-block:: bash
   :linenos:
   :emphasize-lines: 0

    [markus@local]$ ansible-galaxy init roles/grafana

Same procedure as before:

#. move the ``grafana.ini`` file into ``roles/grafana/files/``
#. move the *Grafana* related tasks to ``roles/grafana/tasks/main.yml``
#. move the *Grafana* related handler to ``roles/grafana/handlers/main.yml``
#. add the new ``grafana`` role to the playbook


.. code-block:: diff
   :linenos:
   :emphasize-lines: 7

    --- a/playbook.yml
    +++ b/playbook.yml
    @@ -54,31 +54,9 @@

       roles:
         - prometheus
    +    - grafana

       tasks:
    -    # --- Grafana -----------------------------------------------------------
    -    - name: "Install the Grafana server."
    -      apt:
    -        name: grafana
    -
    -    - name: "Copy Grafana configuration file."
    -      copy:
    -        src: grafana.ini
    -        dest: /etc/grafana/grafana.ini
    -      notify: event_restart_grafana
    -
    -    - name: "Ensure Grafana is started and starts at host boot."
    -      service:
    -        name: grafana
    -        enabled: true
    -        state: started
    -
    -    - name: "Check if Grafana is accessible."
    -      uri:
    -        url: http://127.0.0.1:3000
    -        method: GET
    -        status_code: 200
    -
         - name: "Add Prometheus as datasource to Grafana."
           vars:
             prometheus_datasource:
    @@ -116,15 +94,6 @@
               Accept: "application/json"


    -  # --- After all tasks are executed (if notified) --------------------------
    -  handlers:
    -    - name: "Restart the Grafana service."
    -      service:
    -        name: grafana
    -        state: restarted
    -      listen: event_restart_grafana
    -
    -
     # ===========================================================================
     # Push the "applications" to the application servers
     # ===========================================================================



At this point you might wonder why I didn't move the setup of the
*Grafana* datasource and dashboard into the ``grafana`` role too.
It would work, no doubt about that. My two reasons are:

* keep it small and simple
* dependency management

Adding *Prometheus* as a datasource to *Grafana*, creates a **dependency**
between those two. So far they were independent from each other. We could
rearrange the two roles we have so far, and could use the ``grafana`` role
before the ``prometheus`` role, it wouldn't matter as they are independent.
Establishing the dependency is its own logical unit in my opinion. To
encapsulate that, we create another role:

.. code-block:: bash
   :linenos:
   :emphasize-lines: 0

    $ ansible-galaxy init roles/grafana-prometheus-datasource

Now move the code, which establishes the datasource to
``roles/grafana-prometheus-datasource/tasks/main.yml`` and add the
new role to the playbook:

.. code-block:: diff
   :linenos:
   :emphasize-lines: 7

    --- a/playbook.yml
    +++ b/playbook.yml
    @@ -55,30 +55,9 @@
       roles:
         - prometheus
         - grafana
    +    - grafana-prometheus-datasource

       tasks:
    -    - name: "Add Prometheus as datasource to Grafana."
    -      vars:
    -        prometheus_datasource:
    -          name: "prometheus"
    -          type: "prometheus"
    -          url: "http://127.0.0.1:9090"
    -          access: "proxy"
    -          isDefault: true
    -          basicAuth: false
    -      uri:
    -        url: http://127.0.0.1:3000/api/datasources
    -        method: POST
    -        body: "{{ prometheus_datasource | to_json }}"
    -        body_format: json
    -        user: admin
    -        password: admin
    -        force_basic_auth: yes
    -        status_code: 200,500  # 500 means, the datasource is already added
    -        headers:
    -          Content-Type: "application/json"
    -          Accept: "application/json"
    -
         - name: "Upload the example Grafana dashboard."
           uri:
             url: http://127.0.0.1:3000/api/dashboards/db


Next one is the dashboard of *Grafana*.

#. create a new role with ``ansible-galaxy``
#. move the files into that role
#. move the tasks into ``tasks/main.yml``
#. move the handlers into ``handlers/main.yml``
#. add the role to the playbook


.. code-block:: bash
   :linenos:
   :emphasize-lines: 0

    ansible-galaxy init roles/grafana-dashboard


.. code-block:: diff
   :linenos:
   :emphasize-lines: 7

    --- a/playbook.yml
    +++ b/playbook.yml
    @@ -56,21 +56,7 @@
         - prometheus
         - grafana
         - grafana-prometheus-datasource
    +    - grafana-dashboard
    -
    -  tasks:
    -    - name: "Upload the example Grafana dashboard."
    -      uri:
    -        url: http://127.0.0.1:3000/api/dashboards/db
    -        method: POST
    -        body: "{{ lookup('file', 'infra-node-metrics.json') }}"
    -        body_format: json
    -        user: admin
    -        password: admin
    -        force_basic_auth: yes
    -        status_code: 200
    -        headers:
    -          Content-Type: "application/json"
    -          Accept: "application/json"


Let's move the deployment of the applications into a role too:

.. code-block:: bash
   :linenos:
   :emphasize-lines: 0

   $ ansible-galaxy init roles/workload-deploy

Again, move the code and files, add the new role to the playbook:

.. code-block:: diff
   :linenos:
   :emphasize-lines: 7-8

    --- a/posts/drafts/ansible-playbook-roles/playbook.yml
    +++ b/posts/drafts/ansible-playbook-roles/playbook.yml
    @@ -66,12 +66,5 @@
       become: true
       gather_facts: false

    +  roles:
    +    - workload-deploy
    -  tasks:
    -     - name: "Copy the applications to the servers."
    -       copy:
    -         src: "{{ item }}"
    -         dest: "/root/{{ item }}"
    -       with_items:
    -         - eat_cpu.py
    -         - eat_disk.py
    -         - eat_memory.py

When you take a look at your playbook, you note that there is a nice
layer of abstraction. You'll also spot a violation: The update of the
APT repository cache.

.. code-block:: yaml
   :linenos:
   :emphasize-lines: 0

    - name: "Ensure system package cache is updated."
      apt:
        update_cache: "yes"
        cache_valid_time: 3600

This task is only necessary because we install *Node-Exporter*, *Grafana*
and *Prometheus* from the *APT* repository of *Ubuntu*. We have two
choices here:

* copy this tasks into the roles which need it
* create a new role which does only this task and let others depend on it

While I prefer the first solution, let's do the second one for the sake
of example of creating dependencies between roles.

.. code-block:: bash
   :linenos:
   :emphasize-lines: 0

   $ ansible-galaxy init roles/apt-update

Move the task into ``roles/apt-update/tasks/main.yml``.

.. code-block:: diff
   :linenos:
   :emphasize-lines: 0

   --- a/posts/drafts/ansible-playbook-roles/playbook.yml
   +++ b/posts/drafts/ansible-playbook-roles/playbook.yml
   @@ -29,10 +29,6 @@
          ping:
          with_items: '{{ groups["all"] }}'

   -    - name: "Ensure system package cache is updated."
   -      apt:
   -        update_cache: "yes"
   -        cache_valid_time: 3600

Establish the dependency in:

#. ``roles/grafana/meta/main.yml``
#. ``roles/prometheus/meta/main.yml``
#. ``roles/node-exporter/meta/main.yml``

like this:

.. code-block:: yaml
   :linenos:
   :emphasize-lines: 0

   dependencies:
     - apt-update

Later, when I show you the recording of the playbook execution, you'll
notice that the APT update occurs right before the roles which depend
on it.


-----------------------


General advice
==============

* the complete URL must not be longer than 78 chars
* the initial release date is in the URL
* post directory is part of the URL (make it searchable, don't be fancy)
* aim for less than 15h per post, otherwise the releases will become unstable
* the spelling check is done frequently and at the very end
* add the release date only if confident enough
* start with a brain dump, refine from there
* consider touch screens (mobile phones). CSS hover text magic doesn't work



Structure
=========

#. title
#. abstract
#. table of contents
#. change history table
#. TL;DR (if applicable)
#. use case
#. content
#. summary / conclusion
#. references
#. appendix

This is only the first level. Add another level if necessary. Let 2 levels
be the maximum.

Each section is a permalink and therefore a published resource. That means,
don't change once published permalinks (aka altering sections).


.. code-block:: rst
   :linenos:
   :emphasize-lines: 0

   =====
   title
   =====

   section
   =======

   sub-section
   ===========

   **paragraph header**



Table of contents
=================

Every post has a table of contents. The sections link back to the
table of contents. This makes jumps back and forth easy.

.. code-block:: rst
   :linenos:
   :emphasize-lines: 0

    .. contents::
        :local:
        :backlinks: top



Categories and labels
=====================

There are 3 categories:

* books
* conferences
* openstack

Categories are more coarse grained than labels. Having no category is fine,
it's then seen as being miscellaneous until a category evolves over time.

Add labels as you see fit. Check the existing ones. Use one to three labels.

.. code-block:: rst
   :linenos:
   :emphasize-lines: 0

    .. post:: 25 Aug, 2017
       :category: openstack
       :tags: nova, scheduling, cpu-architecture
       :title: OpenStack Nova Scheduling based on CPU architecture


Code examples
=============

* blocks always with line numbers
* emphasize lines to set focus
* use the proper highlighting language [#pygments]_

Text
----

The config option ``key2`` has value ``value2``.

.. code-block:: rst
   :linenos:
   :emphasize-lines: 0

   The config option ``key2`` has value ``value2``.


Blocks
------

.. code-block:: python
   :linenos:
   :emphasize-lines: 0

   print("hello blog")

.. code-block:: rst
   :linenos:
   :emphasize-lines: 0

   .. code-block:: python
      :linenos:
      :emphasize-lines: 0

      print("hello blog")

Files
-----

.. code-block:: rst
   :linenos:
   :emphasize-lines: 0

    .. literalinclude:: example.ini
       :language: ini
       :linenos:
       :emphasize-lines: 5



Text format
===========

Use **strongly emphasized** to make a point.

.. code-block:: rst
   :linenos:
   :emphasize-lines: 0

   Use **strongly emphasized** to make a point.


----

Use *proper names* for people companies and software.
For example, *Kubernetes*.

.. code-block:: rst
   :linenos:
   :emphasize-lines: 0

   Use *proper names* for people companies and software.
   For example, *Kubernetes*.

----

Use an `inline quote` for inline referencing an external source
(like books) or small direct quotes of cited sources.

.. code-block:: rst
   :linenos:
   :emphasize-lines: 0

   Use an `inline quote` for inline referencing an external source
   (like books) or small direct quotes of cited sources.


----

    Use a block quote for multi line
    direct quotes of cited resources.

.. code-block:: rst
   :linenos:
   :emphasize-lines: 0

       Use a block quote for multi line
       direct quotes of cited resources.



Images
======

Favor vector graphics (``.svg``) over raster maps (``.png``).
Always do a scaling of the images (``:height:`` or ``:width:`` or ``:scale:``),
this enables the "click on the thumbnail to show the full image" logic.


.. code-block:: rst
  :linenos:
  :emphasize-lines: 0

  .. image:: drawing_TOelDqK.svg
     :height: 150px
     :alt: Example drawing with Inkscape.

.. important::

   All images of all posts will be copied to ``_images``. This means
   unique image names are needed to avoid collisions. Use the script
   to generate unique (enough) identifiers.



Spelling
========

Use the spelling directive if it is only needed for one post:

.. code-block:: rst
   :linenos:
   :emphasize-lines: 0

   .. spelling::

      foo

In either case, take care of upper and lower case, singular and plural.



References and links
====================

External
--------

"External" is everything outside of this blog.
Reference to it with auto-numbered footnotes [#footnotes]_


.. code-block:: rst
   :linenos:
   :emphasize-lines: 0

   Reference to it with auto-numbered footnotes [#footnotes]_

Internal
--------

"Internal" is everything inside of this blog.
For example the :ref:`about` page.

.. code-block:: rst
   :linenos:
   :emphasize-lines: 0

   For example the :ref:`about` page.



Lists
=====

Numbered lists for ordered items:

#. first do this,
#. then you can do that,
#. lastly you do another thing.

.. code-block:: rst
   :linenos:
   :emphasize-lines: 0

   Numbered lists for ordered items:

   #. first do this,
   #. then you can do that,
   #. lastly you do another thing.


----

Bullet lists for (unordered) items:

* a hat
* a walking stick
* an umbrella

.. code-block:: rst
   :linenos:
   :emphasize-lines: 0

   Bullet lists for (unordered) items:

   * a hat
   * a walking stick
   * an umbrella



Highlighted info boxes
======================

.. todo::

    Reminder for the author to do this here before publishing.

.. code-block:: rst
   :linenos:
   :emphasize-lines: 0

   .. todo::

       Reminder for the author to do this here before publishing.

----

.. admonition:: Feedback needed

    Use this for actively asking for feedback from the reader.

.. code-block:: rst
   :linenos:
   :emphasize-lines: 0

   .. admonition:: Feedback needed

       Use this for actively asking for feedback from the reader.


----

.. note::

    This is a "mild" highlight. No biggie if the reader misses it.

.. code-block:: rst
   :linenos:
   :emphasize-lines: 0

   .. note::

       This is a "mild" highlight. No biggie if the reader misses it.



----

.. tip::

    This gives advice to the reader.

.. code-block:: rst
   :linenos:
   :emphasize-lines: 0

   .. tip::

       This gives advice to the reader.


----


.. warning::

    Don't do this. This is a common mistake.


.. code-block:: rst
   :linenos:
   :emphasize-lines: 0

   .. warning::

       Don't do this. This is a common mistake.


----

.. important::

    Do this (really) / Be aware of this (really).


.. code-block:: rst
   :linenos:
   :emphasize-lines: 0

   .. important::

       Do this (really) / Be aware of this (really).


Change history
==============

The publish date is the very first entry. Append another entry below the
previous one when:

* the structure got changed
* a paragraph got added or removed
* content got altered which changed the meaning of something

In general, think twice before changing a published post. If a big change
would be necessary, maybe a follow up post is the better choice. If so,
cross-reference each other.

**No addition** needed when:

* typo fix
* small format change (bold, italics, ...)

.. code-block:: rst
   :linenos:
   :emphasize-lines: 7-8

    .. list-table:: Change history:
       :widths: 1 5
       :header-rows: 1

       * - Date
         - Change description
       * - 2017-11-02
         - The first release



References
==========

.. [#pygments] http://pygments.org/

.. [#footnotes] http://www.sphinx-doc.org/en/stable/rest.html#footnotes

.. [#ansconf] http://docs.ansible.com/ansible/latest/intro_configuration.html

.. [#ansidirbug] https://github.com/ansible/ansible/issues/23597

.. [#includerole] http://docs.ansible.com/ansible/latest/include_role_module.html

.. [#importrole] http://docs.ansible.com/ansible/latest/import_role_module.html

.. [#templatemod] http://docs.ansible.com/ansible/latest/template_module.html

.. [#copymod] http://docs.ansible.com/ansible/latest/copy_module.html