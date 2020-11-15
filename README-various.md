Future Features & Ideas
-----------------------

* Decorator for logging function calls
* Easier usage of custom log handlers (currently works `like this <https://logzero.readthedocs.io/en/latest/#adding-custom-handlers-eg-sysloghandler>`_)
* Send logs to remote log collector (maybe)
* Structured logging a la https://structlog.readthedocs.io/en/stable/index.html (maybe)


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

    # Update history
    vi HISTORY.md
    git add HISTORY.md
    git commit -m "Changelog for upcoming release"

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
