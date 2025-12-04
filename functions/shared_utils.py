import os


def is_dir_inside_dir(working_directory, container_dir):
    working_directory = os.path.abspath(working_directory)
    # if not os.path.isdir(working_directory):
    #     return False
    if container_dir in working_directory:
        return True
    return False
