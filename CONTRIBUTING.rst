.. highlight:: shell

============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every little bit
helps, and credit will always be given.

You can contribute in many ways:

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://github.com/rdnfn/beobench/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs. Anything tagged with "bug" and "help
wanted" is open to whoever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for features. Anything tagged with "enhancement"
and "help wanted" is open to whoever wants to implement it.

Write Documentation
~~~~~~~~~~~~~~~~~~~

beobench could always use more documentation, whether as part of the
official beobench docs, in docstrings, or even on the web in blog posts,
articles, and such.

To update the API docs, use the following command inside the ``/docs`` directory:

.. code-block::

    sphinx-apidoc -f -o . ..


Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at https://github.com/rdnfn/beobench/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

Get Started!
------------

Ready to contribute? Here's how to set up `beobench` for local development.

1. Follow :doc:`this guide <guides/dev_env>` to fork the repo and setup the development environment.

2. Inside the devcontainer just set up, create a branch for local development::

    $ git checkout -b dev/name-of-your-bugfix-or-feature

   Now you can make your changes locally.

3. When you're done making changes, check that your changes pass flake8 and the
   tests, including testing other Python versions with tox::

    $ flake8 beobench tests
    $ python setup.py test
    $ tox

4. Commit your changes and push your branch to GitHub::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

5. Submit a pull request through the GitHub website.

Guidelines
----------

Commit messages
~~~~~~~~~~~~~~~

When committing to the Beobench repo, please try to follow `this style
guide by Udacity <https://udacity.github.io/git-styleguide/>`_ for the
commit messages with the following adaptions:

1. Replace the ``chore:`` type with ``aux:``.
2. Use a ``exp:`` type for commits relating to experiment data (e.g. experiment config files).


Pull Requests
~~~~~~~~~~~~~

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.rst.


.. 3. The pull request should work for Python 3.6, 3.7, 3.8 and 3.9.

.. Check https://travis-ci.com/rdnfn/beobench/pull_requests
   and make sure that the tests pass for all supported Python versions.

Tips
----

To run a subset of tests::


    $ python -m unittest tests.test_beobench


Resources
---------

Documentation and cheatsheets for reStructuredText (``.rst`` files):

* https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html
* https://bashtage.github.io/sphinx-material/rst-cheatsheet/rst-cheatsheet.html

Deploying
---------

A reminder for the maintainers on how to deploy. Follow this checklist (inspired by `this checklist <https://gist.github.com/audreyfeldroy/5990987>`_ and `this packaging tutorial <https://packaging.python.org/en/latest/tutorials/packaging-projects/>`_):

1. Update ``HISTORY.rst`` and commit with message like "aux: add changelog for upcoming release 0.1.0"
2. Run

    .. code-block:: console

        bump2version patch # possible: major / minor / patch

3. Push commits *and tags* (`see here how to do this in vscode <https://stackoverflow.com/a/66086007>`_)
4. Merge pull request into ``main`` branch.
5. Add release on GitHub (using existing tag)