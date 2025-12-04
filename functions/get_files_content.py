import os
from config import MAX_CHARS
from functions.shared_utils import is_dir_inside_dir


# If the file_path is outside the working_directory, return a string with an error:
# f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
# If the file_path is not a file, again, return an error string:
#  f'Error: File not found or is not a regular file: "{file_path}"'
def get_file_content(working_directory, file_path):
    try:
        working_directory = os.path.abspath(working_directory)
        full_path = os.path.join(working_directory, file_path)
    except Exception as e:
        return f"Error:{e}"
    if not is_dir_inside_dir(full_path, working_directory):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(full_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    with open(full_path, "r") as f:
        # file_content_string = f.read(MAX_CHARS)
        file_content_string = f.read()
        if len(file_content_string) > 10000:
            # truncate_message = f'[...File "{file_path}" truncated at 10000 characters]'
            file_content_string = f'{file_content_string[0:1000]}[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return file_content_string


# def is_dir_inside_dir(inside_dir, container_dir):
#     # if not os.path.isdir(inside_dir):
#     #     return False
#     if container_dir in inside_dir:
#         return True
#     return False
