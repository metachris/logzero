# -*- coding: utf-8 -*-
"""
This helper provides a versatile yet easy to use and beautiful logging setup.
You can use it to log to the console and optionally to a logfile. This propject
is heavily inspired by the Tornado web framework.

* https://logzero.readthedocs.io
* https://github.com/metachris/logzero

The call `logger.info("hello")` prints log messages in this format:

    [I 170213 15:02:00 test:203] hello

Usage:

    from logzero import logger

    logger.debug("hello")
    logger.info("info")
    logger.warn("warn")
    logger.error("error")

In order to also log to a file, just add a `logfile` parameter:

    logzero.setup_default_logger(logfile="/tmp/test.log")

If you want to use specific loggers instead of the global default logger, use
`setup_logger(..)` instead of `setup_default_logger(..)`:

    logger = logzero.setup_logger(logfile="/tmp/test.log")

The default loglevel is `logging.DEBUG`. You can set it with the
parameter `level`.

See the documentation for more information: https://logzero.readthedocs.io
"""
import sys
import logging
try:
    import curses  # type: ignore
except ImportError:
    curses = None

__author__ = """Chris Hager"""
__email__ = 'chris@linuxuser.at'
__version__ = '1.1.2'

# Python 2+3 compatibility settings for logger
bytes_type = bytes
if sys.version_info >= (3, ):
    unicode_type = str
    basestring_type = str
    xrange = range
else:
    # The names unicode and basestring don't exist in py3 so silence flake8.
    unicode_type = unicode  # noqa
    basestring_type = basestring  # noqa


def setup_logger(name=None, logfile=None, level=logging.DEBUG, formatter=None):
    """
    Configures and returns a fully configured logger instance, no hassles.
    If a logger with the specified name already exists, it returns the existing instance,
    else creates a new one.

    Usage:

    .. code-block:: python

        from logzero import setup_logger
        logger = setup_logger()
        logger.info("hello")

    :arg string name: Name of the `Logger object <https://docs.python.org/2/library/logging.html#logger-objects>`_. Multiple calls to `setup_logger()` with the same name will always return a reference to the same Logger object. (defaut: `__name__`)
    :arg string logfile: If set, also write logs to the specified filename.
    :arg int level: Minimum `logging-level <https://docs.python.org/2/library/logging.html#logging-levels>`_ to display (default: `logging.DEBUG`).
    :arg Formatter formatter: `Python logging Formatter object <https://docs.python.org/2/library/logging.html#formatter-objects>`_ (by default uses the internal LogFormatter).
    :return: A fully configured Python logging `Logger object <https://docs.python.org/2/library/logging.html#logger-objects>`_ you can use with `.debug("msg")`, etc.
    """
    _logger = logging.getLogger(name or __name__)
    _logger.propagate = False
    _logger.setLevel(level)

    # Reconfigure existing handlers
    has_stream_handler = False
    for handler in list(_logger.handlers):
        if isinstance(handler, logging.StreamHandler):
            has_stream_handler = True

        if isinstance(handler, logging.FileHandler) and hasattr(handler, "_is_logzero_internal"):
            # Internal FileHandler needs to be removed and re-setup to be able
            # to set a new logfile.
            _logger.removeHandler(handler)
            continue

        # reconfigure handler
        handler.setLevel(level)
        handler.setFormatter(formatter or LogFormatter())

    if not has_stream_handler:
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(level)
        # formatter = logging.Formatter('%(name)s - %(asctime)-15s - %(levelname)s: %(message)s');
        stream_handler.setFormatter(formatter or LogFormatter())
        _logger.addHandler(stream_handler)

    if logfile:
        filehandler = logging.FileHandler(logfile)
        filehandler._is_logzero_internal = True
        filehandler.setLevel(level)
        filehandler.setFormatter(formatter or LogFormatter(color=False))
        _logger.addHandler(filehandler)

    return _logger


class LogFormatter(logging.Formatter):
    """
    Log formatter used in Tornado. Key features of this formatter are:
    * Color support when logging to a terminal that supports it.
    * Timestamps on every log line.
    * Robust against str/bytes encoding problems.
    """
    DEFAULT_FORMAT = '%(color)s[%(levelname)1.1s %(asctime)s %(module)s:%(lineno)d]%(end_color)s %(message)s'
    DEFAULT_DATE_FORMAT = '%y%m%d %H:%M:%S'
    DEFAULT_COLORS = {
        logging.DEBUG: 4,  # Blue
        logging.INFO: 2,  # Green
        logging.WARNING: 3,  # Yellow
        logging.ERROR: 1,  # Red
    }

    def __init__(self,
                 color=True,
                 fmt=DEFAULT_FORMAT,
                 datefmt=DEFAULT_DATE_FORMAT,
                 colors=DEFAULT_COLORS):
        r"""
        :arg bool color: Enables color support.
        :arg string fmt: Log message format.
          It will be applied to the attributes dict of log records. The
          text between ``%(color)s`` and ``%(end_color)s`` will be colored
          depending on the level if color support is on.
        :arg dict colors: color mappings from logging level to terminal color
          code
        :arg string datefmt: Datetime format.
          Used for formatting ``(asctime)`` placeholder in ``prefix_fmt``.
        .. versionchanged:: 3.2
           Added ``fmt`` and ``datefmt`` arguments.
        """
        logging.Formatter.__init__(self, datefmt=datefmt)

        self._fmt = fmt

        self._colors = {}
        if color and _stderr_supports_color():
            # The curses module has some str/bytes confusion in
            # python3.  Until version 3.2.3, most methods return
            # bytes, but only accept strings.  In addition, we want to
            # output these strings with the logging module, which
            # works with unicode strings.  The explicit calls to
            # unicode() below are harmless in python2 but will do the
            # right conversion in python 3.
            fg_color = (curses.tigetstr("setaf") or curses.tigetstr("setf") or
                        "")
            if (3, 0) < sys.version_info < (3, 2, 3):
                fg_color = unicode_type(fg_color, "ascii")

            for levelno, code in colors.items():
                self._colors[levelno] = unicode_type(
                    curses.tparm(fg_color, code), "ascii")
            self._normal = unicode_type(curses.tigetstr("sgr0"), "ascii")
        else:
            self._normal = ''

    def format(self, record):
        try:
            message = record.getMessage()
            assert isinstance(message,
                              basestring_type)  # guaranteed by logging
            # Encoding notes:  The logging module prefers to work with character
            # strings, but only enforces that log messages are instances of
            # basestring.  In python 2, non-ascii bytestrings will make
            # their way through the logging framework until they blow up with
            # an unhelpful decoding error (with this formatter it happens
            # when we attach the prefix, but there are other opportunities for
            # exceptions further along in the framework).
            #
            # If a byte string makes it this far, convert it to unicode to
            # ensure it will make it out to the logs.  Use repr() as a fallback
            # to ensure that all byte strings can be converted successfully,
            # but don't do it by default so we don't add extra quotes to ascii
            # bytestrings.  This is a bit of a hacky place to do this, but
            # it's worth it since the encoding errors that would otherwise
            # result are so useless (and tornado is fond of using utf8-encoded
            # byte strings whereever possible).
            record.message = _safe_unicode(message)
        except Exception as e:
            record.message = "Bad message (%r): %r" % (e, record.__dict__)

        record.asctime = self.formatTime(record, self.datefmt)

        if record.levelno in self._colors:
            record.color = self._colors[record.levelno]
            record.end_color = self._normal
        else:
            record.color = record.end_color = ''

        formatted = self._fmt % record.__dict__

        if record.exc_info:
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)
        if record.exc_text:
            # exc_text contains multiple lines.  We need to _safe_unicode
            # each line separately so that non-utf8 bytes don't cause
            # all the newlines to turn into '\n'.
            lines = [formatted.rstrip()]
            lines.extend(
                _safe_unicode(ln) for ln in record.exc_text.split('\n'))
            formatted = '\n'.join(lines)
        return formatted.replace("\n", "\n    ")


def _stderr_supports_color():
    color = False
    if curses and hasattr(sys.stderr, 'isatty') and sys.stderr.isatty():
        try:
            curses.setupterm()
            if curses.tigetnum("colors") > 0:
                color = True
        except Exception:
            pass
    return color


_TO_UNICODE_TYPES = (unicode_type, type(None))


def to_unicode(value):
    """
    Converts a string argument to a unicode string.
    If the argument is already a unicode string or None, it is returned
    unchanged.  Otherwise it must be a byte string and is decoded as utf8.
    """
    if isinstance(value, _TO_UNICODE_TYPES):
        return value
    if not isinstance(value, bytes):
        raise TypeError(
            "Expected bytes, unicode, or None; got %r" % type(value))
    return value.decode("utf-8")


def _safe_unicode(s):
    try:
        return to_unicode(s)
    except UnicodeDecodeError:
        return repr(s)


logger = setup_logger(name="_logzero_default")


def setup_default_logger(logfile=None, level=logging.DEBUG, formatter=None):
    """
    Globally reconfigures the default `logzero.logger` instance.

    Usage:

    .. code-block:: python

        from logzero import logger, setup_default_logger
        setup_default_logger(level=logging.WARN)
        logger.info("hello")  # this will not be displayed anymore because minimum loglevel was set to WARN

    :arg string logfile: If set, also write logs to the specified filename.
    :arg int level: Minimum `logging-level <https://docs.python.org/2/library/logging.html#logging-levels>`_ to display (default: `logging.DEBUG`).
    :arg Formatter formatter: `Python logging Formatter object <https://docs.python.org/2/library/logging.html#formatter-objects>`_ (by default uses the internal LogFormatter).
    """
    global logger
    logger = setup_logger(name="_logzero_default", logfile=logfile, level=level, formatter=formatter)
    return logger


if __name__ == "__main__":
    logger = setup_logger()
    logger.info("hello")
