import argparse
import sys
from rich.console import Console
from rich.markdown import Markdown
from scanner import scan_files
from extractor import extract_info
from analyzer import analyze_project
from builder import build_readme

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("directory")
    parser.add_argument("--name", default="MyPythonProject")
    parser.add_argument("--output", default="README_GENERATED.md")
    args = parser.parse_args()

    console = Console()

    try:
        py_files = scan_files(args.directory)
        
        master_dict = analyze_project(args.name, py_files, extract_info)
        
        readme_content = build_readme(master_dict)
        
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(readme_content)
            
        console.print(Markdown(readme_content))
        
    except Exception as e:
        console.print(f"[bold red]Fatal Error:[/bold red] {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()