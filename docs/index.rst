.. highlight:: shell
.. _index:

===================================
`logzero`: Python logging made easy
===================================

`logzero` is a simple and effective logging module for Python 2 and 3.

* Easy logging to console and/or file.
* Pretty formatting, including level-specific colors in the console.
* Robust against str/bytes encoding problems, works with all kinds of character encodings and special characters.
* All contained in a `single file`_.
* Licensed under the MIT license.
* Heavily inspired by the `Tornado web framework`_.
* Hosted on GitHub: https://github.com/metachris/logzero



Installation
=============

Install `logzero` with `pip`_:

.. code-block:: console

    $ pip install -U logzero

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

You can also install `logzero` from the public `Github repo`_:

.. code-block:: console

    $ git clone git://github.com/metachris/logzero
    $ cd logzero
    $ python setup.py install

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/
.. _Github repo: https://github.com/metachris/logzero
.. _tarball: https://github.com/metachris/logzero/tarball/master


Example Usage
=============

You can use `logzero` like this:

.. code-block:: python

    from logzero import setup_logger
    logger = setup_logger()

    ...

    logger.info("hello")

If `logger.info(..)` was called from a file called `test.py` in line 101, the output will look like this:

.. code-block:: console

    [I 170213 15:02:00 test:101] hello


.. _single file: https://github.com/metachris/logzero/blob/master/logzero/__init__.py
.. _Tornado web framework: https://github.com/tornadoweb/tornado

You can easily log variables too:

.. code-block:: python

    logger.debug("var1: %s, var2: %s", var1, var2)



Documentation
=================

`setup_logger(..)`
------------------

.. autofunction:: logzero.setup_logger


Default Log Format
------------------

This is the default log format string:

.. code-block:: python

    DEFAULT_FORMAT = '%(color)s[%(levelname)1.1s %(asctime)s %(module)s:%(lineno)d]%(end_color)s %(message)s'

See also the `Python LogRecord attributes <https://docs.python.org/2/library/logging.html#logrecord-attributes>`_ you can use.


Custom Formatting
-----------------

It is easy to use a custom formatter / a custom log format string:

* Define your log format string (you can use any of the `LogRecord attributes <https://docs.python.org/2/library/logging.html#logrecord-attributes>`_).
* Create a `Formatter object <https://docs.python.org/2/library/logging.html#formatter-objects>`_ (based on `logzero.LogFormatter` to get all the encoding helpers).
* Supply the formatter object to the `formatter` argument in the `setup_logger(..)` method.

This is a working example on how to setup logging with a custom format:

.. code-block:: python

    import logzero

    log_format = '%(color)s[%(levelname)1.1s %(asctime)s %(module)s:%(lineno)d]%(end_color)s %(message)s'
    formatter = logzero.LogFormatter(fmt=log_format)
    logger = logzero.setup_logger(formatter=formatter)


Issues, Feedback & Contributions
================================

All kind of feedback and contributions are welcome.

* `Create an issue <https://github.com/metachris/logzero/issues/new>`_
* Create a pull request
* https://github.com/metachris/logzero
* chris@linuxuser.at // `@metachris <https://twitter.com/metachris>`_
