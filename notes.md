# AI Agent

Based on the name, actually call the function and capture the result.

    Be sure to manually add the working_directory argument to the dictionary of keyword arguments, because the LLM doesn't control that one. The working directory should be ./calculator.
    The syntax to pass a dictionary into a function using keyword arguments is some_function(**some_args).

I used a dictionary of function name (string) -> function to accomplish this.

## Agents

After you have the responses from each function call, use the types.Content constructor to convert the list of responses into a message with a role of user, and append it to your messages

call_function returns a 'types.Content' object. This has a role 'tool', and a 'parts' array.

I have a list of responses, this is called 'func_call_list'.

From the docs: [genai.types.Content](https://googleapis.github.io/python-genai/genai.html#genai.types.Content)
I can create a new one of these with 'role', set to 'user' in this case, and
'parts', which is a list of genai.types.Part.
