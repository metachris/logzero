Future Features & Ideas
-----------------------

* Decorator for logging function calls
* Easier usage of custom log handlers (currently works `like this <https://logzero.readthedocs.io/en/latest/#adding-custom-handlers-eg-sysloghandler>`_)
* JSON output (a la 12 factor app)
* Send logs to remote log collector (maybe)
* Structured logging a la https://structlog.readthedocs.io/en/stable/index.html (maybe)


TODO
----

* Travis CI: pypy3 gives error `RuntimeError: Python 3.3 or later is required` (see `job 255217329 <https://travis-ci.org/metachris/logzero/jobs/255217329>`_)
* Tests

  * Custom handlers and reconfiguration
  * Strange behaviour: py.test with default logger - capturing err does not work if the logger is setup initially in logzero. Only works when setup from the py script.


Related Projects
----------------

* https://logbook.readthedocs.io/en/stable/index.html
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
    tox

    # Update history
    vi HISTORY.rst
    git add HISTORY.rst
    git commit -m "Changelog for upcoming release 0.1.1."

    # Update version
    bumpversion minor

    # Push
    git push && git push --tags

Update conda-forge: https://github.com/metachris/logzero/issues/67#issuecomment-353016366

Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage


.. _pip: https://pip.pypa.io

