# logzero

![Build status for master branch](https://github.com/metachris/logzero/workflows/Run%20the%20tests/badge.svg)
[![Documentation Status](https://readthedocs.org/projects/logzero/badge/?version=latest)](https://logzero.readthedocs.io/en/latest/?badge=latest)
[![Latest version on PyPi](https://img.shields.io/pypi/v/logzero.svg)](https://pypi.python.org/pypi/logzero)
[![Anaconda-Server Badge](https://anaconda.org/conda-forge/logzero/badges/version.svg)](https://anaconda.org/conda-forge/logzero)

Robust and effective logging for Python 2 and 3.

![Logo](https://raw.githubusercontent.com/metachris/logzero/master/docs/_static/logo-small.png)

* Documentation: https://logzero.readthedocs.io
* GitHub: https://github.com/metachris/logzero


Features
--------

* Easy logging to console and/or (rotating) file.
* Provides a fully configured standard [Python logger object](https://docs.python.org/2/library/logging.html#module-level-functions>).
* No dependencies
* Pretty formatting, including level-specific colors in the console.
* Windows color output supported by [colorama](https://github.com/tartley/colorama)
* Robust against str/bytes encoding problems, works with all kinds of character encodings and special characters.
* Multiple loggers can write to the same logfile (also across multiple Python files and processes).
* JSON logging support (with integrated [python-json-logger](https://github.com/madzak/python-json-logger))
* Global default logger with [logzero.logger](https://logzero.readthedocs.io/en/latest/#i-logzero-logger) and custom loggers with [logzero.setup_logger(..)](https://logzero.readthedocs.io/en/latest/#i-logzero-setup-logger).
* Compatible with Python 2 and 3.
* All contained in a [single file](https://github.com/metachris/logzero/blob/master/logzero/__init__.py).
* Licensed under the MIT license.
* Heavily inspired by the [Tornado web framework](https://github.com/tornadoweb/tornado).

![Demo output in color](https://raw.githubusercontent.com/metachris/logzero/master/docs/_static/demo_output.png)


Example Usage
-------------

```python
from logzero import logger

logger.debug("hello")
logger.info("info")
logger.warning("warn")
logger.error("error")

# This is how you'd log an exception
try:
    raise Exception("this is a demo exception")
except Exception as e:
    logger.exception(e)
```

Adding a rotating logfile is that easy:

```python
import logzero
from logzero import logger

# Setup rotating logfile with 3 rotations, each with a maximum filesize of 1MB:
logzero.logfile("/tmp/rotating-logfile.log", maxBytes=1e6, backupCount=3)

# Log messages
logger.info("This log message goes to the console and the logfile")
```

Here are more examples which show how to use logfiles, custom formatters
and setting a minimum loglevel:

```python
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
```

### JSON logging

JSON logging can be enabled for the default logger with `logzero.json()`, or with `setup_logger(json=True)` for custom loggers:

```python
>>> logzero.json()
>>> logger.info("test")
{"asctime": "2020-10-21 10:42:45,808", "filename": "<stdin>", "funcName": "<module>", "levelname": "INFO", "levelno": 20, "lineno": 1, "module": "<stdin>", "message": "test", "name": "logzero_default", "pathname": "<stdin>", "process": 76179, "processName": "MainProcess", "threadName": "MainThread"}

>>> my_logger = setup_logger(json=True)
>>> my_logger.info("test")
{"asctime": "2020-10-21 10:42:45,808", "filename": "<stdin>", "funcName": "<module>", "levelname": "INFO", "levelno": 20, "lineno": 1, "module": "<stdin>", "message": "test", "name": "logzero_default", "pathname": "<stdin>", "process": 76179, "processName": "MainProcess", "threadName": "MainThread"}
```

The logged JSON object has these fields:

```json
{
  "asctime": "2020-10-21 10:43:40,765",
  "filename": "test.py",
  "funcName": "test_this",
  "levelname": "INFO",
  "levelno": 20,
  "lineno": 9,
  "module": "test",
  "message": "info",
  "name": "logzero",
  "pathname": "_tests/test.py",
  "process": 76204,
  "processName": "MainProcess",
  "threadName": "MainThread"
}```

An exception logged with `logger.exception(e)` has these:

```json
{
  "asctime": "2020-10-21 10:43:25,193",
  "filename": "test.py",
  "funcName": "test_this",
  "levelname": "ERROR",
  "levelno": 40,
  "lineno": 17,
  "module": "test",
  "message": "this is a demo exception",
  "name": "logzero",
  "pathname": "_tests/test.py",
  "process": 76192,
  "processName": "MainProcess",
  "threadName": "MainThread",
  "exc_info": "Traceback (most recent call last):\n  File \"_tests/test.py\", line 15, in test_this\n    raise Exception(\"this is a demo exception\")\nException: this is a demo exception"
}```

Take a look at the documentation for more information and examples:

* Documentation: https://logzero.readthedocs.io.


Installation
------------

Install `logzero` with [pip](https://pip.pypa.io):

```shell
$ pip install -U logzero
```

If you don't have [pip](https://pip.pypa.io) installed, this [Python installation guide](http://docs.python-guide.org/en/latest/starting/installation/) can guide
you through the process.

Alternatively, if you use the [Anaconda distribution](https://www.anaconda.com/download/):

```shell
$ conda config --add channels conda-forge
$ conda install logzero
```

You can also install `logzero` from the public [Github repo](https://github.com/metachris/logzero):

```shell
$ git clone https://github.com/metachris/logzero.git
$ cd logzero
$ python setup.py install
```

On openSUSE you can install the current version from repos: [python2-logzero](https://software.opensuse.org/package/python2-logzero), [python3-logzero](https://software.opensuse.org/package/python3-logzero). In the newest openSUSE release you can install it with zypper: `sudo zypper in python2-logzero`.


Development
-----------

Notes:

* Using pytest as test runner
* CI is run with [Github actions](https://github.com/metachris/logzero/tree/master/.github/workflows).
* Download stats: https://pepy.tech/project/logzero

### Getting started

```shell
# Activate virtualenv
$ python3 -m venv venv
$ . venv/bin/activate

# Install main and dev dependencies
$ pip install -e .
$ pip install -r requirements_dev.txt

# Run the tests
$ make test

# Run the linter
$ make lint

# Generate the docs (will auto-open in Chrome)
$ make docs
```

**To do**

* CI to publish package to PyPI


---

Changelog
---------

See the changelog here: https://github.com/metachris/logzero/blob/master/HISTORY.md


Feedback
--------

All kinds of feedback and contributions are welcome.

* [Create an issue](https://github.com/metachris/logzero/issues/new>)
* Create a pull request
* [@metachris](https://twitter.com/metachris) // chris@linuxuser.at
