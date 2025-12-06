from google.genai import types


def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    function_name = function_call_part.name
    function_args = function_call_part.args

    # Based on the name, actually call the function and capture the result.
    # Be sure to manually add the working_directory argument to the dictionary of keyword arguments, because the LLM doesn't control that one. The working directory should be ./calculator.
    # The syntax to pass a dictionary into a function using keyword arguments is some_function(**some_args).
    function_result = function_name(function_args)
    print(function_result)
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )
