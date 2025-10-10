import os
from google import genai
from google.genai import types

def get_files_info(working_directory, directory="."):
    abs_working_path = os.path.abspath(working_directory)
    target_path = os.path.abspath(os.path.join(working_directory, directory))
    if not target_path.startswith(abs_working_path):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(target_path):
        return f'Error: "{directory}" is not a directory'

    try:
        output_lst = []
        for item in os.listdir(target_path):
            #This is required for the item_size and item_is_dir variable expressions, if you pass item instead of the item's path you will get an error.
            item_path = os.path.join(target_path, item)
            item_size = os.path.getsize(item_path)
            item_is_dir =  os.path.isdir(item_path)
            output_lst.append(
                f"- {item}: file_size={item_size} bytes, is_dir={item_is_dir}"
            )    
        return "\n".join(output_lst)      
    except Exception as e:
        return f"Error listing files: {e}"

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)