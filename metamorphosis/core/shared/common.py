import logging
from os import getpid


logging.basicConfig(format='Metamorphosis - %(message)s', level=logging.DEBUG)

def runs_in_subprocess(process):
    info("Subprocess started with PID {}.".format(getpid()))
    # process()

def info(message):
     logging.info(message)