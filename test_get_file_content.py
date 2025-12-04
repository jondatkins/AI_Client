from functions.get_files_content import get_file_content

lorem = get_file_content("calculator", "lorem.txt")
print(lorem)
print(get_file_content("calculator", "main.py"))
print(get_file_content("calculator", "pkg/calculator.py"))
print(get_file_content("calculator", "/bin/cat"))
print(get_file_content("calculator", "pkg/does_not_exist.py"))
