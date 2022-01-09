# -*- coding: utf-8 -*-
"""
This helper provides a versatile yet easy to use and beautiful logging setup.
You can use it to log to the console and optionally to a logfile. This project
is heavily inspired by the Tornado web framework.

* https://logzero.readthedocs.io
* https://github.com/metachris/logzero

The call `logger.info("hello")` prints log messages in this format:

    [I 170213 15:02:00 test:203] hello

Usage:

    from logzero import logger

    logger.debug("hello")
    logger.info("info")
    logger.warning("warn")
    logger.error("error")

In order to also log to a file, just use `logzero.logfile(..)`:

    logzero.logfile("/tmp/test.log")

If you want to use specific loggers instead of the global default logger, use
`setup_logger(..)`:

    logger = logzero.setup_logger(logfile="/tmp/test.log")

The default loglevel is `DEBUG`. You can set it with the
parameter `level`.

See the documentation for more information: https://logzero.readthedocs.io
"""
import functools
import logging
import os
import sys
from datetime import datetime
from logging import CRITICAL, DEBUG, ERROR, INFO, NOTSET, WARN, WARNING  # noqa: F401
from logging.handlers import RotatingFileHandler, SysLogHandler

from logzero.colors import Fore as ForegroundColors
from logzero.jsonlogger import JsonFormatter
from pathlib import Path

try:
    import curses  # type: ignore
except ImportError:
    curses = None

__author__ = """Chris Hager"""
__email__ = 'chris@linuxuser.at'
__version__ = '1.7.0'

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

# Formatter defaults
DEFAULT_FORMAT = '%(color)s[%(levelname)1.1s %(asctime)s %(module)s:%(lineno)d]%(end_color)s %(message)s'
DEFAULT_DATE_FORMAT = '%y%m%d %H:%M:%S'
DEFAULT_COLORS = {
    DEBUG: ForegroundColors.CYAN,
    INFO: ForegroundColors.GREEN,
    WARNING: ForegroundColors.YELLOW,
    ERROR: ForegroundColors.RED,
    CRITICAL: ForegroundColors.RED
}

# Name of the internal default logger
LOGZERO_DEFAULT_LOGGER = "logzero_default"

# Attribute which all internal loggers carry
LOGZERO_INTERNAL_LOGGER_ATTR = "_is_logzero_internal"

# Attribute signalling whether the handler has a custom loglevel
LOGZERO_INTERNAL_HANDLER_IS_CUSTOM_LOGLEVEL = "_is_logzero_internal_handler_custom_loglevel"

# Logzero default logger
logger = None

# Current state of the internal logging settings
_loglevel = DEBUG
_logfile = None
_formatter = None

# Setup colorama on Windows
if os.name == 'nt':
    from colorama import init as colorama_init
    colorama_init()


def setup_logger(name=__name__, logfile=None, level=DEBUG, formatter=None, maxBytes=0, backupCount=0, fileLoglevel=None, log_stream='stderr', isRootLogger=False, json=False, json_ensure_ascii=False):
    """
    Configures and returns a fully configured logger instance, no hassles.
    If a logger with the specified name already exists, it returns the existing instance,
    else creates a new one.

    If you set the ``logfile`` parameter with a filename, the logger will save the messages to the logfile,
    but does not rotate by default. If you want to enable log rotation, set both ``maxBytes`` and ``backupCount``.

    Usage:

    .. code-block:: python

        from logzero import setup_logger
        logger = setup_logger()
        logger.info("hello")

    :arg string name: Name of the `Logger object <https://docs.python.org/2/library/logging.html#logger-objects>`_. Multiple calls to ``setup_logger()`` with the same name will always return a reference to the same Logger object. (default: ``__name__``)
    :arg string logfile: If set, also write logs to the specified filename.
    :arg int level: Minimum `logging-level <https://docs.python.org/2/library/logging.html#logging-levels>`_ to display (default: ``DEBUG``).
    :arg Formatter formatter: `Python logging Formatter object <https://docs.python.org/2/library/logging.html#formatter-objects>`_ (by default uses the internal LogFormatter).
    :arg int maxBytes: Size of the logfile when rollover should occur. Defaults to 0, rollover never occurs.
    :arg int backupCount: Number of backups to keep. Defaults to 0, rollover never occurs.
    :arg int fileLoglevel: Minimum `logging-level <https://docs.python.org/2/library/logging.html#logging-levels>`_ for the file logger (is not set, it will use the loglevel from the ``level`` argument)
    :arg string log_stream: Which standard stream should the log output go to. Can take values of `stderr`, `stdout` or `None`. Defaults to `stderr`.
    :arg bool isRootLogger: If True then returns a root logger. Defaults to False. (see also the `Python docs <https://docs.python.org/3/library/logging.html#logging.getLogger>`_).
    :arg bool json: If True then log in JSON format. Defaults to False. (uses `python-json-logger <https://github.com/madzak/python-json-logger>`_).
    :arg bool json_ensure_ascii: Passed to json.dumps as `ensure_ascii`, default: False (if False: writes utf-8 characters, if True: ascii only representation of special characters - eg. '\u00d6\u00df')
    :return: A fully configured Python logging `Logger object <https://docs.python.org/2/library/logging.html#logger-objects>`_ you can use with ``.debug("msg")``, etc.
    """
    _logger = logging.getLogger(None if isRootLogger else name)
    _logger.propagate = False

    # set the minimum level needed for the logger itself (the lowest handler level)
    minLevel = fileLoglevel if fileLoglevel and fileLoglevel < level else level
    _logger.setLevel(minLevel)

    # Setup default formatter
    _formatter = _get_json_formatter(json_ensure_ascii) if json else formatter or LogFormatter()

    # Ensure the log stream passed by user is valid.
    if log_stream not in ("stderr", "stdout", None):
        _logger.warning("Log stream must be one of `'stderr'`, `'stdout'` or `None`. Using `'stderr'`")
        log_stream = "stderr"

    # Reconfigure existing handlers
    std_stream_handler = None
    for handler in list(_logger.handlers):
        if hasattr(handler, LOGZERO_INTERNAL_LOGGER_ATTR):
            if isinstance(handler, logging.FileHandler):
                # Internal FileHandler needs to be removed and re-setup to be able
                # to set a new logfile.
                _logger.removeHandler(handler)
                continue
            elif isinstance(handler, logging.StreamHandler):
                if log_stream is None or (std_stream_handler and log_stream not in std_stream_handler.stream.name):
                    # remove the std handler (stream_handler) if disabled, or if there is a stream(err/out) mismatch
                    _logger.removeHandler(handler)
                    continue
                else:
                    # Else, this is the stderr/stdout stream that we need to reconfigure
                    std_stream_handler = handler

        # reconfigure handler
        handler.setLevel(level)
        handler.setFormatter(_formatter)

    if log_stream is not None and std_stream_handler is None:
        # This is the block that will be entered for the default logger (ex: `from logzero import logger`)
        std_stream_handler = logging.StreamHandler(stream=getattr(sys, log_stream))
        setattr(std_stream_handler, LOGZERO_INTERNAL_LOGGER_ATTR, True)
        std_stream_handler.setLevel(level)
        std_stream_handler.setFormatter(_formatter)
        _logger.addHandler(std_stream_handler)

    if logfile:
        # Create the folder for holding the logfile, if it doesn't already exist
        Path(logfile).parent.mkdir(parents=True, exist_ok=True)
        
        rotating_filehandler = RotatingFileHandler(filename=logfile, maxBytes=maxBytes, backupCount=backupCount)
        setattr(rotating_filehandler, LOGZERO_INTERNAL_LOGGER_ATTR, True)
        rotating_filehandler.setLevel(fileLoglevel or level)
        rotating_filehandler.setFormatter(_formatter)
        _logger.addHandler(rotating_filehandler)

    return _logger


class LogFormatter(logging.Formatter):
    """
    Log formatter used in Tornado. Key features of this formatter are:
    * Color support when logging to a terminal that supports it.
    * Timestamps on every log line.
    * Robust against str/bytes encoding problems.
    """
    def __init__(self,
                 color=True,
                 fmt=DEFAULT_FORMAT,
                 datefmt=DEFAULT_DATE_FORMAT,
                 colors=DEFAULT_COLORS,
                 syslog_levels=False):
        r"""
        :arg bool color: Enables color support.
        :arg string fmt: Log message format.
          It will be applied to the attributes dict of log records. The
          text between ``%(color)s`` and ``%(end_color)s`` will be colored
          depending on the level if color support is on.
        :arg string datefmt: Datetime format.
          Used for formatting ``(asctime)`` placeholder in ``prefix_fmt``.
        :arg dict colors: color mappings from logging level to terminal color
          code
        :arg bool syslog_levels: Whether to log in the syslog severity level schema.
        .. versionchanged:: 3.2
           Added ``fmt`` and ``datefmt`` arguments.
        """
        logging.Formatter.__init__(self, datefmt=datefmt)

        self._fmt = fmt
        self._syslog_levels = syslog_levels
        self._colors = {}
        self._normal = ''

        if color and _stderr_supports_color():
            self._colors = colors
            self._normal = ForegroundColors.RESET

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
            # byte strings wherever possible).
            record.message = _safe_unicode(message)
        except Exception as e:
            record.message = "Bad message (%r): %r" % (e, record.__dict__)

        record.asctime = self.formatTime(record, self.datefmt)

        if record.levelno in self._colors:
            record.color = self._colors[record.levelno]
            record.end_color = self._normal
        else:
            record.color = record.end_color = ''

        if self._syslog_levels:
            record = self._convert_to_syslog_severity_level(record)

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

    def _convert_to_syslog_severity_level(self, record: logging.LogRecord):
        """
        Borrowed from https://github.com/Azure-Samples/iotedge-logging-and-monitoring-solution/blob/2bd90e21ffe1394bdbb38f8932cbc78c8c836aa1/EdgeSolution/modules/PythonSampleLogs/CustomLogger.py.

        Convert pythong logging log levels to syslog standard. You can compare both using the following links:
        https://en.wikipedia.org/wiki/Syslog#Severity_level
        https://docs.python.org/3/howto/logging.html#logging-levels
        """
        if record.levelno == logging.DEBUG:
            record.levelno = 7
            record.levelname = "DBG"
        if record.levelno == logging.INFO:
            record.levelno = 6
            record.levelname = "INF"
        if record.levelno == logging.WARNING:
            record.levelno = 4
            record.levelname = "WRN"
        if record.levelno == logging.ERROR:
            record.levelno = 3
            record.levelname = "ERR"
        if record.levelno == logging.CRITICAL:
            record.levelno = 2
            record.levelname = "CRIT"

        return record

    def formatTime(self, record, datefmt=None, timespec="milliseconds"):
        if datefmt in ("iso", "azure"):
            dt = datetime.fromtimestamp(record.created, tz=datetime.now().astimezone().tzinfo)
            s = dt.isoformat(" ", timespec=timespec)
            if datefmt == "azure":
                s = s.replace("+", " +")
        else:
            s = super().formatTime(record, datefmt)
        return s


def _stderr_supports_color():
    # Colors can be forced with an env variable
    if os.getenv('LOGZERO_FORCE_COLOR') == '1':
        return True

    # Windows supports colors with colorama
    if os.name == 'nt':
        return True

    # Detect color support of stderr with curses (Linux/macOS)
    if curses and hasattr(sys.stderr, 'isatty') and sys.stderr.isatty():
        try:
            curses.setupterm()
            if curses.tigetnum("colors") > 0:
                return True

        except Exception:
            pass

    return False


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


def setup_default_logger(logfile=None, level=DEBUG, formatter=None, maxBytes=0, backupCount=0, log_stream='stderr'):
    """
    Deprecated. Use `logzero.loglevel(..)`, `logzero.logfile(..)`, etc.

    Globally reconfigures the default `logzero.logger` instance.

    Usage:

    .. code-block:: python

        from logzero import logger, setup_default_logger
        setup_default_logger(level=WARN)
        logger.info("hello")  # this will not be displayed anymore because minimum loglevel was set to WARN

    :arg string logfile: If set, also write logs to the specified filename.
    :arg int level: Minimum `logging-level <https://docs.python.org/2/library/logging.html#logging-levels>`_ to display (default: `DEBUG`).
    :arg Formatter formatter: `Python logging Formatter object <https://docs.python.org/2/library/logging.html#formatter-objects>`_ (by default uses the internal LogFormatter).
    :arg int maxBytes: Size of the logfile when rollover should occur. Defaults to 0, rollover never occurs.
    :arg int backupCount: Number of backups to keep. Defaults to 0, rollover never occurs.
    :arg string log_stream: Which standard stream should the log output go to. Can take values of `stderr`, `stdout` or `None`. Defaults to `stderr`.
    """
    global logger
    logger = setup_logger(name=LOGZERO_DEFAULT_LOGGER, logfile=logfile, level=level, formatter=formatter, backupCount=backupCount, log_stream=log_stream)
    return logger


def reset_default_logger():
    """
    Resets the internal default logger to the initial configuration
    """
    global logger
    global _loglevel
    global _logfile
    global _formatter
    _loglevel = DEBUG
    _logfile = None
    _formatter = None

    # Remove all handlers on exiting logger
    if logger:
        for handler in list(logger.handlers):
            logger.removeHandler(handler)

    # Resetup
    logger = setup_logger(name=LOGZERO_DEFAULT_LOGGER, logfile=_logfile, level=_loglevel, formatter=_formatter)


def loglevel(level=DEBUG, update_custom_handlers=False):
    """
    Set the minimum loglevel for the default logger (`logzero.logger`) and all handlers.

    This reconfigures only the internal handlers of the default logger (eg. stream and logfile).
    You can also update the loglevel for custom handlers by using `update_custom_handlers=True`.

    :arg int level: Minimum `logging-level <https://docs.python.org/2/library/logging.html#logging-levels>`_ to display (default: `DEBUG`).
    :arg bool update_custom_handlers: If you added custom handlers to this logger and want this to update them too, you need to set `update_custom_handlers` to `True`
    """
    logger.setLevel(level)

    # Reconfigure existing internal handlers
    for handler in list(logger.handlers):
        if hasattr(handler, LOGZERO_INTERNAL_LOGGER_ATTR) or update_custom_handlers:
            # Don't update the loglevel if this handler uses a custom one
            if hasattr(handler, LOGZERO_INTERNAL_HANDLER_IS_CUSTOM_LOGLEVEL):
                continue

            # Update the loglevel for all default handlers
            handler.setLevel(level)

    global _loglevel
    _loglevel = level


def formatter(formatter, update_custom_handlers=False):
    """
    Set the formatter for all handlers of the default logger (``logzero.logger``).

    This reconfigures only the logzero internal handlers by default, but you can also
    reconfigure custom handlers by using ``update_custom_handlers=True``.

    Beware that setting a formatter which uses colors also may write the color codes
    to logfiles.

    :arg Formatter formatter: `Python logging Formatter object <https://docs.python.org/2/library/logging.html#formatter-objects>`_ (by default uses the internal LogFormatter).
    :arg bool update_custom_handlers: If you added custom handlers to this logger and want this to update them too, you need to set ``update_custom_handlers`` to `True`
    """
    for handler in list(logger.handlers):
        if hasattr(handler, LOGZERO_INTERNAL_LOGGER_ATTR) or update_custom_handlers:
            handler.setFormatter(formatter)

    global _formatter
    _formatter = formatter


def logfile(filename, formatter=None, mode='a', maxBytes=0, backupCount=0, encoding=None, loglevel=None, disable_stream_loggers=False):
    """
    Setup logging to file (using a `RotatingFileHandler <https://docs.python.org/2/library/logging.handlers.html#rotatingfilehandler>`_ internally).

    By default, the file grows indefinitely (no rotation). You can use the ``maxBytes`` and
    ``backupCount`` values to allow the file to rollover at a predetermined size. When the
    size is about to be exceeded, the file is closed and a new file is silently opened
    for output. Rollover occurs whenever the current log file is nearly ``maxBytes`` in length;
    if either of ``maxBytes`` or ``backupCount`` is zero, rollover never occurs.

    If ``backupCount`` is non-zero, the system will save old log files by appending the
    extensions ‘.1’, ‘.2’ etc., to the filename. For example, with a ``backupCount`` of 5
    and a base file name of app.log, you would get app.log, app.log.1, app.log.2, up to
    app.log.5. The file being written to is always app.log. When this file is filled,
    it is closed and renamed to app.log.1, and if files app.log.1, app.log.2, etc. exist,
    then they are renamed to app.log.2, app.log.3 etc. respectively.

    :arg string filename: Filename of the logfile. Set to `None` to disable logging to the logfile.
    :arg Formatter formatter: `Python logging Formatter object <https://docs.python.org/2/library/logging.html#formatter-objects>`_ (by default uses the internal LogFormatter).
    :arg string mode: mode to open the file with. Defaults to ``a``
    :arg int maxBytes: Size of the logfile when rollover should occur. Defaults to 0, rollover never occurs.
    :arg int backupCount: Number of backups to keep. Defaults to 0, rollover never occurs.
    :arg string encoding: Used to open the file with that encoding.
    :arg int loglevel: Set a custom loglevel for the file logger, else uses the current global loglevel.
    :arg bool disable_stream_loggers: should the default stream loggers(stderr/stdout) be disabled? defaults to `True`
    """
    # First, remove any existing file logger
    __remove_internal_loggers(logger, disable_stream_loggers)

    # If no filename supplied, all is done
    if not filename:
        return

    # Create the folder for holding the logfile, if it doesn't already exist
    Path(filename).parent.mkdir(parents=True, exist_ok=True)

    # Now add
    rotating_filehandler = RotatingFileHandler(filename, mode=mode, maxBytes=maxBytes, backupCount=backupCount, encoding=encoding)

    # Set internal attributes on this handler
    setattr(rotating_filehandler, LOGZERO_INTERNAL_LOGGER_ATTR, True)
    if loglevel:
        setattr(rotating_filehandler, LOGZERO_INTERNAL_HANDLER_IS_CUSTOM_LOGLEVEL, True)

    # Configure the handler and add it to the logger
    rotating_filehandler.setLevel(loglevel or _loglevel)
    rotating_filehandler.setFormatter(formatter or _formatter or LogFormatter(color=False))
    logger.addHandler(rotating_filehandler)

    # If wanting to use a lower loglevel for the file handler, we need to reconfigure the logger level
    # (note: this won't change the StreamHandler loglevel)
    if loglevel and loglevel < logger.level:
        logger.setLevel(loglevel)


def __remove_internal_loggers(logger_to_update, disable_stream_loggers=True):
    """
    Remove the internal loggers (e.g. stderr/stdout logger and file logger) from the specific logger
    :param logger_to_update: the logger to remove internal loggers from
    :param disable_stream_loggers: should the default stream loggers(stderr/stdout) be disabled? defaults to `True`
    """
    for handler in list(logger_to_update.handlers):
        if hasattr(handler, LOGZERO_INTERNAL_LOGGER_ATTR):
            if isinstance(handler, RotatingFileHandler):
                logger_to_update.removeHandler(handler)
            elif isinstance(handler, SysLogHandler):
                logger_to_update.removeHandler(handler)
            elif isinstance(handler, logging.StreamHandler) and disable_stream_loggers:
                logger_to_update.removeHandler(handler)


def syslog(logger_to_update=logger, facility=SysLogHandler.LOG_USER, disable_stream_loggers=True):
    """
    Setup logging to syslog and disable other internal loggers
    :param logger_to_update: the logger to enable syslog logging for
    :param facility: syslog facility to log to
    :param disable_stream_loggers: should the default stream loggers(stderr/stdout) be disabled? defaults to `True`
    :return the new SysLogHandler, which can be modified externally (e.g. for custom log level)
    """
    # remove internal loggers
    __remove_internal_loggers(logger_to_update, disable_stream_loggers)

    # Setup logzero to only use the syslog handler with the specified facility
    syslog_handler = SysLogHandler(facility=facility)
    setattr(syslog_handler, LOGZERO_INTERNAL_LOGGER_ATTR, True)
    logger_to_update.addHandler(syslog_handler)
    return syslog_handler


def json(enable=True, json_ensure_ascii=False, update_custom_handlers=False):
    """
    Enable/disable json logging for all handlers.

    Params:
    * json_ensure_ascii ... Passed to json.dumps as `ensure_ascii`, default: False (if False: writes utf-8 characters, if True: ascii only representation of special characters - eg. '\u00d6\u00df')
    """

    formatter(_get_json_formatter(json_ensure_ascii) if enable else LogFormatter(), update_custom_handlers=update_custom_handlers)


def _get_json_formatter(json_ensure_ascii):
    supported_keys = [
        'asctime',
        'filename',
        'funcName',
        'levelname',
        'levelno',
        'lineno',
        'module',
        'message',
        'name',
        'pathname',
        'process',
        'processName',
        'threadName'
    ]

    def log_format(x):
        return ['%({0:s})s'.format(i) for i in x]
    custom_format = ' '.join(log_format(supported_keys))
    return JsonFormatter(custom_format, json_ensure_ascii=json_ensure_ascii)


def log_function_call(func):
    @functools.wraps(func)
    def wrap(*args, **kwargs):
        args_str = ", ".join([str(arg) for arg in args])
        kwargs_str = ", ".join(["%s=%s" % (key, kwargs[key]) for key in kwargs])
        if args_str and kwargs_str:
            all_args_str = ", ".join([args_str, kwargs_str])
        else:
            all_args_str = args_str or kwargs_str
        logger.debug("%s(%s)", func.__name__, all_args_str)
        return func(*args, **kwargs)
    return wrap


# Initially setup the default logger
reset_default_logger()

if __name__ == "__main__":
    _logger = setup_logger()
    _logger.info("hello")
