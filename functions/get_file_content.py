import os
from configs import MAX_CHAR_LIMIT
from google.genai import types

def get_file_content(working_directory, file_path):
    work_dir_path = os.path.abspath(working_directory)
    path_to_file = os.path.abspath(os.path.join(working_directory, file_path))
    max_char_limit_message = f'[...File "{file_path}" truncated at {MAX_CHAR_LIMIT} characters].'
    
    #if filepath outside working directory return string error
    if not path_to_file.startswith(work_dir_path):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    #if filepath is not a file return string error
    if not os.path.isfile(path_to_file):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    #read the file and return contents as a string see bookbot for reading a file
        #if the file is longer than MAX_CHARS = 10000, truncate the return at 10000 characters and append message
            #[...File "{file_path}" truncated at 10000 characters] to the end
            #Instead of hard coding MAX_CHARS define it in a config.py/constants.py file and import to this
    try:
        with open(path_to_file, "r") as f:
            content = f.read()
            if len(content) > MAX_CHAR_LIMIT:
                truncate_content = content[:MAX_CHAR_LIMIT]
                return truncate_content + max_char_limit_message
            return content
    except Exception as e:
        return f'Error reading file {e}'
    
    #If any errors arise from standardlibrary functions, catch them and return an Error string (see the try: except: system used in get_files_info)
    # directory. Fill this file with at least 20,000 character from the lorem ipsum text. See bootdev link for access
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Opens, reads, and returns the contents of a file constrained to the working directory, if the file contains more than {MAX_CHAR_LIMIT} it truncates the return to 10000 characters.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file, constrained to the working directory, to open and read contents of.",
            ),
        },
        required=["file_path"]
    ),
)