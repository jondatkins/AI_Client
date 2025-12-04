import os
from functions.shared_utils import is_dir_inside_dir


def write_file(working_directory, file_path, content):
    full_path = os.path.join(working_directory, file_path)
    if not is_dir_inside_dir(full_path, working_directory):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    try:
        if not os.path.exists(os.path.dirname(full_path)):
            os.makedirs(full_path)
        with open(full_path, "w") as file:
            file.write(content)
    except Exception as e:
        return f"Error: {e}"
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'


# If the file_path is outside the working_directory, return a string with an error:
# f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
