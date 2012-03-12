########################
Contributing to Pymaging
########################

Like every open-source project, Pymagin is always looking for motivated
individuals to contribute to it's source code.
However, to ensure the highest code quality and keep the repository nice and
tidy, everyone is encouraged to follow a few simple guidelines to make it
easier for everyone.


*********
Community
*********

People interested in developing for the Pymaging should join the #pymaging
IRC channel on `freenode`_ for help and to discuss the development.


*************
In a nutshell
*************

Here's what the contribution process looks like, in a bullet-points fashion, and
only for the stuff we host on GitHub:

#. Pymaging is hosted on `GitHub`_, at https://github.com/ojii/pymaging
#. The best method to contribute back is to create an account there, then fork
   the project. You can use this fork as if it was your own project, and should
   push your changes to it.
#. When you feel your code is good enough for inclusion, "send us a `pull
   request`_", using the nice GitHub web interface.



*****************
Contributing Code
*****************


General
=======

- Code *must* be tested. Untested patches will be declined.
- If a patch affects the public facing API, it must document these changes.

Since we're hosted on GitHub, pymagin uses `git`_ as a version control system.

The `GitHub help`_ is very well written and will get you started on using git
and GitHub in a jiffy. It is an invaluable resource for newbies and old timers
alike.


Syntax and conventions
======================

We try to conform to `PEP8`_ as much as possible. A few highlights:

- Indentation should be exactly 4 spaces. Not 2, not 6, not 8. **4**. Also, tabs
  are evil.
- We try (loosely) to keep the line length at 79 characters. Generally the rule
  is "it should look good in a terminal-base editor" (eg vim), but we try not be
  [Godwin's law] about it.


Process
=======

This is how you fix a bug or add a feature:

#. `fork`_ us on GitHub.
#. Checkout your fork.
#. Hack hack hack, test test test, commit commit commit, test again.
#. Push to your fork.
#. Open a pull request.


Tests
=====

Having a wide and comprehensive library of unit and integration tests is
of exceeding importance. Contributing tests is widely regarded as a very
prestigious contribution (you're making everybody's future work much easier by
doing so). Good karma for you. Cookie points. Maybe even a beer if we meet in
person :)

If you're unsure how to write tests, feel free to ask for help on IRC.

Running the tests
-----------------

To run the tests we recommend using ``nose``. If you have ``nose`` installed,
just run ``nosetests`` in the root directory. If you don't, you can also use
``python -m unittest discover``.


**************************
Contributing Documentation
**************************

Perhaps considered "boring" by hard-core coders, documentation is sometimes even
more important than code! This is what brings fresh blood to a project, and
serves as a reference for old timers. On top of this, documentation is the one
area where less technical people can help most - you just need to write a
semi-decent English. People need to understand you. We don't care about style or
correctness.

Documentation should be:

- We use `Sphinx`_/`restructuredText`_. File extensions should be .rst.
- Written in English. We can discuss how it would bring more people to the
  project to have a Klingon translation or anything, but that's a problem we
  will ask ourselves when we already have a good documentation in English.
- Accessible. You should assume the reader to be moderately familiar with
  Python, but not anything else.

Also, contributing to the documentation will earn you great respect from the
core developers. You get good karma just like a test contributor, but you get
double cookie points. Seriously. You rock.

Section style
=============

We use Python documentation conventions fo section marking:

* ``#`` with overline, for parts
* ``*`` with overline, for chapters
* ``=``, for sections
* ``-``, for subsections
* ``^``, for subsubsections
* ``"``, for paragraphs


.. _fork: http://github.com/ojii/pymaging
.. _Sphinx: http://sphinx.pocoo.org/
.. _PEP8: http://www.python.org/dev/peps/pep-0008/
.. _GitHub : http://www.github.com
.. _GitHub help : http://help.github.com
.. _freenode : http://freenode.net/
.. _pull request : http://help.github.com/send-pull-requests/
.. _git : http://git-scm.com/
.. _restructuredText: http://docutils.sourceforge.net/docs/ref/rst/introduction.html

