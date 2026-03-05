import subprocess
import os
import re

def execute(path, interactive=False, program_args=None):
    cmd, script_type = build_command(path)

    if program_args:
        cmd.extend(program_args)

    if interactive:
        proc = subprocess.Popen(cmd)

    proc = subprocess.Popen(
        cmd, 
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    return proc, script_type

def build_command(path):
    ext = os.path.splitext(path)[1]

    if ext == ".py":
        return ["python3", path], "python"
    
    elif ext == ".sh":
        return ["bash", path], "bash"

    elif ext == ".cpp":
        base = os.path.splitext(path)[0]
        exe = base
        compile_result = subprocess.run(
            ["g++", path, "-o", exe],
            capture_output=True,
            text=True
        )

        if compile_result.returncode != 0:
            raise RuntimeError(f"Compilation failed!: \n{compile_result.stderr}")
        
        return [exe], "cpp"
    
    elif os.access(path, os.X_OK):
        return [path], "binary"
    
    else:
        raise ValueError("Unsupported at this time")
    