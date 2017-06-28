.. highlight:: shell
.. _index:

===================================
`logzero`: Python logging made easy
===================================

Robust and effective logging for Python 2 and 3.

.. image:: _static/logo.png
   :alt: Logo
   :width: 300px

**Features**

* Easy logging to console and/or file.
* Pretty formatting, including level-specific colors in the console.
* Robust against str/bytes encoding problems, works with all kinds of character encodings and special characters.
* Compatible with Python 2 and 3.
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

    $ git clone https://github.com/metachris/logzero.git
    $ cd logzero
    $ python setup.py install

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/
.. _Github repo: https://github.com/metachris/logzero
.. _tarball: https://github.com/metachris/logzero/tarball/master
.. _single file: https://github.com/metachris/logzero/blob/master/logzero/__init__.py
.. _Tornado web framework: https://github.com/tornadoweb/tornado


Example Usage
=============

You can use `logzero` like this:

.. code-block:: python

    from logzero import setup_logger
    logger = setup_logger()

    logger.debug("hello")
    logger.info("info")
    logger.warn("warn")
    logger.error("error")

If `logger.info(..)` was called from a file called `demo.py`, the output will look like this:

.. image:: _static/demo_output.png
   :alt: Demo output in color

.. code-block:: console

    [D 170628 09:30:53 demo:4] hello
    [I 170628 09:30:53 demo:5] info
    [W 170628 09:30:53 demo:6] warn
    [E 170628 09:30:53 demo:7] error

You can also easily log to a file as well:

.. code-block:: python

    logger = setup_logger(logfile="/tmp/test.log")

This is how you can log variables too:

.. code-block:: python

    logger.debug("var1: %s, var2: %s", var1, var2)

This is how you can set the minimum logging level to `INFO` (default is `DEBUG`):

.. code-block:: python

    setup_logger(level=logging.INFO)


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
