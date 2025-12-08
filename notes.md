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

## Expected Output

(aiagent) wagslane@MacBook-Pro-2 aiagent % uv run main.py "how does the calculator render results to the console?"

- Calling function: get_files_info
- Calling function: get_file_content
Final response:
Alright, I've examined the code in `main.py`. Here's how the calculator renders results to the console:

- **`print(to_print)`:** The core of the output is done using the `print()` function.
- **`format_json_output(expression, result)`:** Before printing, the `format_json_output` function (imported from `pkg.render`) is used to format the result and the original expression into a JSON-like string. This formatted string is then stored in the `to_print` variable.
- **Error handling:** The code includes error handling with `try...except` blocks. If there's an error during the calculation (e.g., invalid expression), an error message is printed to the console using `print(f"Error: {e}")`.

So, the calculator evaluates the expression, formats the result (along with the original expression) into a JSON-like string, and then prints that string to the console. It also prints error messages to the console if any errors occur.
