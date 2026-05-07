import ast

class InfoExtractor(ast.NodeVisitor):
    def __init__(self):
        self.data = {"classes": [], "functions": [], "imports": []}

    def visit_Import(self, node):
        for alias in node.names:
            self.data["imports"].append(alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        if node.module:
            self.data["imports"].append(node.module)
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
        docstring = ast.get_docstring(node)
        self.data["classes"].append({
            "name": node.name,
            "methods": methods,
            "docstring": docstring if docstring else ""
        })
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        args = [a.arg for a in node.args.args]
        docstring = ast.get_docstring(node)
        line_count = getattr(node, 'end_lineno', node.lineno) - node.lineno + 1
        
        complexity = sum(1 for child in ast.walk(node) if isinstance(child, (ast.If, ast.For, ast.While, ast.Try)))
        
        self.data["functions"].append({
            "name": node.name,
            "args": args,
            "line_count": line_count,
            "docstring": docstring if docstring else "",
            "complexity": complexity
        })
        self.generic_visit(node)

def extract_info(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    tree = ast.parse(content)
    extractor = InfoExtractor()
    extractor.visit(tree)
    
    extractor.data["module_docstring"] = ast.get_docstring(tree) or ""
    extractor.data["total_lines"] = len(content.splitlines())
    
    return extractor.data