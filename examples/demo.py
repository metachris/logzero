# Import the `logzero.logger` instance
from logzero import logger

# Start logging
logger.debug("hello")
logger.info("info")
logger.warning("warn")
logger.error("error")

# Log exceptions
try:
    raise Exception("this is a demo exception")
except Exception as e:
    logger.exception(e)

# JSON logging
print("\n\nHere starts JSON logging...\n")
import logzero

logzero.json()
logger.info("JSON test")

# Logfile (check with `cat /tmp/logzero-demo.log`)
logzero.logfile("/tmp/logzero-demo.log")
logger.info("going into logfile, in JSON format")

# Disable JSON
logzero.json(False)
logger.info("going into logfile, with standard formatter")
