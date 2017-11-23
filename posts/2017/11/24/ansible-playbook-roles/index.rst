
.. post::
   :tags: ansible, iac
   :title: Ansible Playbook Refactoring into Roles

.. spelling::
   foo



=======================================
Ansible Playbook Refactoring into Roles
=======================================

In a previous post (:ref:`monitoring-prometheus`), we created one playbook
which contained all the logic. This post will show how to do a refactoring of
a playbook into smaller, reusable *Ansible Roles*. This allows us to hide
complexity and to provide defined interfaces. It also increases the
ability to work in parallel on different parts of your
*Infrastructure as Code (IaC)* project. I won't explore how you publish
your roles to *Ansible Galaxy* but merely show a basic recipe how you
move *Playbook* logic step by step into project specific roles.

.. contents::
    :local:
    :backlinks: top

.. todo:: date of the change history

.. list-table:: Change history:
   :widths: 1 5
   :header-rows: 1

   * - Date
     - Change description
   * - 2017-11-24
     - The first release


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

Starting point
==============

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

   <asciinema-player src="../../../../../_static/asciinema/asciinema_vagrant-up_c671UQ5.json" cols="120" rows="30" poster="npt:0:09"></asciinema-player>


Start the playbook (without any encapsulation in roles):

.. raw:: html

   <asciinema-player src="../../../../../_static/asciinema/asciinema_playbook_HHyJsRV.json" cols="120" rows="30" poster="npt:0:12"></asciinema-player>


Enable *Ansible* to use local roles
===================================

When I start to refactor roles out of a playbook, I usually do
it by adding a new directory ``roles`` to the project. The *Ansible*
configuration file ``ansible.cfg`` [#ansconf]_ needs to be created and an
entry to the ``roles_path`` key needs to be added:

.. literalinclude:: ansible.cfg
   :language: ini
   :linenos:
   :emphasize-lines: 5

The highlighted line tells *Ansible* to look for roles in the relative
directory ``roles`` and the absolute directory ``/etc/ansible/roles``,
which is the default directory when you use roles from others.

The other settings in this file make my life a little easier most of the
time, but they are not absolutely necessary.

.. note::

   Later steps can be, to put a role in a dedicated git repo only for that
   role and use it in your company only, or push it to *Ansible Galaxy*
   for reuse by others.


The basic recipe
================

When doing an *as-is* extraction of the logical units (like we do in
this post), follow these steps:

#. create a new role with ``ansible-galaxy init roles/<role-name>``
#. add the role to the ``playbook.yml``
#. move the tasks into ``roles/<role-name>/tasks/main.yml``
#. move the handlers into ``roles/<role-name>/handlers/main.yml``
#. move the static files used by those tasks and handlers
   into ``roles/<role-name>/files/``
#. move the template files used by those tasks and handlers into
   ``roles/<role-name>/templates/``
#. run the playbook to verify we didn't introduce an error

Let's use this basic recipe with the logic of installing the
*Node Exporter*.

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
   |-- infra-node-metrics.json
   |-- playbook.yml
   |-- prometheus.yml
   `-- Vagrantfile


The ``ansible-galaxy init`` command uses a template to create a directory for
the role and uses a naming convention for the sub-directories
and files.

.. note::

   Two directories are missing here, namely ``templates`` and ``files``.
   This is an already reported bug [#ansidirbug]_ but it's not solved yet
   (at least in my version 2.3.1, installed via *pypi*).

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

.. hint::

   You can delete the directories and files you don't need for that role.
   *Ansible* can handle that. I usually keep them to have some kind of
   uniformity among the roles and the superfluous directories don't
   bother me.

The ``README.md`` is also worth taking a look at an filling in the missing
documentation pieces. I'm omitting it in this post.

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


Use the role in the playbook instead of the moved tasks. See this *diff*
to see the difference:

.. code-block:: diff
   :linenos:
   :emphasize-lines: 0

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



Extract more logical units
==========================

For the sake of example, I'll go excessive here and refactor every logic
in that *playbook* into their own *roles*, following the basic refactoring
recipe explained before. You'll see the recurring pattern pretty quickly.



Extract a ``prometheus`` role
-----------------------------

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
   :emphasize-lines: 0

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



Extract a ``grafana`` role
--------------------------

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
   :emphasize-lines: 0

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



Extract a ``grafana-prometheus-datasource`` role
------------------------------------------------

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

   [markus@local]$ ansible-galaxy init roles/grafana-prometheus-datasource

Now move the code, which establishes the datasource to
``roles/grafana-prometheus-datasource/tasks/main.yml`` and add the
new role to the playbook:

.. code-block:: diff
   :linenos:
   :emphasize-lines: 0

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



Extract a ``grafana-dashboard`` role
------------------------------------

Next one is the dashboard upload into *Grafana*.

.. code-block:: bash
   :linenos:
   :emphasize-lines: 0

   [markus@local]$ ansible-galaxy init roles/grafana-dashboard


.. code-block:: diff
   :linenos:
   :emphasize-lines: 0

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


Extract a ``workload-deploy`` role
----------------------------------

Let's move the deployment of the applications into a role too:

.. code-block:: bash
   :linenos:
   :emphasize-lines: 0

   [markus@local]$ ansible-galaxy init roles/workload-deploy

Again, move the code and files, add the new role to the playbook:

.. code-block:: diff
   :linenos:
   :emphasize-lines: 0

   --- a/playbook.yml
   +++ b/playbook.yml
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



Extract an ``apt-update`` role
------------------------------

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

   [markus@local]$ ansible-galaxy init roles/apt-update

Move the task into ``roles/apt-update/tasks/main.yml``.

.. code-block:: diff
   :linenos:
   :emphasize-lines: 0

   --- a/playbook.yml
   +++ b/playbook.yml
   @@ -29,10 +29,6 @@
          ping:
          with_items: '{{ groups["all"] }}'

   -    - name: "Ensure system package cache is updated."
   -      apt:
   -        update_cache: "yes"
   -        cache_valid_time: 3600

**Define a role dependency**

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



Extract a ``ssh-accessible`` role
---------------------------------

Let's go excessive and refactor the rest of the tasks into roles.

.. code-block:: bash
   :linenos:
   :emphasize-lines: 0

   [markus@local]$ ansible-galaxy init roles/ssh-accessible

Move the SSH task into the role and add the role to the playbook:

.. code-block:: diff
   :linenos:
   :emphasize-lines: 0

   --- a/playbook.yml
   +++ b/playbook.yml
   @@ -7,17 +7,10 @@
      become: true
      gather_facts: false

   -  tasks:
   -    - name: "Wait for SSH to be ready."
   -      become: false
   -      delegate_to: localhost
   -      wait_for:
   -        port: 22
   -        host: '{{ ansible_host }}'
   -        search_regex: "OpenSSH"
   -        delay: 5
   -        timeout: 300
   +  roles:
   +    - ssh-accessible

   +  tasks:
        - name: "Add our servers to the hosts file."
          lineinfile:
            dest: /etc/hosts



Extract an ``ip-name-mapping`` role
-----------------------------------

Extract the IP address to name mapping too:

.. code-block:: bash
   :linenos:
   :emphasize-lines: 0

   [markus@local]$ ansible-galaxy init roles/name-ip-mapping


.. code-block:: diff
   :linenos:
   :emphasize-lines: 0

   --- a/playbook.yml
   +++ b/playbook.yml
   @@ -9,19 +9,7 @@

      roles:
        - ssh-accessible
   +    - name-ip-mapping
   -
   -  tasks:
   -    - name: "Add our servers to the hosts file."
   -      lineinfile:
   -        dest: /etc/hosts
   -        # use the IP address we specified in the Vagrantfile
   -        line: '{{ hostvars[item].ansible_host }} {{item}}'
   -      with_items: '{{ groups["all"] }}'
   -
   -    - name: "Ping each other via DNS names."
   -      ping:
   -      with_items: '{{ groups["all"] }}'
   -



The result of the as-is extraction
==================================

Nothing more to extract out of the playbook. We have this result:

.. literalinclude:: playbook_roles.yml
   :language: yaml
   :linenos:
   :emphasize-lines: 0

The layer of abstraction becomes obvious. Someone, who hasn't written
this playbook can grasp in a few moments what's happening (but not *how*
it is happening).

Our project structure looks like this:

.. code-block:: bash
   :linenos:
   :emphasize-lines: 0

   [markus@local]$ tree --dirsfirst
   .
   |-- roles
   |   |-- apt-update
   |       |-- [...]
   |   |-- grafana
   |       |-- [...]
   |   |-- grafana-dashboard
   |       |-- [...]
   |   |-- grafana-prometheus-datasource
   |       |-- [...]
   |   |-- name-ip-mapping
   |       |-- [...]
   |   |-- node-exporter
   |       |-- [...]
   |   |-- prometheus
   |       |-- [...]
   |   |-- ssh-accessible
   |       |-- [...]
   |   `-- workload-deploy
   |       |-- [...]
   |-- ansible.cfg
   |-- hosts.ini
   |-- playbook.yml
   `-- Vagrantfile

   68 directories, 83 files

I trimmed it down a little. You see that this is much cleaner than
our starting point. The files are in the directories of the appropriate
roles.

Let's take a look at the *playbook* execution with roles:

.. raw:: html

   <asciinema-player src="../../../../../_static/asciinema/asciinema_playbook_roles_etwQtsN.json" cols="120" rows="30" poster="npt:0:10"></asciinema-player>

The name of the roles are now part of the displayed tasks (as prefixes),
which makes it easier to spot what's happening.


Define configuration interfaces
===============================

At this point, we did an as-is extraction and relied on the defaults
we used. There was no way to configure roles from a users point of view.
We'll take a look at role variables from two aspects:

* to get used in a conditional
* to be a placeholder for actual value



Role variable in a conditional
------------------------------

Let's look at a real-world example with the *Grafana* role. As explained
in a previous post (:ref:`monitoring-prometheus`), the *Ubuntu*
package for it got removed with *Ubuntu 17.10* and we need some kind
of transition strategy. We have different choices to do this:

* create a new *Grafana* role which installs from source
* extend the existing *Grafana* role to install from APT or source,
  depending on a configured variable

Honestly, both choices are valid in my opinion, each with advantages and
disadvantages. I've chosen the latter approach here to demo how a separation
of concerns could be done with *Ansible* role variables. To elaborate on
that, imagine you're the *Grafana* expert in your company and two different
groups want to use your role. One group uses *Ubuntu 16.04* until the long
term support expires, the other group upgrades every time to a new LTS
release, e.g. *Ubuntu 18.04* in April next year, which doesn't have
the OS package anymore. The users mostly don't care how the installation
happens, the just want to have the service available in their setup and
you're the person responsible to make that happen and deal with their
different setups.

Let's add a variable to the *Grafana* role, which has a default value,
but is supposed to get overridden if needed. The file
``roles/grafana/defaults/main.yml`` could look like this:


.. code-block:: yaml
   :linenos:
   :emphasize-lines: 0

   ---
   # defaults file for grafana

   install_method: os-package

``os-package`` is the default value for the variable ``install_method``.
Another valid value, to override the default one, could then be ``source``.
I've chosen those names arbitrarily, there is no naming convention.

.. tip::

   At this point you should strongly consider to fill out the section
   *"Role Variables"* in the *README* file of that role.


Before we make use of that new variable, move the contents of
``roles/grafana/tasks/main.yml`` into a newly created file
``roles/grafana/tasks/apt_install.yml``. Now we add this conditional
to the empty ``roles/grafana/tasks/main.yml``:

.. code-block:: yaml
   :linenos:
   :emphasize-lines: 0

   ---
   # tasks file for grafana

   - name: "Install from operating system package."
     include: apt_install.yml
     when: install_method == "os-package"

   - name: "Install from source."
     include: source_install.yml
     when: install_method == "source"

The important part here is, that we are **backwards compatible**.
The default value ``os-package`` enables the conditional to hit
which includes and executes the old logic to install from APT.

The new code path in ``roles/grafana/tasks/source_install.yml`` is
rather unspectacular:

.. code-block:: yaml
   :linenos:
   :emphasize-lines: 0

   ---

   - name: "Install from source."
     fail:
       msg: "TODO not yet done!"

I haven't yet found time to develop the logic to install *Grafana*
from source, so I let the task simply fail.

In the playbook, we used the role like this:

.. code-block:: yaml
   :linenos:
   :emphasize-lines: 6

   - hosts: monitoring
     become: true

     roles:
       - prometheus
       - grafana

Executed, you'll see this in the output:

.. code-block:: bash
   :linenos:
   :emphasize-lines: 3

   TASK [grafana : Install from source.] ************************
   Thursday 23 November 2017  11:46:55 +0100 (0:00:00.227)
   skipping: [monitoring]

Notice that we skipped the task to install from source, as our
conditional worked.

Now let's configure the role by overwriting the role's variable:

.. code-block:: yaml
   :linenos:
   :emphasize-lines: 6

   - hosts: monitoring
     become: true

     roles:
       - prometheus
       - { role: grafana, install_method: source }

Let's execute the playbook again:

.. code-block:: bash
   :linenos:
   :emphasize-lines: 3

   TASK [grafana : Install from source.] ************************
   Thursday 23 November 2017  11:50:33 +0100 (0:00:00.014)
   fatal: [monitoring]: FAILED! => {"changed": false, "failed": true, "msg": "TODO not yet done!"}

The conditional has matched and the task failed like expected.



Role variable as placeholder
----------------------------

The most common usage for role variables is in providing the actual
values to use, because they cannot be known upfront. In our example,
we assumed that *Prometheus* and *Grafana* run on the same host.
That's why using ``127.0.0.1`` as IP address for the datasource was
working. To make your roles more flexible, you can promote that
to a role variable and make it configurable. That way you could deploy
*Prometheus* and *Grafana* on different hosts. As we decided to put
the logic which creates the dependency between them in a separate role,
we have to edit the file
``roles/grafana-prometheus-datasource/defaults/main.yml``:

.. code-block:: yaml
   :linenos:
   :emphasize-lines: 0

   ---
   # defaults file for roles/grafana-prometheus-datasource

   prometheus_datasource_url: "http://127.0.0.1:9090"

Now we can make use of that in our existing logic in the task of that
role:

.. code-block:: diff
   :linenos:
   :emphasize-lines: 0

   --- a/roles/grafana-prometheus-datasource/tasks/main.yml
   +++ b/roles/grafana-prometheus-datasource/tasks/main.yml
   @@ -6,7 +6,7 @@
        prometheus_datasource:
          name: "prometheus"
          type: "prometheus"
   -      url: "http://127.0.0.1:9090"
   +      url: "{{ prometheus_datasource_url }}"
          access: "proxy"
          isDefault: true
          basicAuth: false

This role variable can be set like in the example before. For the sake
of example, here another way you can set the role variable, which is
more readable when you have more variables to set:

.. code-block:: yaml
   :linenos:
   :emphasize-lines: 2-3

   - hosts: monitoring
     vars:
       prometheus_datasource_url: "http://192.168.101.10:9090"

     roles:
       - grafana-prometheus-datasource


.. hint::

   There are even more ways to do it, but it's fine to start this way
   and to explore other ways and variable precedence later [#ansvars]_.



Conclusion
==========

This post showed a basic recipe how you can refactor your *Ansible*
playbooks by extracting logical units of work into *Ansible roles*.
Roles are reusable, configurable and encapsulated units of work.
The readability of playbooks get increased, like we saw after
the refactoring of our previously long playbook.
Roles can also be shared with others in your company (or on
*Ansible Galaxy*), which avoids that the same work gets done twice.

I think of roles as the *Ansible* equivalent to classes of object
oriented programming languages, e.g. *Python*. Sure, you can hack down
everything in one long *Python* script, but at some point you're life
gets a lot easier when you start moving logical units into classes
and use their public interfaces. Just like we did with *Ansible roles* here.

There are even more hard-coded values in our project. Download the
:download:`project source files <ansible-playbook-roles.tar.gz>`
and try yourself on it.



References
==========

.. [#ansconf] http://docs.ansible.com/ansible/latest/intro_configuration.html

.. [#ansidirbug] https://github.com/ansible/ansible/issues/23597

.. [#templatemod] http://docs.ansible.com/ansible/latest/template_module.html

.. [#copymod] http://docs.ansible.com/ansible/latest/copy_module.html

.. [#includerole] http://docs.ansible.com/ansible/latest/include_role_module.html

.. [#importrole] http://docs.ansible.com/ansible/latest/import_role_module.html

.. [#ansvars] http://docs.ansible.com/ansible/latest/playbooks_variables.html
