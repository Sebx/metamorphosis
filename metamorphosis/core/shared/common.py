##
# File: core\shared\common.py.
#
# Summary:  Common class.

import logging
import multiprocessing

LOGGER = multiprocessing.get_logger()
LOGGER.setLevel(logging.INFO)
LOGGER.basicConfig(filename="metamorphosis.log",
                   format="Metamorphosis - [%(asctime)s] [%(name)s] [%(levelname)s] %(message)s",
                   level=logging.DEBUG)


def info(message):
    LOGGER.info(message)
    print(message)


def get_logger():
    return LOGGER


class DictWatch(dict):
    def __init__(self, *args, **kwargs):
        self.callback = kwargs.pop("callback")
        dict.__init__(self, args)

    def __setitem__(self, key, val):
        self.callback(key, val)
        dict.__setitem__(self, key, val)
