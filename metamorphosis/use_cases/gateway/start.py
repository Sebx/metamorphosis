##
# File: use_cases\gateway\start.py.
#
# Summary:  Start class.

import os
import time
from metamorphosis.core.shared.common import info
from multiprocessing import Manager, get_context

def run(registry):
    active = True
    
    while active:
        registry["gateway_active"] = True
        time.sleep(1)
        info("Worker process id: {0}".format(os.getpid()))
        active = registry["gateway_active"]
