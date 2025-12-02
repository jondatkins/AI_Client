import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
import getopt


def main():
    if len(sys.argv) < 2:
        print("You need to give me a prompt / question")
        sys.exit(1)
    is_verbose = False
    if "--verbose" in sys.argv[1:]:
        is_verbose = True
    user_prompt = sys.argv[1]
    response = get_response(user_prompt)
    print_response(response, is_verbose)
    if is_verbose:
        print_verbose_info(user_prompt, response)


def get_response(user_prompt):
    load_dotenv()
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
    )
    return response


def print_response(response, is_verbose):
    print(response.text)


def print_verbose_info(user_prompt, response):
    print(f"User prompt: {user_prompt}")
    if response.usage_metadata is not None:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    else:
        print("No usage_metadata returned")


if __name__ == "__main__":
    main()
