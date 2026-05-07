import os

def scan_files(directory, blacklist=None):
    if blacklist is None:
        blacklist = ['.git', '__pycache__', '.venv', 'venv']
    
    py_files = []
    
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in blacklist]
        
        for file in files:
            if file.endswith('.py'):
                py_files.append(os.path.join(root, file))
                
    return py_files