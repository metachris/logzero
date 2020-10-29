History
=======

1.6.0 (2020-10-29)
------------------

-   JSON logging support ([PR 344][])
-   Ability to easily change colors ([\#82][])
-   Allow creating a root logger ([\#342][])
-   Bugfix: file logging with lower loglevel than stream ([PR 338][])
-   Running tests with Python up to 3.9
-   Dependency updates

1.5.0 (2018-03-07)
------------------

-   `logzero.syslog(..)` ([PR 83][])

1.4.0 (2018-03-02)
------------------

-   Allow Disabling stderr Output ([PR 83][1])

1.3.0 (2017-07-19)
------------------

-   Color output now works in Windows (supported by colorama)

1.2.1 (2017-07-09)
------------------

-   Logfiles with custom loglevels (eg. stream handler with DEBUG and
    file handler with ERROR).

1.2.0 (2017-07-05)
------------------

-   Way better API for configuring the default logger with <span
    class="title-ref">logzero.loglevel(..)</span>, <span
    class="title-ref">logzero.logfile(..)</span>, etc.
-   Built-in rotating logfile support.

``` python
import logging
import logzero
from logzero import logger

# This log message goes to the console
logger.debug("hello")

# Set a minimum log level
logzero.loglevel(logging.INFO)

# Set a logfile (all future log messages are also saved there)
logzero.logfile("/tmp/logfile.log")

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

1.1.2 (2017-07-04)
------------------

-   Better reconfiguration of handlers, doesn't remove custom handlers
    anymore

1.1.0 (2017-07-03)
------------------

-   Bugfix: Disabled color logging to logfile

1.1.0 (2017-07-02)
------------------

-   Global default logger instance (<span
    class="title-ref">logzero.logger</span>)
-   Ability to reconfigure the default logger with (<span
    class="title-ref">logzero.setup\_default\_logger(..)</span>)
-   More tests
-   More documentation

1.0.0 (2017-06-27)
------------------

-   Cleanup and documentation

0.2.0 (2017-06-12)
------------------

-   Working logzero package with code and tests

0.1.0 (2017-06-12)
------------------

-   First release on PyPI.

  [PR 344]: https://github.com/metachris/logzero/pull/344
  [\#82]: https://github.com/metachris/logzero/issues/82
  [\#342]: https://github.com/metachris/logzero/pull/342
  [PR 338]: https://github.com/metachris/logzero/pull/338
  [PR 83]: https://github.com/metachris/logzero/pull/84
  [1]: https://github.com/metachris/logzero/pull/83
