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

* GitHub repository: https://github.com/metachris/logzero
* Documentation: https://logzero.readthedocs.io


Features
--------

* Easy logging to console and/or file.
* Provides a fully configured standard `Python logger object <https://docs.python.org/2/library/logging.html#module-level-functions>`_.
* Pretty formatting, including level-specific colors in the console.
* Robust against str/bytes encoding problems, works with all kinds of character encodings and special characters.
* Multiple loggers can write to the same logfile (also across multiple Python files).
* Global default logger with `logzero.logger` and custom loggers with `logzero.setup_logger(..)`.
* Compatible with Python 2 and 3.
* All contained in a `single file`_.
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

Take a look at the documentation for more information and examples:

* Documentation: https://logzero.readthedocs.io.


Installation
=============

Install `logzero` with `pip`_:

.. code-block:: console

    $ pip install -U logzero


Future Features & Ideas
-----------------------

* Rotating Logfiles
* JSON output a la 12 factor app
* Send logs to remote log collector (maybe)
* Structured logging a la https://structlog.readthedocs.io/en/stable/index.html (maybe)


Related Projects
----------------

* https://structlog.readthedocs.io/en/stable/why.html
* https://12factor.net/logs
* fluentd, logstash


Notes: How to release a new version
-----------------------------------

via https://cookiecutter-pypackage.readthedocs.io/en/latest/pypi_release_checklist.html

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

