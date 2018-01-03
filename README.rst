===========================
PYM: PYthon Manager (macOS)
===========================

Work in progress. Below is the plan.

Distribution
============

PYM will only be (officially) distributed via Homebrew. The formula will
directly depend on python3, pyenv, and everything else it needs to build
Pythons. [#]_

.. [#] https://github.com/pyenv/pyenv/wiki/Common-build-problems#requirements

The formula does not install anything anywhere outside the keg, except a
``pym`` script to Homebrew’s bin directory (typically ``/usr/local/bin``).
The script would look something like this (not tested)::

    #!/bin/sh

    PREFIX="$(brew --prefix)"
    PYMCELLAR="$PREFIX/Cellar/pym"
    PYTHONPATH="$PYMCELLAR/$(ls -1 "$PYMCELLAR" | tail -n1):$PYTHONPATH"
    "$PREFIX/bin/python3" -m pym $@

So we always use the latest Homebrew Python to run PYM as a module. This avoids
the need of revision-bumping after each Homebrew Python upgrade, which is
ridiculus to me.

I don’t think this is acceptable for Homebrew (I can be wrong), so the formula
will be in a tap for now.


Basic Interface
===============

Similar to SNAFU_.

.. _Snafu: https://github.com/uranusjr/snafu


Versions
========

::

    pym install X.Y

PYM will use pyenv’s ``python-build`` command to build the best match, [#]_
and install it into ``$HOME/.pym/versions/X.Y``. Unlike pyenv, PYM only lets
you specify X.Y, not the micro part.

.. [#] https://github.com/pyenv/pyenv/tree/master/plugins/python-build

After installation, a simlink for ``pythonX.Y`` and a shim for ``pipX.Y`` will
be installed into ``$HOME/.pym/bin``.


Shims
=====

Similar to pyenv (and SNAFU), ``pip`` and ``easy_install`` commands will be
shimmed to allow auto-publishing hooks after you install a package. Unlike
SNAFU, some simple shell scripts will suffice, fortunately. The script will
be generated dynamically, when the user ``use`` versions, to point to the
correct version.

We don’t have the registry to work with. A simple ``config`` file inside
``.pym`` should be enough though. Since all shims know where they point to on
their own, this config is only needed when the user runs ``pym use --add``.


Questions to Answer
===================

Do we need to maintain a list of versions?
------------------------------------------

I hope not.

The simplest solution is asking ``python-build``::

    python-build --definitions

and use a regular expression to get the right version for the name. The
downside is that the command is a bit slow (because there are a ton of
definitions, and the list will only grow longer).

Another way is to look inside pyenv. The definitions are in
``$INSTALL_ROOT/plugins/python-build/share/python-build/``

But how do we find pyenv’s install root? It is not that difficult if we only
want to target Homebrew, but… Or maybe we can do something like

* Get the real path of ``pyenv``. It should be in ``$INSTALL_ROOT/bin``.
* Look for deifnitions with a relative path.

But that seems too fragile. Maybe it would be best to try this, and fallback to
asking ``python-build`` on failure?

