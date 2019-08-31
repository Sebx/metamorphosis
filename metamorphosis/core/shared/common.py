import logging
import multiprocessing

logger = multiprocessing.get_logger()
logger.setLevel(logging.INFO)
logging.basicConfig(filename='metamorphosis.log',
                    format="Metamorphosis - [%(asctime)s] [%(name)s] [%(levelname)s] %(message)s", 
                    level=logging.DEBUG)

def info(message):
    logger.info(message)
    print(message)

def get_logger():
    return logger 

class DictWatch(dict):
    def __init__(self, *args, **kwargs):
        self.callback = kwargs.pop('callback')
        dict.__init__(self, args)

    def __setitem__(self, key, val):
        self.callback(key, val)
        dict.__setitem__(self, key, val)
