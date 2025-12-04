import os
from functions.shared_utils import is_dir_inside_dir


def main():
    pass


# The directory parameter should be treated as a relative path within the
# working_directory. Use os.path.join(working_directory, directory) to
# create the full path, then validate that it falls under the working directory.
def get_files_info(working_directory, directory="."):
    # working_directory = os.path.abspath(working_directory)
    full_path = os.path.join(working_directory, directory)
    if not os.path.isdir(full_path):
        return f'Error: "{full_path}" is not a directory'
    if not is_dir_inside_dir(full_path, working_directory):
        return f'Error: Cannot list "{full_path}" as it is outside the permitted working directory'
    if directory.startswith(".."):
        return f'Error: Cannot list "{full_path}" as it is outside the permitted working directory'
    files_list = os.listdir(full_path)
    markdown_info = []
    dir_name = "current" if directory == "." else f"'{directory}'"
    result_for_dir = f"Result for {dir_name} directory:"
    markdown_info.append(result_for_dir)
    for file in files_list:
        file_path = os.path.join(full_path, file)
        file_size = os.path.getsize(file_path)
        file_string = f"  - {file}: file_size={file_size} bytes, is_dir={not os.path.isfile(file_path)}"
        markdown_info.append(file_string)

    dir_contents = "\n".join(markdown_info)
    return dir_contents


# def is_dir_inside_dir(working_directory, container_dir):
#     working_directory = os.path.abspath(working_directory)
#     if not os.path.isdir(working_directory):
#         return False
#     if container_dir in working_directory:
#         return True
#     return False
#

main()
