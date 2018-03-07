=======
logzero
=======


.. image:: https://img.shields.io/pypi/v/logzero.svg
    :target: https://pypi.python.org/pypi/logzero
    :alt: Latest version on PyPi

.. image:: https://travis-ci.org/metachris/logzero.svg?branch=master
    :target: https://travis-ci.org/metachris/logzero
    :alt: Build status for master branch

.. image:: https://readthedocs.org/projects/logzero/badge/?version=latest
    :target: https://logzero.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://pyup.io/repos/github/metachris/logzero/shield.svg
    :target: https://pyup.io/repos/github/metachris/logzero/
    :alt: Updates

.. image:: https://anaconda.org/conda-forge/logzero/badges/version.svg
    :target: https://anaconda.org/conda-forge/logzero
    :alt: Anaconda-Server Badge

Robust and effective logging for Python 2 and 3.

.. image:: https://raw.githubusercontent.com/metachris/logzero/master/docs/_static/logo-small.png
   :alt: Logo
   :width: 300px

* Documentation: https://logzero.readthedocs.io
* GitHub: https://github.com/metachris/logzero


Features
--------

* Easy logging to console and/or (rotating) file.
* Provides a fully configured standard `Python logger object <https://docs.python.org/2/library/logging.html#module-level-functions>`_.
* Pretty formatting, including level-specific colors in the console.
* Windows color output supported by `colorama`_
* Robust against str/bytes encoding problems, works with all kinds of character encodings and special characters.
* Multiple loggers can write to the same logfile (also across multiple Python files).
* Global default logger with `logzero.logger <https://logzero.readthedocs.io/en/latest/#i-logzero-logger>`_ and custom loggers with `logzero.setup_logger(..) <https://logzero.readthedocs.io/en/latest/#i-logzero-setup-logger>`_.
* Compatible with Python 2 and 3.
* All contained in a `single file`_.
* Licensed under the MIT license.
* Heavily inspired by the `Tornado web framework`_.


.. image:: https://raw.githubusercontent.com/metachris/logzero/master/docs/_static/demo_output.png
   :alt: Demo output in color
   :width: 300px


.. _single file: https://github.com/metachris/logzero/blob/master/logzero/__init__.py
.. _Tornado web framework: https://github.com/tornadoweb/tornado
.. _colorama: https://github.com/tartley/colorama


Example Usage
-------------

.. code-block:: python

    from logzero import logger

    logger.debug("hello")
    logger.info("info")
    logger.warn("warn")
    logger.error("error")

    # This is how you'd log an exception
    try:
        raise Exception("this is a demo exception")
    except Exception as e:
        logger.exception(e)


Adding a rotating logfile is that easy:

.. code-block:: python

    import logzero
    from logzero import logger

    # Setup rotating logfile with 3 rotations, each with a maximum filesize of 1MB:
    logzero.logfile("/tmp/rotating-logfile.log", maxBytes=1e6, backupCount=3)

    # Log messages
    logger.info("This log message goes to the console and the logfile")


Here are more examples which show how to use logfiles, custom formatters
and setting a minimum loglevel:

.. code-block:: python

    import logging
    import logzero
    from logzero import logger

    # This log message goes to the console
    logger.debug("hello")

    # Set a minimum log level
    logzero.loglevel(logging.INFO)

    # Set a logfile (all future log messages are also saved there)
    logzero.logfile("/tmp/logfile.log")

    # You can also set a different loglevel for the file handler
    logzero.logfile("/tmp/logfile.log", loglevel=logging.ERROR)

    # Set a rotating logfile (replaces the previous logfile handler)
    logzero.logfile("/tmp/rotating-logfile.log", maxBytes=1000000, backupCount=3)

    # Disable logging to a file
    logzero.logfile(None)

    # Set a custom formatter
    formatter = logging.Formatter('%(name)s - %(asctime)-15s - %(levelname)s: %(message)s');
    logzero.formatter(formatter)

    # Log some variables
    logger.info("var1: %s, var2: %s", var1, var2)

Take a look at the documentation for more information and examples:

* Documentation: https://logzero.readthedocs.io.


Installation
------------

Install `logzero` with `pip`_:

.. code-block:: console

    $ pip install -U logzero

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

Alternatively, if you use the `Anaconda distribution <https://www.anaconda.com/download/>`_:

.. code-block:: console

    $ conda config --add channels conda-forge
    $ conda install logzero

You can also install `logzero` from the public `Github repo`_:

.. code-block:: console

    $ git clone https://github.com/metachris/logzero.git
    $ cd logzero
    $ python setup.py install

On openSUSE you can install the current version from repos: `python2-logzero <https://software.opensuse.org/package/python2-logzero>`_, `python3-logzero <https://software.opensuse.org/package/python3-logzero>`_. In the newest openSUSE release you can install it with zypper: `sudo zypper in python2-logzero`.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/
.. _Github repo: https://github.com/metachris/logzero


Changelog
---------

See the changelog here: https://github.com/metachris/logzero/blob/master/HISTORY.rst


Feedback
--------

All kinds of feedback and contributions are welcome.

* `Create an issue <https://github.com/metachris/logzero/issues/new>`_
* Create a pull request
* `@metachris <https://twitter.com/metachris>`_ // chris@linuxuser.at
