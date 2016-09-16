import functools
import logging
import inspect
import json
import os


def json_parse(func):
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        response = func(*args, **kwargs)
        return json.loads(response.read())
    return wrapped

#############################################################################
# Setup logging
#############################################################################
LOGS_DIR = os.environ.get('LOGS_DIR', './')
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s %(filename)s:'
                    '%(lineno)d -- %(message)s',
                    filename=os.path.join(LOGS_DIR, 'sys_test.log'),
                    filemode='w')

console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s %(filename)s:'
                              '%(lineno)d -- %(message)s')
console.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.addHandler(console)


def debug(logger):
    def wrapper(func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            logger.debug(
                "Calling: {} with args: {} {}".format(
                    func.__name__, args, kwargs
                )
            )
            result = func(*args, **kwargs)
            logger.debug(
                "Done: {} with result: {}".format(func.__name__, result))
            return result
        return wrapped
    return wrapper

logwrap = debug(logger)

