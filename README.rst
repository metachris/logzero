=======
logzero
=======


.. image:: https://img.shields.io/pypi/v/logzero.svg
        :target: https://pypi.python.org/pypi/logzero

.. image:: https://img.shields.io/travis/metachris/logzero.svg
        :target: https://travis-ci.org/metachris/logzero

.. image:: https://readthedocs.org/projects/logzero/badge/?version=latest
        :target: https://logzero.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/metachris/logzero/shield.svg
     :target: https://pyup.io/repos/github/metachris/logzero/
     :alt: Updates


Robust and effective logging for Python 2 and 3.

.. image:: docs/_static/logo-small.png
   :alt: Logo
   :width: 300px

* Documentation: https://logzero.readthedocs.io
* GitHub: https://github.com/metachris/logzero


Features
--------

* Easy logging to console and/or (rotating) file.
* Provides a fully configured standard `Python logger object <https://docs.python.org/2/library/logging.html#module-level-functions>`_.
* Pretty formatting, including level-specific colors in the console.
* Robust against str/bytes encoding problems, works with all kinds of character encodings and special characters.
* Multiple loggers can write to the same logfile (also across multiple Python files).
* Global default logger with `logzero.logger <https://logzero.readthedocs.io/en/latest/#i-logzero-logger>`_ and custom loggers with `logzero.setup_logger(..) <https://logzero.readthedocs.io/en/latest/#i-logzero-setup-logger>`_.
* Compatible with Python 2 and 3.
* All contained in a `single file`_.
* No further Python dependencies.
* Licensed under the MIT license.
* Heavily inspired by the `Tornado web framework`_.


.. image:: docs/_static/demo_output.png
   :alt: Demo output in color
   :width: 300px


.. _single file: https://github.com/metachris/logzero/blob/master/logzero/__init__.py
.. _Tornado web framework: https://github.com/tornadoweb/tornado


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
=============

Install `logzero` with `pip`_:

.. code-block:: console

    $ pip install -U logzero


Changelog
---------

See the changelog here: https://github.com/metachris/logzero/blob/master/HISTORY.rst


Future Features & Ideas
-----------------------

* Decorator for logging function calls
* Easier usage of custom log handlers (currently works `like this <https://logzero.readthedocs.io/en/latest/#adding-custom-handlers-eg-sysloghandler>`_)
* JSON output (a la 12 factor app)
* Send logs to remote log collector (maybe)
* Structured logging a la https://structlog.readthedocs.io/en/stable/index.html (maybe)


TODO
----

* Tests

  * Custom handlers and reconfiguration
  * Strange behaviour: py.test with default logger - capturing err does not work if the logger is setup initially in logzero. Only works when setup from the py script.


Related Projects
----------------

* https://12factor.net/logs
* Log collectors: fluentd, logstash, etc.
* https://structlog.readthedocs.io/en/stable/why.html


Notes: How to release a new version
-----------------------------------

via https://cookiecutter-pypackage.readthedocs.io/en/latest/pypi_release_checklist.html

.. code-block:: console

    # Run the tests
    py.test
    make lint

    # Update history
    vi HISTORY.rst
    git add HISTORY.rst
    git commit -m "Changelog for upcoming release 0.1.1."

    # Update version
    bumpversion minor

    # Push
    git push && git push --tags


Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage


.. _pip: https://pip.pypa.io

