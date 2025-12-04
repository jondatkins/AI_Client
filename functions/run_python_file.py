import os
from shared_utils import is_dir_inside_dir


def run_python_file(working_directory, file_path, args=[]):
    full_path = os.path.join(working_directory, file_path)
    if not is_dir_inside_dir(full_path, working_directory):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(full_path):
        return f'Error: File "{file_path}" not found.'
    _, ext = os.path.splitext(full_path)
    if not ext == ".py":
        f'Error: "{file_path}" is not a Python file.'
