import os

def analyze_project(project_name, file_paths, extract_func):
    master_dict = {
        "project_name": project_name,
        "total_files": len(file_paths),
        "total_lines": 0,
        "total_functions": 0,
        "total_classes": 0,
        "files": []
    }
    
    for path in file_paths:
        try:
            raw_data = extract_func(path)
            funcs = raw_data.get("functions", [])
            classes = raw_data.get("classes", [])
            
            funcs.sort(key=lambda x: (x["name"].startswith("_"), -x.get("complexity", 0)))
            
            master_dict["total_lines"] += raw_data.get("total_lines", 0)
            master_dict["total_functions"] += len(funcs)
            master_dict["total_classes"] += len(classes)
            
            file_info = {
                "file_name": os.path.basename(path),
                "path": path,
                "module_docstring": raw_data.get("module_docstring", ""),
                "total_lines": raw_data.get("total_lines", 0),
                "classes": classes,
                "functions": funcs,
                "imports": list(set(raw_data.get("imports", [])))
            }
            master_dict["files"].append(file_info)
            
        except Exception:
            continue
            
    return master_dict