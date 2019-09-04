##
# Fn:   compile_code(code, app, topics)
#
# Summary:  Compile code.
#
# Author:   Seban.
#
# Date: 4/9/2019.
#
# Parameters:
# code -        The code. 
# app -         The application. 
# topics -      The topics. 

def compile_code(code, app, topics):
    functions = {}
    code_object = compile(code)
    exec(code_object, functions)
    constructor = functions["StatelessFunction"]
    arguments = inspect(constructor)
    parameters = {arg: val for arg, val in topics if arg in arguments}
    if "app" in arguments:
        parameters["app"] = app
    return constructor(**parameters)
