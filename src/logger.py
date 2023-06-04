import logging
import sys

logger = logging.getLogger()

logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter(
    '%(asctime)s - [%(levelname)s] - %(message)s - %(funcName)s - '
    'строка %(lineno)d'
)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
