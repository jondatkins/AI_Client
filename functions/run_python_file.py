import os
import subprocess
from functions.shared_utils import is_dir_inside_dir
from google.genai import types


def run_python_file(working_directory, file_path, args=[]):
    full_path = os.path.join(working_directory, file_path)
    if not is_dir_inside_dir(full_path, working_directory):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(full_path):
        return f'Error: File "{file_path}" not found.'
    _, ext = os.path.splitext(full_path)
    if not ext == ".py":
        return f'Error: "{file_path}" is not a Python file.'
    try:
        result = subprocess.run(
            ["python", file_path] + args,
            timeout=30,
            capture_output=True,
            check=True,
            cwd=working_directory,
        )
        comp_proc_obj = result
    except Exception as e:
        return f"Error: executing Python file: {e}"

    return_string = f"STDOUT: {comp_proc_obj.stdout} STDERR: {comp_proc_obj.stderr}"
    if not comp_proc_obj.returncode == 0:
        return_string = (
            f"{return_string} Process exited with code {comp_proc_obj.returncode}"
        )
    return return_string


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execue python file at given path, using the optional args",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file": types.Schema(
                type=types.Type.STRING,
                # description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
                description="The python file to execute, relative to the working directory.",
            ),
        },
    ),
)
