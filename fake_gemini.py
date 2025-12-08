from unittest.mock import MagicMock
from types import SimpleNamespace


def make_fake_response(
    with_function_call=True,
    text="This is fake text output",
):
    global counter
    counter += 1
    response_1 = "get_files_info"
    response_2 = "get_file_content"
    response_3 = """
Alright, I've examined the code in `main.py`. Here's how the calculator renders results to the console:

- **`print(to_print)`:** The core of the output is done using the `print()` function.
- **`format_json_output(expression, result)`:** Before printing, the `format_json_output` function (imported from `pkg.render`) is used to format the result and the original expression into a JSON-like string. This formatted string is then stored in the `to_print` variable.
- **Error handling:** The code includes error handling with `try...except` blocks. If there's an error during the calculation (e.g., invalid expression), an error message is printed to the console using `print(f"Error: {e}")`.

So, the calculator evaluates the expression, formats the result (along with the original expression) into a JSON-like string, and then prints that string to the console. It also prints error messages to the console if any errors occur.
"""
    func_name = ""
    func_args = {}
    if counter == 1:
        func_name = response_1
    if counter == 2:
        func_name = response_2
        func_args = {"file_path": "main.py"}
    if counter == 3:
        func_name = ""
    # ---- MOCK USAGE METADATA ----
    usage_metadata = SimpleNamespace(
        prompt_token_count=42,
        candidates_token_count=17,
    )

    # ---- MOCK NORMAL TEXT OUTPUT ----
    fake_text = text

    # ---- MOCK FUNCTION CALLS ----
    if with_function_call:
        fake_function_call = SimpleNamespace(
            name=func_name,
            # args={"value": 123},
            # args={"file_path": "main.py"},
            args=func_args,
        )
        function_calls = [fake_function_call]
    else:
        function_calls = []

    # ---- MOCK CANDIDATES ----
    fake_candidate = SimpleNamespace(
        content=func_name,
        finish_reason="stop",
    )
    candidates = [fake_candidate]

    # ---- BUILD RESPONSE ----
    resp = MagicMock()
    resp.usage_metadata = usage_metadata
    resp.text = fake_text
    resp.function_calls = function_calls
    resp.candidates = candidates

    return resp


counter = 0


class FakeModels:
    def generate_content(self, model, contents, config):
        # You can toggle whether a function call happens:
        if counter < 3:
            return make_fake_response(with_function_call=True)
        else:
            return make_fake_response(with_function_call=False)


class FakeClient:
    models = FakeModels()
