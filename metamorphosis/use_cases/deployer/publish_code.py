##
# File: use_cases\deployer\publish_code.py.
#
# Summary:  Publish code class.

import os
import time

from metamorphosis.core.shared.common import info


def run(registry):
    registry["deployer_active"] = True
    time.sleep(1)
    info("Worker process id: {0}".format(os.getpid()))

    try:
        pass
        # create_stateless_function(received.value["sourcecode"], app)
    except Empty:
        return False

    return True


def create_stateless_function(source_code, app, topicDict):
    functions = {}
    code_object = compile(source_code)
    exec(code_object, functions)
    stateless_function_constructor = functions["StatelessFunction"]
    arguments = inspect(stateles_function_constructor)
    parameters = {arg: val for arg, val in topicDict if arg in arguments}
    if "app" in arguments:
        parameters["app"] = app
    return stateless_function_constructor(**parameters)
