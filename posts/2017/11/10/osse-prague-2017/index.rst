
.. post:: 10 Nov, 2017
   :category: conferences
   :title: The 2017 Open Source Summit Europe in Praque



================================================
The 2017 *Open Source Summit Europe* in *Praque*
================================================



This post is my recap of the *Open Source Summit Europe* conference which
took place in *Praque (Czech Republic)* from October 23-26, 2017. I'll go
briefly through the sessions I attended and the notes I took.



.. contents::
    :local:
    :backlinks: top



.. list-table:: Change history:
   :widths: 1 5
   :header-rows: 1

   * - Date
     - Change description
   * - 2017-11-10
     - The first release



Context
=======

The *Open Source Summit Europe* describes itself as:

    LinuxCon, ContainerCon, CloudOpen and the new Open Community
    Conference combine under one umbrella name in 2017 - the Open
    Source Summit. At the Open Source Summit, you will collaborate,
    share information and learn across a wide variety of topics,
    with 2,000 technologists and community members.

It is one of the many events of the *Linux Foundation* [#lfe]_
and the main page for the conference itself can be found at [#osself]_.
The full schedule for the event I attended is at [#ossesched]_ and the
videos to the keynotes can be found at [#osseyt]_.

.. image:: osse_2017_inspiration_everywhere_Vrh34Wh.JPG
   :height: 250px



Sessions
========

At any given time I had two to four conflicting sessions in my bookmarks,
so I had to decide which ones to go to. Here's the chronological list
of sessions I attended. The session, reachable via the *sched* links,
often have their presentations attached.

If you're short on time, only read:

* :ref:`sec_observability`
* :ref:`sec_not_source`
* :ref:`sec_devops_effort`

These were my top 3 session of this conference.



Going Modular: Turning Legacy Docs into User-Story-Based Content
----------------------------------------------------------------

*Robert Kratky (Red Hat)*: http://sched.co/ByIP

The usual measure of success for writing documentation is **comprehensiveness**.
Everything needs to be documented. With shorter delivery cycles of the software
to document, it got harder to achieve that level of comprehensiveness. It is
also hard to read a monolithic document of dozens to **hundreds of pages**.

So they started to use a modular approach, based on the question, how to
achieve a **specific goal**. He made a comparison to *StackOverflow*, which
basically does exactly that. It's **not comprehensive**, but focuses on
specific content and user stories to document. They created a documentation
assembly based on action oriented, modular templates, which allowed them to
deliver the **most important documentation** in each delivery cycle.



Code Detective: How to Investigate Linux Performance Issues
-----------------------------------------------------------

*Gabriel Krisman (Collabora)*: http://sched.co/BxIA

*Gabriel* mentioned *Amdahl's law* [#amdahl]_ and that you should not do
**premature** optimization without knowing what parts of your code base
is **hot code**. He recommends knowing the ``perf`` profiling tool and
metrics like ``cache-misses`` and ``branch-misses``. It's probably also
a good idea to stick to common algorithms and avoid being fancy, as the
compiler most likely optimizes better than you. At [#colla]_, they show
more tips and tricks.



Collaboration in Kernel Mailing Lists
-------------------------------------

*Dawn Foster (The Scale Factory)*: http://sched.co/BxIH

This was a presentation of *Dawn's* research for her PhD. Key findings where,
that **task affiliation** is far greater than *company affiliation*. Also,
that the **timezone pain** gets mitigated by the asynchronous nature of mailing
lists. Lastly, **professional relationships** get stronger with face to face
meetings like conferences.

She chose a very interesting type of data visualization for (strength of)
collaboration. I don't know the name of that diagram type; it's basically
a dependency graph arranged in a cycle. Check out her slides at the link
above.



.. _sec_gqm:

Applying Goals-Question-Metrics to Software Development Management
------------------------------------------------------------------

*Jose Manrique Lopez de la Fuente (Bitergia)*: http://sched.co/ByIM

I wasn't aware of the term **inner source** [#inner]_, until *Jose* mentioned
it in his talk. To move in that direction he discussed the use of
*goal, question, metric* **(GQM)** [#gqm]_ and the *DevOps* framework **CALMS**:

* Culture
* Automation
* Lean
* Measurement
* Sharing

He mentioned that the *Community Health Analytics Open Source Software*
**(CHAOSS)** can help you to navigate through the complex and very important
non-code part of software development.



From *Dockerfiles* to *Ansible Container*
-----------------------------------------

*Tomas Tomecek (Red Hat)*: http://sched.co/BxIW

*Tomas* showed examples of non-trivial **hard-to-read Dockerfiles** and
the problems he faced with parsing and linting them due to the missing
spec of the **file format**. He worried about the **varying degrees** of
quality, freshness and maintenance of the images at *DockerHub*.

His idea was to use **ansible-container** to make things more
readable, flexible and reusable, until the **Moby buildkit** could lift
some (or all) of the mentioned limitations of *Dockerfiles*.



*EulerOS Isula*: Born For Cloud, Drive Cloud Native
---------------------------------------------------

*Wei Xiong (Huawei)*: http://sched.co/Cflp

*Huawei* promotes a **cloud-pipe-device ecosystem** [#cpd]_. All the different
parts which play a role until a service can be consumed, run on *Linux*.
But the OS **package dependencies** get harder to maintain, especially across
those very different parts:

* cloud (*Huawei*'s public cloud *Atlas*),
* pipe (IIUC, the networking elements),
* devices (on the end-consumer side)

Instead of having one generic multi purpose *Linux* instance, they create
multiple **single purpose** *Linux* instances, based on a common ancestor
**EulerOS** [#euler]_. It's the divide and conquer strategy for problems,
which means they build assembly lines with smaller parts with the goal to
have better control.

It was also interesting to hear that they target to have ~90% of the workload
happening in containers within the next 2 years. Securing containers happens
with *KVM*.



.. _sec_kub_tools:

Developer Tools for *Kubernetes*
--------------------------------

*Michelle Noorali & Matt Butcher (Microsoft)*: http://sched.co/CexK

*Michelle* and *Matt* started with a rough categorization of applications,
based on their **lifespan** (short vs. long) and state
(**stateless** vs. stateful). Stateless, short living (mostly **event driven**)
applications are a good match for **serverless** technology, whereas web
applications are your typical long running, **stateful** applications.

To package your application ready for **kubernetes**, you can use **helm**.
With **draft** you can automate the *helm* packaging and reduce the cognitive
load, as it hides some of the complexity. Your event driven pipeline can
be simplified with **brigade**. They also mentioned a tool called **pack**,
but I didn't find more information with a short google search, so maybe
I misheard.


.. _sec_iac:

Pipeline as Code For Your Infrastructure as Code
------------------------------------------------

*Kris Buytaert (Inuits.eu)*: http://sched.co/BxIo

*Kris* also mentioned *CLAMS*, like *Jose* did in :ref:`sec_gqm`.
He pointed out that it is very important to **version your automation code**
and that you **should not click around in the UI** to set something up.
An interesting measure of success was:

  Deploy your Infrastructure as Code (*IaC*) on a Friday afternoon
  at 5pm and go home confidently.

He suggested to use the **monitoring** you set up as the **acceptance tests**
for your *IaC* efforts. For all that, a **Continuous Integration (CI)** system
is the basis, as it is the prerequisite for **Continuous Delivery**, which is
the prerequisite for **Continuous Deployment**.
Apparently, **pipelineDSL**  and **Jenkins Job DSL** are popular ways
to implement your pipelines.
At the end, he warned from a *"pipeline sprawl"*, a state where you have so
many pipelines that it becomes unmanageable.



*Serverless* - Is It For Your Organization?
-------------------------------------------

*Michael Bright (HPE)*: http://sched.co/BxIz

As already mentioned in :ref:`sec_kub_tools`, **serverless** is useful
for short lived applications, like periodic tasks or event driven logic.
It's also useful for **glue logic** between different systems. The main
philosophy behind *serverless* seems to be, that you don't care about servers
anymore and use **Backend as a Service (BaaS)**, which is mostly based
on re-used (recycled) containers nowadays. Another advantage might be
the **billing as you go** on a very granular level. It's still a young
technology (**~3 years old**), I'm curious how this technology will evolve
in the next years.



.. _sec_observability:

360 Degree Observability
------------------------

*Ilan Rabinovitch (Datadog)*: http://sched.co/ByIc

*Ilan's* talk was my personal highlight of this conference. Like in
:ref:`sec_iac`, he suggested a **monitoring driven development**.
As the **things to monitor** he listed:

* *Application Performance Monitoring* (**APM**)
* *Real User Monitoring* (**RUM**)
* **Synthetics** (simulate user interactions)

In his experience RUM and synthetics work best together. The monitoring
can be extended with an algorithmic approach of **anomaly detection**
and **forecasting**.

He reminded the audience, that **the problem is not the right tool**
it's the **unknown unknowns** [#unknown]_ you don't know you should measure.

As a side note, check out the *Twitter* *honest status page* [#honest]_,
it's hilarious (because it's true).



Using Containers and Continuous Packaging to Build Native *Fossology* Packages
------------------------------------------------------------------------------

*Bruno Cornec (HPE) and Michael Jaeger (Siemens)*: http://sched.co/BxJC

*Bruno* and *Michael* work on the **Fossology** project, a tool and database
to scan software for all the **licensing details** you need to specify when
building and offering a package.
Their advice was to **package early, package always**. You should also be
able to create a package without committing the code first.
The way they do it, is to have one **templated spec file** with macros, where
the configuration is done on the outside of this file.
They do the build continuously inside of containers with different
operating system versions, as there are
**differences between minor versions of distributions** which have a
significant impact on the package build process. Something I wasn't aware of.



IBM LinuxONE: The Largest Scalable Linux Server
-----------------------------------------------

*Jens Voelker & John Smith (IBM)*: http://sched.co/Cgor

**Disclaimer:** I work in this area at *IBM*.

*Jens* and *John* presented the **LinuxOne**, an **IBM Z Mainframe**
especially for *Linux* server hosting. Mainly used by governments and
banks because of the **security** aspects, it's use case also includes
**license consolidation**. Its design fits perfectly for **huge databases**
as it can **avoid sharding**, which otherwise would result in performance
penalties.

The traditional use cases got extended in the past by making it ready for
the **(private) cloud** [#icp]_ and container based applications. For example,
**Docker Enterprise** integrated LinuxONE into its CI pipeline and is fully
supported on **IBM Z** since this month. Your **microservice meshes**
also benefit from the high bandwidth inside the machine, which results in
low latency. For even more data protection, use the
**Secure Service Containers (SSC)**.

Academics and researcher can do their first steps with the
**Open Mainframe Project** [#openz]_.



No One Puts the JVM in a Container
----------------------------------

*Joerg Schad & Johannes Unterstein (Mesosphere)*: http://sched.co/BxIl

The gist of this talk was, be very aware of what you pack into a container
and what actually happens inside the container and on the host. An example
was given with a *Java* application. Apparently, before *Java8*, the
**JRE is not aware of cgroups** and uses host resources. And the hard limit on
memory controlled by *cgroups* means, that the docker process gets killed
when it reaches a state of over-consumption. With *Java8* and later, you
can use the **flags** ``UseCGroupMemoryLimitForHeap`` and
``UnlockExperimentalVMOptions``. With this, all the *namespace* and *cgroup*
mapping on the real resources get considered.


.. _sec_devops_effort:

*Docker*, *Moby* is Killing Your `#devops` Efforts
--------------------------------------------------

*Kris Buytaert (Inuits.eu)*: http://sched.co/BxJd

It was an opinionated talk (which is good, that's why I go to conferences)
and *Kris* is obviously very passionate about **DevOps**. His main points
were, that Enterprises are afraid of (public) clouds and are in favor of
**"caged" private clouds**, where you emulate non-caged private clouds with huge
VMs (previously requested with an internal ticketing system) and run *Docker*
in it.

The actual problem, that **developers and operators don't talk to each other**
didn't get tackled, as a *Docker* container is treated now like a fancy tarball,
which gets thrown over the wall with *"works on my machine, I'm done"*.
To be precise, he didn't complain about **Docker** as a technology,
he was more worried about **how we use** this technology.



Workshop: Continuous Integration with the Open Build Service
------------------------------------------------------------

*Eduardo Navarro & Björn Geuken (SUSE Linux GmbH)*: http://sched.co/ByRq

The **open build service (OBS)** [#obs]_ can build **OS packages** for different
package managers and CPU architectures and distributions. It is based on
*kiwi* [#kiwi]_, an OS image builder. A *github* webhook integration is
available, so it should be possible to create a
**continuous integration with continuous delivery**
approach with it. A private installation of OBS is also possible.

To be honest, I didn't fully attend this workshop, as it conflicted with
another session I wanted to see, so I missed probably some information.
It sounded very promising though.



Everything You Always Wanted to Know About Object Storage
---------------------------------------------------------

*Erit Wasserman (Red Hat)*: http://sched.co/CnWI

The fun fact first, *Erit* let us know that *Ceph* got its name from
*Cephalopods* [#ceph]_ (squids, octopuses and suchlike). The high-level
differences between the common ways to store data are:

* **block storage** has no metadata but is fast
* **file system** has hierarchy and metadata and in-place writes
* **object storage** has flat namespace; objects are **immutable**

As the objects are immutable, each version of an object is a new object,
which means you need a **retention policy** to deal with the needed disk space.

Apparently, **Ceph** offers block, file and object storage and uses
**rados** as the underlying distributed object storage, while
**radosgw** lifts some limits of *rados* (I didn't get the details which
limits). As the single objects can be big, you need a way to be resilient
against network issues, so it divides single large objects into smaller ones
and does a **multipart upload**.



.. _sec_not_source:

Open Source is Just About the Source, Isn't It?
-----------------------------------------------

*Isabel Drost-Fromm (Europace AG)*: http://sched.co/ByIo

*Isabel* talked about everything development related but the code, which is
great, as *"the messy problems are people problems"* and I have to agree.
The source code is only a small part of the project and the **community** is at
least as important as the code. She made excellent points about the
**different ways of communication**, trademarking, licensing, change management,
FAQs, work delegation and much more. Finding ways for newbies to replicate
correct behavior is important too. A lot to think about when you start
your next open source project.



Transactional Updates with *btrfs* and RPMs
-------------------------------------------

*Thorsten Kukuk (SUSE)*: http://sched.co/BxK2

*Thorsten* did a proof of concept with *btrfs*, a copy on write general
purpose filesystem to enable **transactional operating system updates** without
reboots. He uses the **btrfs subvolumes** (not to be confused with LVM volumes)
and their **snapshot** capability to achieve this. Unfortunately I didn't get
all the details, but having to never reboot again after an update sounds
like operators would love it.



Tutorial: Container Orchestration with *Kubernetes*
---------------------------------------------------

*Michael Steinfurth (B1 Systems GmbH)*: http://sched.co/ByRs

This session showed how **kubernetes** uses *etcd* for saving data.
You can run *etcd* on *kubernetes* itself or as dedicated servers
and you need at least **3 etcd nodes** to have a **quorum**.
The *etcd* clients have to advertise themselves to the peers.
*Michael* used **flanneld** for networking overlay and stored the
network configuration in *etcd* and the whole **etcd cluster** is then
aware of this new value. For all that, you can use **kubectl**,
a configuration tool and cluster CLI.



Event Recap
===========

It was a very good event; the quality of the sessions ans speakers was
excellent. Everything was well organized. The evening event on Wednesday
took place in the *Municipal House*, a gorgeous building (see image below).
I'm looking forward to the next event, October 22 - 24, 2018 in Edinburgh,
Scotland.

.. image:: municipal_house_praque_SXY5xEK.JPG
   :height: 250px



References
==========

.. [#lfe] http://events.linuxfoundation.org/

.. [#osself] http://events.linuxfoundation.org/events/open-source-summit-europe

.. [#ossesched] https://osseu17.sched.com/

.. [#osseyt] https://www.youtube.com/playlist?list=PLbzoR-pLrL6pISWAq-1cXP4_UZAyRtesk

.. [#amdahl] https://en.wikipedia.org/wiki/Amdahl%27s_law

.. [#colla] https://www.collabora.com/news-and-blog.html?blogs

.. [#inner] https://en.wikipedia.org/wiki/Inner_source

.. [#gqm] https://en.wikipedia.org/wiki/GQM

.. [#cpd] http://www1.huawei.com/en/static/HW-104296.pdf

.. [#euler] http://developer.huawei.com/ict/en/site-euleros/euleros-introduction

.. [#unknown] https://en.wikipedia.org/wiki/There_are_known_knowns

.. [#honest] https://twitter.com/honest_update

.. [#icp] https://www.ibm.com/cloud-computing/products/ibm-cloud-private/

.. [#openz] https://www.openmainframeproject.org/

.. [#obs] http://openbuildservice.org/

.. [#kiwi] https://github.com/openSUSE/kiwi

.. [#ceph] https://en.wikipedia.org/wiki/Cephalopod
