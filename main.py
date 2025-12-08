import argparse
import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from call_function import available_functions, call_function
from prompts import system_prompt
from fake_gemini import FakeClient
from config import MAX_ITERS


def main():
    call_real_ai()
    # call_fake_ai()
    # debug_fake_ai()


def get_cli_parser():
    parser = argparse.ArgumentParser(description="AI Code Assistant")
    parser.add_argument("user_prompt", type=str, help="Prompt to send to Gemini")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    return args


def debug_fake_ai():
    prompt_text = "how does the calculator render results to the console?"
    messages = [types.Content(role="user", parts=[types.Part(text=prompt_text)])]
    client = FakeClient()
    call_generate_content(client, messages, False)


def call_fake_ai():
    args = get_cli_parser()
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    client = FakeClient()
    if args.verbose:
        print(f"User prompt: {args.user_prompt}\n")
    # call_generate_content(client, messages, args.verbose)
    call_generate_content(client, messages, False)


def call_real_ai():
    args = get_cli_parser()
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable not set")

    client = genai.Client(api_key=api_key)
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    if args.verbose:
        print(f"User prompt: {args.user_prompt}\n")
    call_generate_content(client, messages, args.verbose)


def call_generate_content(client, messages, is_verbose):
    iters = 0
    while True:
        iters += 1
        if iters > MAX_ITERS:
            print(f"Maximum iterations ({MAX_ITERS}) reached.")
            sys.exit(1)
        try:
            final_response = generate_content(client, messages, is_verbose)
            if final_response:
                print(f"Final response:\n{final_response}")
                break

        except Exception as e:
            print(f"Error in generate_content: {e}")


def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )
    if not response.usage_metadata:
        raise RuntimeError("Gemini API response appears to be malformed")

    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    if response.candidates:
        for candidate in response.candidates:
            function_call_content = candidate.content
            messages.append(function_call_content)

    if not response.function_calls:
        return response.text

    function_responses = []

    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, verbose)
        if (
            not function_call_result.parts
            or not function_call_result.parts[0].function_response
        ):
            raise Exception("empty function call result")
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
        function_responses.append(function_call_result.parts[0])

    if not function_responses:
        raise Exception("no function responses generated, exiting.")

    messages.append(types.Content(role="user", parts=function_responses))

    return response


if __name__ == "__main__":
    main()
