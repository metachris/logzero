# logzero

![Build status for master branch](https://github.com/metachris/logzero/workflows/Run%20the%20tests/badge.svg)
[![Documentation Status](https://readthedocs.org/projects/logzero/badge/?version=latest)](https://logzero.readthedocs.io/en/latest/?badge=latest)
[![Latest version on PyPi](https://img.shields.io/pypi/v/logzero.svg)](https://pypi.python.org/pypi/logzero)
[![Anaconda-Server Badge](https://anaconda.org/conda-forge/logzero/badges/version.svg)](https://anaconda.org/conda-forge/logzero)
[![Downloads](https://pepy.tech/badge/logzero/week)](https://pepy.tech/project/logzero)

Robust and effective logging for Python 2 and 3.

![Logo](https://raw.githubusercontent.com/metachris/logzero/master/docs/_static/demo-output-with-beaver.png)

* Documentation: https://logzero.readthedocs.io
* GitHub: https://github.com/metachris/logzero


Features
--------

* Easy logging to console and/or (rotating) file.
* Provides a fully configured standard [Python logger object](https://docs.python.org/2/library/logging.html#module-level-functions>).
* JSON logging (with integrated [python-json-logger](https://github.com/madzak/python-json-logger))
* Pretty formatting, including level-specific colors in the console.
* No dependencies
* Windows color output supported by [colorama](https://github.com/tartley/colorama)
* Robust against str/bytes encoding problems, works with all kinds of character encodings and special characters.
* Multiple loggers can write to the same logfile (also across multiple Python files and processes).
* Global default logger with [logzero.logger](https://logzero.readthedocs.io/en/latest/#i-logzero-logger) and custom loggers with [logzero.setup_logger(..)](https://logzero.readthedocs.io/en/latest/#i-logzero-setup-logger).
* Compatible with Python 2 and 3.
* All contained in a [single file](https://github.com/metachris/logzero/blob/master/logzero/__init__.py).
* Licensed under the MIT license.
* Heavily inspired by the [Tornado web framework](https://github.com/tornadoweb/tornado).


Installation:

```shell
python -m pip install logzero
```

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

# JSON logging
import logzero
logzero.json()

logger.info("JSON test")

# Start writing into a logfile
logzero.logfile("/tmp/logzero-demo.log")

# Set a minimum loglevel
logzero.loglevel(logzero.WARNING)
```

This is the output:

![demo-output](https://raw.githubusercontent.com/metachris/logzero/master/docs/_static/demo-output-json.png)

Note: You can find more examples in the documentation: https://logzero.readthedocs.io

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
}
```

Exceptions logged with `logger.exception(e)` have these additional JSON fields:

```json
{
  "levelname": "ERROR",
  "levelno": 40,
  "message": "this is a demo exception",
  "exc_info": "Traceback (most recent call last):\n  File \"_tests/test.py\", line 15, in test_this\n    raise Exception(\"this is a demo exception\")\nException: this is a demo exception"
}
```

Take a look at the documentation for more information and examples:

* Documentation: https://logzero.readthedocs.io.


Installation
------------

Install `logzero` with [pip](https://pip.pypa.io):

```shell
python -m pip install logzero
```

Here's how you setup a virtualenv and download and run the demo:

```shell
# Create and activate a virtualenv in ./venv/
python3 -m venv venv
. venv/bin/activate

# Install logzero
python -m pip install logzero

# Download and run demo.py
wget https://raw.githubusercontent.com/metachris/logzero/master/examples/demo.py
python demo.py
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

Contributors
------------

* [Chris Hager](https://github.com/metachris)
* [carlodr](https://github.com/carlodri)
* [Brian Lenz](https://github.com/brianlenz)
* [David Martin](https://github.com/dmartin35)
* [Zakaria Zajac](madzak) (creator of [python-json-logger](https://github.com/madzak/python-json-logger))

---

Development
-----------

**Getting started**

```shell
$ git clone https://github.com/metachris/logzero.git
$ cd logzero

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

# You can enable watching mode to automatically rebuild on changes:
$ make servedocs
```

To test with Python 2.7, you can use Docker:

```shell
docker run --rm -it -v /Users/chris/stream/logzero:/mnt python:2.7 /bin/bash
```

Now you have a shell with the current directory mounted into `/mnt/` inside the container.

**Notes**

* [pytest](https://docs.pytest.org/en/latest/) is the test runner
* CI is run with [Github actions](https://github.com/metachris/logzero/tree/master/.github/workflows).
* Download stats: https://pepy.tech/project/logzero

---

Changelog
---------

See the changelog here: https://github.com/metachris/logzero/blob/master/HISTORY.md


Feedback
--------

All kinds of feedback and contributions are welcome.

* [Create an issue](https://github.com/metachris/logzero/issues/new)
* Create a pull request
* [@metachris](https://twitter.com/metachris)

![logo](https://raw.githubusercontent.com/metachris/logzero/master/docs/_static/logo-420.png)
