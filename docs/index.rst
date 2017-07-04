.. highlight:: shell
.. _index:

===================================
`logzero`: Python logging made easy
===================================

Robust and effective logging for Python 2 and 3.

.. image:: _static/logo-small.png
   :alt: Logo
   :width: 300px

**Features**

* Easy logging to console and/or file.
* Provides a fully configured standard `Python logger object <https://docs.python.org/2/library/logging.html#module-level-functions>`_.
* Pretty formatting, including level-specific colors in the console.
* Robust against str/bytes encoding problems, works with all kinds of character encodings and special characters.
* Multiple loggers can write to the same logfile (also works across multiple Python files).
* Global default logger with `logzero.logger <#i-logzero-logger>`_ and custom loggers with `logzero.setup_logger(..) <#i-logzero-setup-logger>`_.
* Compatible with Python 2 and 3.
* All contained in a `single file`_.
* No further Python dependencies.
* Licensed under the MIT license.
* Heavily inspired by the `Tornado web framework`_.
* Hosted on GitHub: https://github.com/metachris/logzero


.. image:: _static/demo_output.png
   :alt: Demo output in color
   :width: 300px


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

You can use `logzero` with the default `logger` like this:

.. code-block:: python

    from logzero import logger

    logger.debug("hello")
    logger.info("info")
    logger.warn("warn")
    logger.error("error")

If this was a file called `demo.py`, the output will look like this:

.. image:: _static/demo_output.png
   :alt: Demo output in color
   :width: 300px

.. code-block:: console

    [D 170628 09:30:53 demo:4] hello
    [I 170628 09:30:53 demo:5] info
    [W 170628 09:30:53 demo:6] warn
    [E 170628 09:30:53 demo:7] error


You can reconfigure the global default logger with `logzero.setup_default_logger(..) <#i-logzero-setup-default-logger>`_, to set a
logfile, minimum loglevel or a custom formatter.

------------

Instead of using the default logger you can also setup a specific `logger` object with `logzero.setup_logger(..) <#i-logzero-setup-logger>`_:

.. code-block:: python

    from logzero import setup_logger
    logger = setup_logger(logfile="/tmp/test.log", level=logging.WARN)

    logger.debug("hello")
    logger.info("info")
    logger.warn("warn")
    logger.error("error")


Logging to a logfile
------------------

You can also easily setup logging to a logfile by supplying the `logfile` attribute.
`logzero` supports multiple loggers writing to the same logfile, even across multiple Python files.


You can set the logfile for the global default logger with `logzero.setup_default_logger(..) <#i-logzero-setup-default-logger>`_ like this:

.. code-block:: python

    logzero.setup_default_logger(logfile="/tmp/test.log")

To configure a specific logger instance use `logzero.setup_logger(..) <#i-logzero-setup-logger>`_:

.. code-block:: python

    logger = logzero.setup_logger(logfile="/tmp/test.log")


Logging variables
------------------


This is how you can log variables too:

.. code-block:: python

    logger.debug("var1: %s, var2: %s", var1, var2)


Setting the minimum loglevel
----------------------------

You can set the minimum logging level to any of the standard `Python log levels <https://docs.python.org/2/library/logging.html#logging-levels>`_.
For instance if you want to set the minimum logging level to `INFO` (default is `DEBUG`):

.. code-block:: python

    setup_logger(level=logging.INFO)


Adding custom handlers (eg. RotatingLogFile)
--------------------------------------------

Since `logzero` uses the standard `Python logger object <https://docs.python.org/2/library/logging.html#module-level-functions>`_,
you can attach any `Python logging handlers <https://docs.python.org/2/library/logging.handlers.html>`_ you can imagine!

This is how you add a `RotatingFileHandler <https://docs.python.org/2/library/logging.handlers.html#rotatingfilehandler>`_:

.. code-block:: python

    import logzero
    import logging
    from logging.handlers import RotatingFileHandler

    # Setup the RotatingFileHandler
    rotating_file_handler = RotatingFileHandler("/tmp/app-rotating.log", maxBytes=100000, backupCount=2)
    rotating_file_handler.setLevel(logging.DEBUG)
    rotating_file_handler.setFormatter(logzero.LogFormatter(color=False))

    # Attach it to the logzero default logger
    logzero.logger.addHandler(rotating_file_handler)

    # Log messages
    logzero.logger.info("this is a test")


Documentation
=================

.. _i-logzero-logger:

`logzero.logger`
------------------

`logzero.logger` is an already set up standard `Python logger instance <https://docs.python.org/2/library/logging.html#module-level-functions>`_ for your convenience. You can use it from all your
files and modules directly like this:

.. code-block:: python

    from logzero import logger

    logger.debug("hello")
    logger.info("info")
    logger.warn("warn")
    logger.error("error")

You can reconfigure the default logger globally with `logzero.setup_default_logger(..) <#i-logzero-setup-default-logger>`_.

See the documentation for the `Python logger instance <https://docs.python.org/2/library/logging.html#module-level-functions>`_ for more information about how you can use it.

.. _i-logzero-setup-logger:

`logzero.setup_logger(..)`
------------------

.. autofunction:: logzero.setup_logger

.. _i-logzero-setup-default-logger:

`logzero.setup_default_logger(..)`
------------------

.. autofunction:: logzero.setup_default_logger


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
    logzero.setup_default_logger(formatter=formatter)


Issues, Feedback & Contributions
================================

All kind of feedback and contributions are welcome.

* `Create an issue <https://github.com/metachris/logzero/issues/new>`_
* Create a pull request
* https://github.com/metachris/logzero
* chris@linuxuser.at // `@metachris <https://twitter.com/metachris>`_
