def analyze(stdout, stderr, exit_code):
    if exit_code != 0:
        return "Failure"
    
    combined = (stdout + stderr).lower()

    if "warning" in combined:
        return "Warning"
    
    return "Success!"