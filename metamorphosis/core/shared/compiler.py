def compile_code(code, app, topics):
    functions = {}
    code_object = compile(code)
    exec(code_object, functions)
    stateless_function_constructor = functions['StatelessFunction']
    arguments = inspect(stateles_function_constructor)
    parameters = {arg: val for arg, val in topics if arg in arguments}
    if 'app' in arguments:
        parameters['app'] = app
    return stateless_function_constructor(**parameters)