
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


Let's move the deployment of the applications into a role too:

.. code-block:: bash
   :linenos:
   :emphasize-lines: 0

   $ ansible-galaxy init roles/workload-deploy

Again, move the code and files, add the new role to the playbook:

.. code-block:: diff
   :linenos:
   :emphasize-lines: 0

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

Let's go excessive and refactor the rest of the tasks into roles.

.. code-block:: bash
   :linenos:
   :emphasize-lines: 0

   $ ansible-galaxy init roles/ssh-accessible

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


To go to an extreme, extract the IP address to name mapping too:

.. code-block:: bash
   :linenos:
   :emphasize-lines: 0

   $ ansible-galaxy init roles/name-ip-mapping


.. code-block:: diff
   :linenos:
   :emphasize-lines: 0

   --- a/posts/drafts/ansible-playbook-roles/playbook.yml
   +++ b/posts/drafts/ansible-playbook-roles/playbook.yml
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


Nothing more to extract out of the playbook. We have this end result:

.. literalinclude:: playbook.yml
   :language: yaml
   :linenos:
   :emphasize-lines: 0

Our project structure looks like this:

.. code-block:: bash
   :linenos:
   :emphasize-lines: 0

   [markus@local]$ tree --dirsfirst
   .
   |-- roles
   |   |-- apt-update
   |   |   |-- defaults
   |   |   |   `-- main.yml
   |   |   |-- handlers
   |   |   |   `-- main.yml
   |   |   |-- meta
   |   |   |   `-- main.yml
   |   |   |-- tasks
   |   |   |   `-- main.yml
   |   |   |-- tests
   |   |   |   |-- inventory
   |   |   |   `-- test.yml
   |   |   |-- vars
   |   |   |   `-- main.yml
   |   |   `-- README.md
   |   |-- grafana
   |   |   |-- defaults
   |   |   |   `-- main.yml
   |   |   |-- files
   |   |   |   `-- grafana.ini
   |   |   |-- handlers
   |   |   |   `-- main.yml
   |   |   |-- meta
   |   |   |   `-- main.yml
   |   |   |-- tasks
   |   |   |   `-- main.yml
   |   |   |-- tests
   |   |   |   |-- inventory
   |   |   |   `-- test.yml
   |   |   |-- vars
   |   |   |   `-- main.yml
   |   |   `-- README.md
   |   |-- grafana-dashboard
   |   |   |-- defaults
   |   |   |   `-- main.yml
   |   |   |-- files
   |   |   |   `-- infra-node-metrics.json
   |   |   |-- handlers
   |   |   |   `-- main.yml
   |   |   |-- meta
   |   |   |   `-- main.yml
   |   |   |-- tasks
   |   |   |   `-- main.yml
   |   |   |-- tests
   |   |   |   |-- inventory
   |   |   |   `-- test.yml
   |   |   |-- vars
   |   |   |   `-- main.yml
   |   |   `-- README.md
   |   |-- grafana-prometheus-datasource
   |   |   |-- defaults
   |   |   |   `-- main.yml
   |   |   |-- handlers
   |   |   |   `-- main.yml
   |   |   |-- meta
   |   |   |   `-- main.yml
   |   |   |-- tasks
   |   |   |   `-- main.yml
   |   |   |-- tests
   |   |   |   |-- inventory
   |   |   |   `-- test.yml
   |   |   |-- vars
   |   |   |   `-- main.yml
   |   |   `-- README.md
   |   |-- name-ip-mapping
   |   |   |-- defaults
   |   |   |   `-- main.yml
   |   |   |-- handlers
   |   |   |   `-- main.yml
   |   |   |-- meta
   |   |   |   `-- main.yml
   |   |   |-- tasks
   |   |   |   `-- main.yml
   |   |   |-- tests
   |   |   |   |-- inventory
   |   |   |   `-- test.yml
   |   |   |-- vars
   |   |   |   `-- main.yml
   |   |   `-- README.md
   |   |-- node-exporter
   |   |   |-- defaults
   |   |   |   `-- main.yml
   |   |   |-- handlers
   |   |   |   `-- main.yml
   |   |   |-- meta
   |   |   |   `-- main.yml
   |   |   |-- tasks
   |   |   |   `-- main.yml
   |   |   |-- tests
   |   |   |   |-- inventory
   |   |   |   `-- test.yml
   |   |   |-- vars
   |   |   |   `-- main.yml
   |   |   `-- README.md
   |   |-- prometheus
   |   |   |-- defaults
   |   |   |   `-- main.yml
   |   |   |-- files
   |   |   |   `-- prometheus.yml
   |   |   |-- handlers
   |   |   |   `-- main.yml
   |   |   |-- meta
   |   |   |   `-- main.yml
   |   |   |-- tasks
   |   |   |   `-- main.yml
   |   |   |-- tests
   |   |   |   |-- inventory
   |   |   |   `-- test.yml
   |   |   |-- vars
   |   |   |   `-- main.yml
   |   |   `-- README.md
   |   |-- ssh-accessible
   |   |   |-- defaults
   |   |   |   `-- main.yml
   |   |   |-- handlers
   |   |   |   `-- main.yml
   |   |   |-- meta
   |   |   |   `-- main.yml
   |   |   |-- tasks
   |   |   |   `-- main.yml
   |   |   |-- tests
   |   |   |   |-- inventory
   |   |   |   `-- test.yml
   |   |   |-- vars
   |   |   |   `-- main.yml
   |   |   `-- README.md
   |   `-- workload-deploy
   |       |-- defaults
   |       |   `-- main.yml
   |       |-- files
   |       |   |-- eat_cpu.py
   |       |   |-- eat_disk.py
   |       |   `-- eat_memory.py
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
   |-- hosts.ini
   |-- playbook.yml
   `-- Vagrantfile

   68 directories, 83 files

Let's take a look at the *playbook* execution with roles:

.. raw:: html

   <asciinema-player src="../../../_static/asciinema/asciinema_playbook_roles_etwQtsN.json" cols="120" rows="30"></asciinema-player>

The name of the roles are now part of the displayed tasks (as prefixes),
which makes it easier to spot what's happening.


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
