
.. post::
   :tags: conferences
   :title: The 2017 Open Source Summit Europe in Praque

.. spelling::
   todo



================================================
The 2017 *Open Source Summit Europe* in *Praque*
================================================




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

Intro
=====

The *Open Source Summit Europe* describes itself as:

    LinuxCon, ContainerCon, CloudOpen and the new Open Community
    Conference combine under one umbrella name in 2017 - the Open
    Source Summit. At the Open Source Summit, you will collaborate,
    share information and learn across a wide variety of topics,
    with 2,000 technologists and community members.

It's one of the many events of the *Linux Foundation*:
http://events.linuxfoundation.org/

The main page for the conference itself is at:
http://events.linuxfoundation.org/events/open-source-summit-europe

The full schedule for the event I attended is at:
https://osseu17.sched.com/



Sessions
========

At any given time I had two to four conflicting sessions in my bookmarks,
so I had to decide which ones to go to. Here's the chronological list
of sessions I attended.




Going Modular: Turning Legacy Docs into User-Story-Based Content
----------------------------------------------------------------

*Robert Kratky, Red Hat*

http://sched.co/ByIP

issue:

* (legacy) measure of success: comprehensiveness
* hard to read and write

why:

* less monolithic; smaller now
* delivery cycles

user story

* measure of success: user achieves specific goals
* very selective content

assembly

* templates
* action oriented
* modular


Code Detective: How to Investigate Linux Performance Issues
-----------------------------------------------------------

*Gabriel Krisman, Collabora*

http://sched.co/BxIA

* *Amdahl's law*
* hot code
* **premature** optimization
* ``perf`` profiling
* CPU cache gets destroyed / fetching from memory is expensive ``cache-misses``
* "branch prediction" ``branch-misses``
* compiler optimizes better than you
* learn performance/profiling tools
* use common algorithms / avoid being fancy
* col.la/blog shows code snippets



Collaboration in Kernel Mailing Lists
-------------------------------------

*Dawn Foster, The Scale Factory*

http://sched.co/BxIH

* task affiliation > company affiliation
* timezone pain gets mitigated
* professional relationships get stronger with f2f conferences
* interesting visualization of (strength of) collaboration



Applying Goals-Question-Metrics to Software Development Management
------------------------------------------------------------------

*Jose Manrique Lopez de la Fuente, Bitergia*

http://sched.co/ByIM

* https://en.wikipedia.org/wiki/GQM
* inner source
* DevOps framework CALMS
* CHAOSS analytics software



From *Dockerfiles* to *Ansible Container*
-----------------------------------------

*Tomas Tomecek, Red Hat*

http://sched.co/BxIW

* *Dockerfiles* can get easily hard to read
* parsing/linting is hard due to missing spec of the file format
* quality/freshness/maintenance of images varies
* ansible-container makes things readable/flexible/reusable
* *Moby buildkit* could lift the limitations of *Dockerfile*



*EulerOS Isula*: Born For Cloud, Drive Cloud Native
---------------------------------------------------

*Wei Xiong, Huawei*

http://sched.co/Cflp

* unified platform for device, pipe, cloud (?)
* OS package dependencies get hard to maintain
* trend of moving away to generic Linux to single purpose Linux
* crate multiple single purpose Linux instances
* basically follows the divide and conquer strategy for problems
* build assembly lines with the smaller parts
* 30-50% are moving to container (target: ~90% in 2y)
* *Huawei*'s public cloud *Atlas*
* secured container based on KVM
* https://github.com/euleros/isula



Developer Tools for *Kubernetes*
--------------------------------

*Michelle Noorali & Matt Butcher, Microsoft*

http://sched.co/CexK

* distinguish applications based on their lifespan (*serverless* vs. web app)
* event-driven typically short-lived
* stateful vs. stateless
* *helm* packages stuff for *kubernetes*
* *draft* automates the *helm* stuff
* *draft* hides complexity of *kubernetes*
* *cognitive load* as a complexity unit?
* *pack* does ???
* *brigage* is event-driven pipeline action stuff for k8s



Pipeline as Code For Your Infrastructure as Code
------------------------------------------------

*Kris Buytaert, Inuits.eu*

http://sched.co/BxIo

* CLAMS: Culture, Lean, Automation, Measurement, Sharing
* CI prerequisite of "continues delivery" prerequisite of "continues deployment"
* measure of success: deploy FR at 5pm and go home and be confident
* version your automation code
* testing for *IaC* equals monitoring (== acceptance test)
* "pipeline sprawl" (same issue like "image sprawl")
* *pipelineDSL*  vs. *Jenkins Job DSL*
* don't click around in the UI!
* *IaC* as a means to do DR (in case the user data is saved)



*Serverless* - Is It For Your Organization?
-------------------------------------------

*Michael Bright, HPE*

http://sched.co/BxIz

* don't care about servers
* *backend as a service* (*BaaS*)
* billing as you go on a very granular level
* event driven
* useful for glue-logic / periodic tasks / short-lived
* mostly based on re-used / recycled containers
* ~3 years old







360 Degree Observability
------------------------

*Ilan Rabinovitch, Datadog*

http://sched.co/ByIc

* "monitoring driven development"
* "the problem is not the right tool"
* "unknown unknowns"
* application performance monitoring (APM)
* Real User Monitoring (RUM)
* synthetics (simulate user interactions)
* RUM + synthetics work best together
* Example: Amazon down march 2016 == 3.75M USD loss
* twitter: honest status updates
* anomaly detection (algorithmic approach)
* forecasting
* "work metric" (work -> resource -> events)




Using Containers and Continuous Packaging to Build Native *Fossology* Packages
------------------------------------------------------------------------------

*Bruno Cornec, Hewlett Packard Enterprise and Michael Jaeger, Siemens*

http://sched.co/BxJC

* *project-creator.org* creates packages for different distributions and package managers
* *fossology* scans for licenses
* "package early, package always"
* create a package without committing the code first
* one templated spec file with macros; configuration on the outside of this file
* there are differences with an impact even between minor versions of distributions





IBM LinuxONE: The Largest Scalable Linux Server
-----------------------------------------------

*Jens Voelker & John Smith, IBM*

http://sched.co/Cgor

* license consolidation is still a thing
* gov + banking ~= 50% of users
* 12 machines with ~ 6000 Oracle databases ~= biggest deployment
* *sCaaS* and IBM Private Cloud are already on the slides
* DockerEE integrated LinuxONE into its CI pipeline
* microservice meshes and latency; throughput benefits from internal IO
* the scale cube
* Nov. 2017: DockerEE fully supported on Z
* SSC == Secure System Container
* large databases: avoid *sharding* as it adds performance penalties
* "open mainframe" project






No One Puts the JVM in a Container
----------------------------------

*Joerg Schad & Johannes Unterstein, Mesosphere*

http://sched.co/BxIl

* DC/OS based on *apache mesos* (container orchestration)
* "feels" like a "lightweight VM"
* see all process (of the host) inside the container (?)
* namespaces are just views (mapping on the real things)
* control groups *cgroups* v1 vs. v2
* hard limit on memory + over-consumption kills the docker process
* JNI and NIO consume non-heap space
* before Java8, JRE is not aware of *cgroups* and uses host resources
* UseCGroupMemoryLimitForHeap and UnlockExperimentalVMOptions flags





*Docker*, *Moby* is Killing Your `#devops` Efforts
--------------------------------------------------

*Kris Buytaert, Inuits.eu*

http://sched.co/BxJd

* *Docker* -> *Moby*
* Enterprises are afraid of (public) cloud
* "caged" private clouds (request VMs)
* emulating non-caged private clouds with huge
  VMs and run docker in it
* docker container is the new fancy tarball
* "how do you build the hosts that run the containers?"
* "SW development ends when your last end user is dead"





Workshop: Continuous Integration with the Open Build Service
------------------------------------------------------------

*Eduardo Navarro & Björn Geuken, SUSE Linux GmbH*

http://sched.co/ByRq

* private installation of http://openbuildservice.org/ possible
* build packages for different package manager and architectures and distributions
* *github* webhook/integration available
* OBS is based on "kiwi"
* https://github.com/chrisbr/workshop-obs-ci
* *ppc64* is already there; *s390x* too?




Everything You Always Wanted to Know About Object Storage
---------------------------------------------------------

*Erit Wasserman, Red Hat*

http://sched.co/CnWI

* block storage has no metadata but is fast
* file system has hierarchy and metadata and in-place writes
* object storage has flat namespace; objects are immutable
* divide single large objects with *multipart upload*
* each version of an object is a new object => space usage
* *Ceph* == *Cephalopod*
* *ceph* offers block, file and object storage
* *rados* is the underlying distributed object storage
* *radosgw* lifts limits of *rados*








Open Source is Just About the Source, Isn't It?
-----------------------------------------------

*Isabel Drost-Fromm, Europace AG*

http://sched.co/ByIo

* the messy problems are people problems
* the source code is only a small part of the project
* community over code
* no one reads the FAQ, but you can copy the answers
* newbies need a way to replicate correct behavior
* think in "providing help to users"
* *disqus* with ML interface (?)
* explicit call to action brings out the lurkers
* real time help requests
* change management needs to be early in place
* delegating work is crucial





Transactional Updates with *btrfs* and RPMs
-------------------------------------------

*Thorsten Kukuk, SUSE*

http://sched.co/BxK2

* *btrfs* == copy on write general purpose filesystem
* *subvolumes* != LVM volumes
* snapshot capability





Tutorial: Container Orchestration with *Kubernetes*
---------------------------------------------------

*Michael Steinfurth, B1 Systems GmbH*

http://sched.co/ByRs

* *kubernetes* uses *etcd* for saving data
* *etcd* on *kubernetes* itself or as dedicated servers
* >= 3 *etcd* nodes to have a quorum (odd numbers)
* *etcd* clients have to advertise themselves to the peers
* *flanneld* for networking overlay
* network configuration (*flanneld*) saved in *etcd*
* *etcd* cluster is then aware of this new value
* never do a live coding session for people to repeat the steps live
* *kubectl* is a configuration tool and cluster CLI
* opinion: there are too many low-detail plumbing commands for the many
  moving parts. I miss one or two abstraction levels with more goal
  oriented (not task oriented) commands. opinionated stacks are fine!
  Look into one car factory and you know them all, why? because
  there are industry best practices; less freedom is fine sometimes.
  You're goal should be to deliver value to the user, not being
  fancy in the way you work. Boring is the new exciting.


Event Recap
===========

Very good event, I'm looking forward to the next one, October 22 - 24, 2018
in Edinburgh, Scotland.
