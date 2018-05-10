
.. post:: May 11, 2018
   :category: conferences
   :title: The 2018 KubeCon and CloudNativeCon in Copenhagen, Denmark

.. spelling::
   Serverless
   sandboxed
   mortems
   Mixins
   Kubernetes
   podcast



==========================================================
The 2018 KubeCon and CloudNativeCon in Copenhagen, Denmark
==========================================================

This post is my recap of the *KubeCon and CloudNativeCon* conference which
took place in *Copenhagen (Denmark)* from May 1-4, 2018. I'll go
briefly through the sessions I attended and the notes I took.



.. contents::
    :local:
    :backlinks: top

.. list-table:: Change history:
   :widths: 1 5
   :header-rows: 1

   * - Date
     - Change description
   * - 2018-05-11
     - The first release


.. image:: IMG_20180502_084341340.jpg
   :width: 95%
   :alt: The room for the keynotes.


All sessions can be found here:
https://kccnceu18.sched.com/mobile/#page:page-schedule

All 300+ recordings of the whole event can be found in this playlist:
https://www.youtube.com/watch?v=OUYTNywPk-s&list=PLj6h78yzYM2N8GdbjmhVU65KYm_68qBmo

Be aware that the 35 minute session limit takes its toll. They speak really fast
sometimes.

If you want to sound smart in the next weeks and months, use these keywords:

* *serverless* / *FaaS*
* service mesh with *istio*
* chaos engineering
* security with *gVisor*



Top 3
=====

If you're low on time, watch only these three videos, which were my highlights
of the event:

* `Crossing the River by Feeling the Stones`:

  https://www.youtube.com/watch?v=xlNYYy8pzB4

* `Anatomy of a Production Kubernetes Outage`:

  https://www.youtube.com/watch?v=OUYTNywPk-s

* `Multi-Tenancy in Kubernetes: Best Practices Today, and Future Directions`:

  https://www.youtube.com/watch?v=xygE8DbwJ7c



----

**Tuesday**

Lightning talks
===============

On Tuesday evening, there were some *lighting talks*. In case you don't know what that
means, it's a series of different topics, each typically presented within 5 minutes.
Apparently I'm not into that kind of format, although the topics were interesting.
If you do such a format in the future, please don't try to squash 20 min of content
into the session by talking extra fast. I didn't note down anything in the 90 minutes,
but it was a nice start for the next three days.



----

**Wednesday**


Day 1 Keynotes
==============

https://www.youtube.com/watch?v=C1kwY0N4PUk

I've had bad experiences with keynotes at other conferences in the past. They tended
to be either boring or some executives didn't have a clue what they are talking about.
I gave it another try this time, and it was a much better experience than in the past.
The sessions were quite **good and entertaining** with some interesting announcements
(see the other *keynotes* blocks later on in this post). The most interesting thing
at this morning where the presentation of the **maturity model of the CNCF projects**
https://www.cncf.io/projects/ which sorts projects either in **Sandbox** or
**Incubating** or **Graduated** depending on different criteria. Interesting new
projects are:

* *NATS* for messaging https://nats.io/
* *SPIFFE* / *SPIRE* for identity management https://spiffe.io/

Let's go through the sessions after the keynotes one by one.



Whats Up With All The Different Container Runtimes?
===================================================

https://www.youtube.com/watch?v=lHv0LVEIPk8

There is *containerd*, *rkt*, *cri-o*, *LXC*, *kata* and others.
I was still a little clueless after this session, to be honest.
The criteria chosen in the presentation didn't really struck with me.
If there are no strong reasons (and experiments to prove theories), I guess
it's safe to keep on going with *Docker* as a runtime.

My main takeaway from this session is, that the different competing runtimes
are encouraged to fulfill a common behavior, the **Container Runtime Interface (CRI)**
https://github.com/opencontainers/runtime-spec/blob/master/spec.md
specified by the the **Open Container Initiave (OCI)**. This enables portability and
**avoids vendor lock-in**.



Evolving Systems Design: From Unreliable RPC to Resilience with *Linkerd*
=========================================================================

https://www.youtube.com/watch?v=2EqkvPqk7JU

This is one of the many talks about a **service mesh**, this time with
*Linkerd*. The speaker shared his experiences of replacing a messaging
queue with a service mesh, built with *Linkerd*. A few features made
*Linkerd* very interesting:

* possibility of A/B testing
* built-in bulk head pattern
* automated retries on fails

I think those things are possible with common message queues too, but
apparently he was quite happy with the results and it solved the problems
he faced well enough.

I'll probably take a closer look at *Linkerd* in a separate post.



Open Source and Building Online Communities using Social Media and Communications
=================================================================================

https://www.youtube.com/watch?v=V0qaU512zrg

Communication is key. I don't know many people who doubt that.
How to have good and efficient communications, that's the hard question.
The speaker shared some insights and most of it boils down to
**know your audience**. As a way to deal with all the different platforms,
using *Twitter* for engagement with the audience and other social media
channels for sharing expertise where suggested.




Continuously Deliver your *Kubernetes* Infrastructure
=====================================================

https://www.youtube.com/watch?v=1xHmCrd8Qn8

A few of the more interesting practices the speaker shared were:

* **no pet clusters** (the variance is too much maintenance effort)
* do operations by *Github* pull request (so called **gitops**)
  https://www.weave.works/blog/gitops-operations-by-pull-request
* there is no maintenance window. For example, security fixes need to be
  applicable at every point in time.
* run *etcd* outside of the *Kubernetes* master nodes

The folks from *Zalando* open sourced their *Cluster Lifecycle Manager (CLM)*
at https://github.com/zalando-incubator/cluster-lifecycle-manager and think
it's worth having a look.

They use *Ginkgo* as **Behavior Driven Development (BDD)** testing framework
https://onsi.github.io/ginkgo/ to ensure no regressions slipped through
with an upgrade.

There was much more than what I noted down. It was an excellent session which
condensed the 2 years long operations knowledge down into 35 minutes.



Building a Cloud Native Culture in an Enterprise
================================================

https://www.youtube.com/watch?v=Tm4VfJtOHt8

I have not expected to see people from *The New York Times* (or any other
traditional print medium) at a cloud conference. It was surprising to hear
that they also don't see themselves as a print company anymore, but simply
a news company, which makes sense, as the consumption habits change fast.
In one of the keynotes, it was mentioned that more than half their users
were getting their news online, so it's not surprising to hear that they
need to manage their online content.

One of the challenges was the transition from a print company to a content
delivery company. To aid in the transition, they made good experiences
with having office hours and **support channels** in slack. I think that can be
a general pattern for dealing with **cultural change**.

To enable the internal teams, they see themselves in a **delivery engineering**
way and mentioned this blog post:
http://gregdmd.com/blog/2015/07/19/delivery-engineering-team/

Lastly, they weren't the only one which continuously mentioned the importance
of having well defined **Service Level Objectives (SLO)** which can be
measured and improved over time.




Serverless WG BOF
=================

The *Serverless* working group consists of all major cloud providers and
one of the first goals is the harmonization of an **event format**. Otherwise
the interoperability suffers and the hook-in cost is too high. The spec can
be found at https://github.com/cloudevents/spec/blob/master/spec.md


The latest **whitepaper** of the group can be found at
https://github.com/cncf/wg-serverless/tree/master/whitepaper
It also contains a link to the current *Serverless* **landscape** at
https://docs.google.com/spreadsheets/d/10rSQ8rMhYDgf_ib3n6kfzwEuoE88qr0amUPRxKbwVCk/
which is an interesting overview.

An aspect of *Serverless* could be to serve as an enabler for a **ChatOps** model.



Evening keynotes
================

There were also some keynotes at the evening, and the highlight of it was the
**post mortem** of an outage the *Monzo* bank had some time ago. The previous link
brings you to the video, I can highly recommend it. It's great to listen to the
experiences others made, and especially the things which went wrong. I wish we
would all be more open with the things which aren't traditional success stories.
That story also showed, that **chaos engineering** as a discipline is a necessity.
Kudos to *Monzo* for being open here!

Google announced two things here:

* *gVisor* for sandboxed containers: https://github.com/google/gvisor
* *stackdriver* for observability: https://cloud.google.com/stackdriver/

They also mentioned their podcast I wasn't aware of:
https://www.gcppodcast.com/categories/kubernetes/

Last but not least, Prometheus in version 2 is out and fast as hell,
thanks to the new implementation of the underlying time series database.




----

**Thursday**



Day 2 Keynotes
==============

The keynotes this morning also set more focus on **security** which was a
major theme throughout the conference. Naturally, **gVisor** got mentioned
again. Also, **Prometheus** is everywhere and it was not the first (or the
last time) **istio** was mentioned https://istio.io/.

The **operator framwork** got mentioned here and in later sessions.
In short, it's a way to write code for all the tasks a human application
operator would do, including the necessary operations knowledge.
I've probably need to invest some time in the future to think this
through: https://coreos.com/blog/introducing-operator-framework.



Managing *Kubernetes*: What You Need to Know About Day 2
========================================================

https://www.youtube.com/watch?v=0TBelL8UBQU

The main takeaways from this excellent session were:

* **user experience** matters for adoption of change
* **cultural change** and technical change are equally necessary
* think simple

It was obvious throughout the session that the speaker had a lot of
experience when it comes to manage *Kubernetes*. Luckily, he wrote it
down and it will be published this summer:
https://www.safaribooksonline.com/library/view/managing-kubernetes/9781492033905/

Some specific tips were:

* define "high availability"
* **Mean Time to Recovery (MTTR)** is THE metric
* organization specific logic can be done with dynamic admission control:
  https://kubernetes.io/docs/admin/extensible-admission-controllers/
* a bootstrapping machine helps to commoditize deployments
* volumes are bound to availability zones, so think about that in failover
  scenarios



Stories from the Playbook
=========================

https://www.youtube.com/watch?v=N2JUGnwinbQ

The speakers work in the Google **Site Reliability Engineering (SRE)** team
and shared some best practices:

* playbooks improve the **Mean Time to Recovery (MTTR)**
* playbooks reduce the cognitive load
* have *probers* as part of observability https://github.com/google/cloudprober
* use resource limits on pods
* have an established escalation path
* use **coordinate -> communicate -> control** as an escalation protocol
* do blameless post mortems
* solve issues in four steps:

  #. symptom analysis
  #. apply mitigation
  #. find root cause
  #. apply fix

* a fast track for emergency rollouts might also prove useful

They also currently work on problem fingerprinting as a technique to identify
problems faster and automatized.

Another interesting read is the SRE book at
https://landing.google.com/sre/book/chapters/introduction.html

And lastly a hint to the *Google Kubernetes Engine (GKE)* and its new
beta offering of private clusters:
https://cloud.google.com/kubernetes-engine/docs/how-to/private-clusters



Challenges to Writing Cloud Native Applications
===============================================

https://www.youtube.com/watch?v=di6oFceM_CQ

The key takeaways were:

* Persistent data in cloud native environments is a hard problem.
* Having multiple data stores with data replication between them is hard to do
  but useful.
* Service coupling and latency have impact on scheduling because of resources.
* Design for isolated testability even for end-to-end tests of your service.
* Include the operators in the architecture decision process as many issues
  are platform specific.

Among others, the speaker recommended the book *Designing Distributed Systems*
https://www.oreilly.com/library/view/designing-distributed-systems/9781491983638/
So much to read, so little time...



Kubernetes Multi-Cluster Operations without Federation
======================================================

https://www.youtube.com/watch?v=zVOIk7nO_ts

As an example, that probably every organization has at least 3 clusters, the
common setup of having a development cluster, a test/staging cluster and a
production cluster was shown. In the speakers experience, having 5-10 clusters
is the average. How do you deal with operations which span multiple clusters?

The **Kubernetes Federation** concept in its current form is seen as not fit for
that at the moment:
https://kubernetes.io/docs/concepts/cluster-administration/federation/
One of the main problems is the necessary root access of the federation server,
which is a security problem.

A possible solution cloud be the **Cluster Registry** project at
https://github.com/kubernetes/cluster-registry and by creating a workflow with
custom *Kubernetes* resources
https://kubernetes.io/docs/concepts/api-extension/custom-resources/
which get managed by the operator pattern
https://coreos.com/blog/introducing-operators.html

According to the speaker, the user experience is best with *Kubernetes* tools,
that's why the extension points are preferred.



Building Event-Driven Pipelines with Brigade
============================================

https://www.youtube.com/watch?v=yhfc0FKdFc8

*Brigade* is a tool, running in *Kubernetes*, which allows to create workflows
based on **events**. I'm not sure how this differs from *Function as a Service (FaaS)*,
e.g. OpenFaaS https://github.com/openfaas/faas

The main use case is probably in the continuous integration / continuous delivery
area. The speaker created an example pipeline with a CLI tool **brigateterm**
during the session. In it's simplest form, it resembles the popular mobile app
IFTTT, but on steroids. Said that, writing **glue code** between legacy applications
with *Brigade* might be a useful area for that technology too. There should be
enough of that in your company :)



Observability and the Depths of Debugging Cloud-Native Applications using *Linkerd* and Conduit
===============================================================================================

https://www.youtube.com/watch?v=RC_9ywj0yz8

*Conduit* is another example of a **service mesh** tool. It uses the sidecar pattern
to serve as a proxy: https://docs.microsoft.com/en-us/azure/architecture/patterns/sidecar

Injecting the sidecar besides the application to debug, enables us to add
**debugging functionality** without altering the application itself. It's worth
noting that service mesh debugging is very different to monolith debugging.
As the proxies have now all the knowledge about the communication of your
distributed application, you can start querying them for various metrics
to pin down the problematic service. This session walked us through that process.



----

**Friday**

Day 3 Keynotes
==============

The third day of the keynotes was also very good. The folks from *Google* showed
how they could save energy my **machine learning**
https://www.youtube.com/watch?v=I6iMznIYwM8.
The *KubeFlow* project is the toolkit which enables that:
https://github.com/kubeflow/kubeflow.
Another example of machine learning was the keynote by folks from *booking.com*,
who use it to recognize pictures for assets they can use to promote locations.

Regarding **security**, the keynote from Liz demonstrated wonderfully the flaws of
using root inside a container https://www.youtube.com/watch?v=ltrV-Qmh3oY.
Apparently most *Dockerfiles* out there don't use the ``USER`` keyword.
I also learned about the ``$ capsh --print`` command. Very recommendable video.

As mentioned at the beginning of this post, the best talk for me was the one
named `Crossing the River by Feeling the Stones`. It's about **strategy** and
how to communicate it https://www.youtube.com/watch?v=xlNYYy8pzB4.
If your company or organization has a strategy which is similar to one of
the auto-generated ones at https://strategy-madlibs.herokuapp.com you
should have a lot of fun with that talk. It was also the first time I heard
about the evolution:

#. from genesis
#. to custom build
#. to service / product
#. to utility / commodity

I have read this post more in detail
https://blog.gardeviance.org/2015/09/how-commodity-is-something.html
and think more about this.



Kubernetes 101: DIY Workshop
============================

https://www.youtube.com/watch?v=mYsp_cGY2O0

As mentioned in another section here, the acceptance of change in your
organization is one non-technical problem you need to solve before sustainable
change actually happens. This session suggested doing a hands-on workshop
to increase that acceptance and pointed to *Kubernetes* learning material
at https://github.com/jpetazzo/container.training.

A few tips for your own workshop are:

* No need to be an expert to teach something
* Limit unnecessary options
* Hand out printed credentials
* Consider network timeouts, maybe do the actions from a controller node




What Does “Production Ready” Really Mean for a *Kubernetes* Cluster?
====================================================================

https://www.youtube.com/watch?v=EjSiZgGdRqk

TL;DR: There are many possible definitions, you should have one.

The speaker went through several aspects, be it *High Availability (HA)*,
single point of failure, safe application of changes, you name it.
The summary for me is, that being "production ready" isn't easy, and
even harder if the stakeholders have no common understanding what it means
or costs. To get a feeling if your *Kubernetes* goes out of sync with
what is commonly accepted, the conformance test suite is helpful:
https://github.com/cncf/k8s-conformance.




Prometheus Monitoring Mixins: Using *Jsonnet* to Package Together Dashboards, Alerts and Exporters
==================================================================================================

https://www.youtube.com/watch?v=b7-DtFfsL6E

*Jsonnet* is a domain specific language (DSL) concerned with JSON configuration.
Prometheus Dashboards, for example, are just big JSON objects. This is awesome if
you want to store them in your *Github* project or want to share it with others.
The downside of JSON is, that you cannot have variables or control structures or
anything which can increase maintainability. *Jsonnet* allows you to more easily
**share your JSON configuration** by providing configuration entry points as
variables. It can do more that that, have a look at the examples at https://jsonnet.org/.
*Jsonnet* is the base for **Ksonnet**, a DSL for *Kubernetes* resources
https://ksonnet.io/. This configurability allows the creators of a service
to also offer a **best practice template** with specific configuration
extension points.



Kubernetes Runs Anywhere, but Does your Data?
=============================================

https://www.youtube.com/watch?v=Ot66g1WzXEU

The most important thing here is the **Container Storage Interface (CSI)**
which helps to abstract the storage back-end and allow data migration
https://kubernetes.io/blog/2018/01/introducing-container-storage-interface/.
Because, if your data cannot migrate, the migration of your application might
be impaired. If you rely on a specific storage back-end, you might be in a
vendor lock-in. The concept described in the link before reminds me of the
driver concept in the *OpenStack Cinder* project.



OpenStack SIG Deep Dive
=======================

https://www.youtube.com/watch?v=l03heU_uG1s

With my history of OpenStack, I was wondering what the according special interest
group was working on. The project can be found at
https://github.com/kubernetes/cloud-provider-openstack
and like others SIGs, the enablement of a common set of standards for external
cloud providers is one of the goals. The cloud controller manager is still in
alpha state at the time of this post:
https://kubernetes.io/docs/tasks/administer-cluster/running-cloud-controller/




Multi-Tenancy in *Kubernetes*: Best Practices Today, and Future Directions
==========================================================================

https://www.youtube.com/watch?v=xygE8DbwJ7c

The session was fully packed with content and I think the speaker could
talk about that topic much longer and in-depth than the 35 minute limit
allowed him to.

The first and important thing is, that you need to **define multi-tenancy**
when you talk about it. For example, *Kubernetes* doesn't care about
application internal multi-tenancy. The other cases could be:

* one tenant per cluster
* one tenant per *Kubernetes* namespace
* tenant specific nodes

Especially the multi-tenancy per namespace, which can be seen as semi-trusted
within a company, could be enough. **Role Based Access Control (RBAC)** can
already do a lot here.

As pods can talk to each other too, the network policy is a fine grained
mechanism which could help your problem.

The scheduler related features also can help you to isolate workload
from each other, for example **tains and tolerations**
https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/
as well as **affinity and anti-affinity**
https://kubernetes.io/docs/concepts/configuration/assign-pod-node/.

A work in progress are **security profiles**, but I didn't find a spec for it.



Event Recap
===========

It was a great conference with fantastic content and speakers. The room sizes were
perfect. I always found a seat and didn't have to fall back to another session.
The conference center also had a reasonable size, so that the 10 minute window to
get to the next session was enough time. The lunch, coffee and snacks were plenty.
Everything was well organized. The only thing to complain about was the lack of
power supplies.

The whole event, and the way the people speak about *Kubernetes*, reminded me of
my first OpenStack experiences 3 years ago, where the project was at its peak of
the hype cycle. Don't get me wrong, *Kubernetes* (and *OpenStack* for that matter)
is a great project which solves a specific problem space very well,
but I'm convinced that the hype cycle is inevitable, and it might me reasonable to
remind ourselves that *Kubernetes* is just another tool in the toolbox where you
need to know how and when to apply it, and when another tool might be more appropriate.



.. image:: IMG_20180504_082231239.jpg
   :width: 95%
   :alt: The sponsors room.

