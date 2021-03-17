# Import the `logzero.logger` instance
import logzero
from logzero import logger

logzero.loglevel(logzero.WARNING)

# Start logging
logger.debug("hello")
logger.info("info")
logger.warning("warn")
logger.error("error")
