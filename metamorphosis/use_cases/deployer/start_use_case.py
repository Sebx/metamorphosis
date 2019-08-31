import os
import time
from multiprocessing import Manager, get_context

from core.shared.common import info
from core.shared.consumer import Consumer

broker_consumer = Consumer()


def run(registry):
    active = True

    while active:
        registry["deployer_active"] = True
        time.sleep(1)
        broker_consumer.start()
        info("Worker process id: {0}".format(os.getpid()))
        active = registry["deployer_active"]


@broker_consumer.handle("siumlj60-default")
def receive_message(message):
    info("msg: {0}".format(message))
