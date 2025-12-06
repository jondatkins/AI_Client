import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from constants import model_name
from call_function import available_functions


def main():
    if len(sys.argv) < 2:
        print("You need to give me a prompt / question")
        sys.exit(1)
    is_verbose = False
    if "--verbose" in sys.argv[1:]:
        is_verbose = True
    user_prompt = sys.argv[1]
    response = get_response(user_prompt)
    print_info(user_prompt, response, is_verbose)


def get_response(user_prompt):
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable not set")
    client = genai.Client(api_key=api_key)
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    # config=types.GenerateContentConfig(
    #     tools=[available_functions], system_instruction=system_prompt
    # )
    response = client.models.generate_content(
        model=model_name,
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )

    return response


def print_info(user_prompt, response, verbose):
    print(f"User prompt: {user_prompt}")
    if not response.usage_metadata:
        raise RuntimeError("Gemini API response appears to be malformed")
    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    print("Response:")
    if response.function_calls is not None:
        for function_call_part in response.function_calls:
            print(
                f"Calling function: {function_call_part.name}({function_call_part.args})"
            )

    else:
        print(response.text)


if __name__ == "__main__":
    main()
