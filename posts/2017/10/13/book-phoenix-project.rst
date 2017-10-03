
.. post:: 13 Oct, 2017
   :category: books
   :title: Book Review: The Phoenix Project


.. spelling::
   phoenix project
   Spafford
   Behr


===================================
Recommendation: The Phoenix Project
===================================

This is my take on the book
`The Phoenix Project: A  Novel about IT, DevOps, and Helping Your Business Win`
from 2014 by Gene Kim; Kevin Behr; George Spafford. It's more of a personal 
reflection why I like the book -- and why I think you should read it too --
and less of a review.

The book follows the character *Bill Palmer* who's working for
*Parts Unlimited*, a fictional company producing and selling automotive parts.
The company is struggling, as it cannot keep up with their competitors.
The e-commerce project *Phoenix* is supposed to put a stop to the struggle
and bring the company back to the top. And Bill, our protagonist,
unexpectedly promoted from a mid-level operations manager to
*Vice President of IT Operations*, is now responsible for making it happen,
and (of course) things are falling apart.

.. contents::
   :local:
   :backlinks: top
   :depth: 1


.. list-table:: Change history:
   :widths: 1 5
   :header-rows: 1

   * - Date
     - Change description
   * - 2017-10-13
     - The first release



Overview
========

Type:
    Novel: story telling with a fictional company and characters.

Target group:
    Developers, operators, compliance folks, managers.

Focus:
    End-to-end view of software development, delivery and operations.

ISBN search:
    https://isbnsearch.org/isbn/0988262509

Preview:
    .. raw:: html

       <iframe type="text/html"
           width="336"
           height="550"
           frameborder="0"
           allowfullscreen style="max-width:100%"
           src="https://read.amazon.co.uk/kp/card?asin=B00AZRBLHO&preview=inline&linkCode=kpe&ref_=cm_sw_r_kb_dp_Rt7YzbFJXBVP6" >
       </iframe>



Why you should read it
======================

With *"you"*, I'm talking specifically to us IT people, working in companies
>500 people. It gets harder to relate if you're working in a smaller company,
I guess. If you're in your last semesters of college and majoring in something
IT related, read it as a preparation for the work life (that and all the
*Dilbert* cartoons).

The first time the book struck a nerve was when *Brent*, an IT engineer, was
introduced. Brent is the go-to guy for anything non-trivial. Funnily enough,
he's also most of the time **the only one who knows how it works**. All the
negative sides of this (and how to overcome them) are mentioned in the book.
I'm sure you can name *your Brent* too.

It also doesn't stop with Brent. The book introduces different characters from
different areas in the company. Marketing, developers, the compliance and audit
folks, and of course the operators. You're going to
**recognize many of those characters and their behaviors in your own company**.

Why is this useful for you, you ask? The authors **wave in little learning
lessons** into the story, each time the protagonist and his team fail and
recover. And the team faces obstacles over and over again. A short,
non-exhaustive summary might be:

* developers: get a system wide view; coding is only a part of a bigger 
  picture
* security folks: don't follow the rules blindly, risk mitigation can
  have multiple forms
* managers: not only your team has to perform (help each other out)
* operators: reduce variance and manual effort
* marketing: you're part of the overall flow
* everyone: consider other teams have valid concerns too

And lastly, if you ever struggled to explain to your (non-IT) friends or
family members **how the IT life looks like**, give them this book. They can
ignore the learning aspect and enjoy the thrill of a bunch of IT people
when a system goes down and the finger pointing starts.

If you're not convinced by now, the next section will contain very specific
examples from the book, which might give you a better understanding where
I come from.


The 5 most noteworthy things
============================

I'll start each point with a citation of the book and add my 2 cents
right after it.


1. Work In Progress
-------------------

    WIP is one of the root causes for chronic due-date problems,
    quality issues, and expediters. [...] WIP is the silent killer.

The really great thing about this point is, you can fix that on your own
without relying on somebody else. My very personal rule-of-thumb is, three
items max at any given time. Your results may vary. Also, what size these
items are is also a very personal thing. If they overlap, great,
if they are 100% distinct, 3 contexts is the maximum my mind can handle.

If you work in a company where the culture is very reporting focused,
you might face a situation where having *a lot of things in progress*
is considered to be good thing, while *finishing a few items* might be
less recognized as an effort. Unfortunately, I don't have a solution to
that, as it also depends on your values and motivation.


2. Bottleneck
-------------

    [...] [releasing work] should be based on the tempo of how quickly the
    bottleneck resource can consume work.

That's a thing I honestly have never seen in reality although it makes so
much sense. I blame responsibilities/incentives which are based on single
elements of a value chain only instead of the overall value chain. If you've
ever heard sentences like the following, you may be in such a situation:

* Marketing: *"The developers didn't deliver what we promised."*
* Devs: *"The test team didn't find time to test our latest changes."*
* Test: *"The new SW dev bucket needs a completely different HW setup."*
* Ops: *"We can apply these changes earliest in 6 months."*
* Everyone: *"We could be faster if it weren't for the others..."*


3. Improvements
---------------

    [...] any improvements made anywhere besides the bottleneck
    are an illusion.

Again a thought which makes a ton of sense. The value flow through the
company is not like a garden hose where you put more pressure on it and
then more comes out at the end. It's more like a traffic jam. You can
blast your radio, open a window, honk like crazy, but you won't go faster
until the bottleneck widens.

Despite of the logic, I (and maybe you too) encountered surprising
difficulties when it comes to open up known bottlenecks, not because of
technological reasons but social reasons.


4. Operations
-------------

    It's not the upfront capital that kills you, it's the
    operations and maintenance on the back end.

Raise your hand if you ever were in a meeting were it got decided that a
homegrown solution is the best way although you know N already existing
solutions which fulfill the requirements but nobody listened to you.
Now it's one or two years later and the Behemoth of an "easy" solution
is nearly unmaintainable and every requested change needs 1 PY to implement.

If you've observed this, then the people who made the decisions may have
put more value on the initial costs and less on the operations cost.
It's the same fallacy you make when you buy a car based on the buying price
only and not count in the maintenance cost of the next N years when you
drive it.


5. Flow
-------

    [...] as important as throttling the release of work
    is managing the handoffs. [...] [the] goal is to maximize
    the flow.

Here's a thought I can put a lot of blame on me. I'm a software developer,
and until I've read this book, I've never spent a reasonable amount of
thought on it how operators have to deal with my genius solutions.
Deployment, operations, upgrades; these things were the
*"issues of other people"* and therefor invisible to me. ``¯\_(ツ)_/¯``
I try to become better in this area.

This also doesn't stop at the handoffs between developers and operators.
There are a lot of earlier stages were *work* gets released. Be it:

* a market analysis to justify development effort
* a requirements engineering document
* a feature specification

Sloppy handoffs are an easy way to kill efficiency and throughput. Value
is only generated as soon as the *user can consume* the effort we've
spent for the solution.

----

This book gave me a lot of insights and I enjoyed reading and learning from
it. 

