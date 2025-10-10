import os, subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    abs_path_work_dir = os.path.abspath(working_directory)
    abs_path_file = os. path.abspath(os.path.join(working_directory, file_path))

    if not abs_path_file.startswith(abs_path_work_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(abs_path_file):
        return f'Error: File "{file_path}" not found.'
    
    if not abs_path_file.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    
    try:
        command = ["python", abs_path_file]
        if args:
            command.extend(args)
        
        result = subprocess.run(
            command,
            capture_output=True,
            text= True,
            timeout=30,
            cwd = abs_path_work_dir
            )
        output = []
        
        if result.stdout:
            output.append(f'STDOUT: \n{result.stdout}')
        if result.stderr:
            output.append(f'STDERR: \n{result.stderr}')
        if result.returncode != 0:
            output.append(f'Process exited with code \n{result.returncode}')
        
        return "\n".join(output) if output else "No output produced."

    except Exception as e:
        raise f"Error: executing Python file: {e}"
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file within the working directory and returns the output from the interpreter.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Optional arguments to pass to the Python file.",
                ),
                description="Optional arguments to pass to the Python file.",
            ),
        },
        required=["file_path"],
    ),
)