# AI Agent

Based on the name, actually call the function and capture the result.

    Be sure to manually add the working_directory argument to the dictionary of keyword arguments, because the LLM doesn't control that one. The working directory should be ./calculator.
    The syntax to pass a dictionary into a function using keyword arguments is some_function(**some_args).

I used a dictionary of function name (string) -> function to accomplish this.
