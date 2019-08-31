import time
import sys
from multiprocessing import Manager, get_context

from core.shared.common import info

from ..deployer.start_use_case import run as deployer
from ..gateway.start_use_case import run as gateway


def run():
    active = True

    with Manager() as manager:
        context = get_context("spawn")
        registry = manager.dict()
        registry["app_active"] = True

        try:
            deployer_proc = init_deployer(context, registry)
            gateway_proc = init_gateway(context, registry)
        except:
            info("Exception: {0}".format(sys.exc_info()[0]))
            info("Exiting!")
            registry["app_active"] = False
        finally:
            active = registry["app_active"]
            
        while active:
            time.sleep(1)
            active = registry["app_active"]


def init_deployer(context, registry):
    process = context.Process(target=deployer, args=(registry,))
    process.start()
    info("Deployer worker process started with id: {0}".format(process.pid))
    return process


def init_gateway(context, registry):
    process = context.Process(target=gateway, args=(registry,))
    process.start()
    info("Gateway worker process started with id: {0}".format(process.pid))
    return process



