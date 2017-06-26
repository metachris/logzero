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


Python logging made easy

* GitHub repository: https://github.com/metachris/logzero.
* Documentation: https://logzero.readthedocs.io.


Features
--------

* Easy logging to console and/or file.
* Pretty formatting, including level-specific colors in the console.
* Robust against str/bytes encoding problems, works with all kinds of character encodings and special characters.
* All contained in a `single file`_.
* Licensed under the MIT license.
* Heavily inspired by the `Tornado web framework`_.
* Hosted on GitHub: https://github.com/metachris/logzero


Example Usage
-------------

    from logzero import setup_logger
    logger = setup_logger()
    logger.info("hello")


Take a look at the documentation for more information and examples:

* Documentation: https://logzero.readthedocs.io.


Notes
-----

* https://cookiecutter-pypackage.readthedocs.io/en/latest/pypi_release_checklist.html


Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

