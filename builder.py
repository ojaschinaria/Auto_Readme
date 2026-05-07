import os

def generate_tree(files, project_name):
    tree = "## 🗂️ Project Architecture\n\n```text\n"
    tree += f"📦 {project_name}\n"
    
    paths = sorted([f["path"] for f in files])
    
    for p in paths:
        filename = os.path.basename(p)
        tree += f"└── 📜 {filename}\n"
        
    tree += "```\n\n"
    return tree

def generate_toc(files):
    toc = "## 📑 Table of Contents\n"
    for f in files:
        anchor = f['file_name'].replace('.', '').lower()
        toc += f"* [{f['file_name']}](#-{''.join(e for e in anchor if e.isalnum())})\n"
    return toc + "\n"

def build_readme(master_dict):
    max_comp = 0
    for f in master_dict["files"]:
        for fn in f.get("functions", []):
            max_comp = max(max_comp, fn.get("complexity", 0))

    md = f"# 📊 {master_dict['project_name']}\n\n"
    
    md += f"![Total Files](https://img.shields.io/badge/Files-{master_dict['total_files']}-blue) "
    md += f"![Total Lines](https://img.shields.io/badge/Lines-{master_dict['total_lines']}-success) "
    md += f"![Classes](https://img.shields.io/badge/Classes-{master_dict['total_classes']}-yellow) "
    md += f"![Functions](https://img.shields.io/badge/Functions-{master_dict['total_functions']}-orange) "
    md += f"![Max Complexity](https://img.shields.io/badge/Max_Complexity-{max_comp}-red)\n\n"
    
    md += "## 🚀 About\n"
    md += "> *Write a brief 1-2 sentence description of your project here.*\n\n"
    
    md += "## ⚙️ Quick Start\n"
    md += "```bash\npython main.py\n```\n\n"
    md += "---\n\n"
    
    md += generate_tree(master_dict["files"], master_dict['project_name'])
    md += "---\n\n"
    md += generate_toc(master_dict["files"])
    md += "---\n\n"
    
    md += "## 🔍 File Reference\n\n"
    for f in master_dict["files"]:
        md += f"### 📄 {f['file_name']}\n"
        
        clean_path = f['path'].replace('\\', '/')
        md += f"**Location:** `./{clean_path}` | **Total Lines:** `{f['total_lines']}`\n\n"
        
        if f.get("module_docstring"):
            clean_mod_doc = f['module_docstring'].replace('\n', ' ')
            md += f"> {clean_mod_doc}\n\n"
        
        if f.get("imports"):
            formatted_imports = [f"`{imp}`" for imp in sorted(f['imports'])]
            md += f"**Dependencies:** {', '.join(formatted_imports)}\n\n"
        
        if f.get("classes"):
            md += "#### 🧩 Classes\n\n"
            md += "| Class Name | Methods Available | Description |\n| :--- | :--- | :--- |\n"
            for c in f["classes"]:
                methods = ", ".join([f"`{m}`" for m in c["methods"]]) if c["methods"] else "*None*"
                doc = c['docstring'].replace('\n', ' ') if c['docstring'] else "*No description provided.*"
                md += f"| **`{c['name']}`** | {methods} | {doc} |\n"
            md += "\n"
            
        if f.get("functions"):
            md += "#### ⚙️ Functions\n\n"
            md += "| Function Name | Arguments | Lines | Complexity | Purpose |\n| :--- | :--- | :--- | :--- | :--- |\n"
            for fn in f["functions"]:
                args = ", ".join([f"`{a}`" for a in fn["args"]]) if fn["args"] else "*None*"
                doc = fn['docstring'].replace('\n', ' ') if fn['docstring'] else "*No description provided.*"
                md += f"| **`{fn['name']}`** | {args} | {fn['line_count']} | {fn.get('complexity', 0)} | {doc} |\n"
            md += "\n"
            
    return md