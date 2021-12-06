import logging
from sys import stdout


logger = logging.getLogger('api-logger')

logger.setLevel(logging.DEBUG)
logFormatter = logging.Formatter("%(levelname)-5s: %(asctime)-20s: %(message)s")
consoleHandler = logging.StreamHandler(stdout)
consoleHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)
