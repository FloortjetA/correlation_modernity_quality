from pathlib import Path

file_name = "scikit-learn"
repo_path = f"python_repos\\{file_name}"

def get_python_file_line_counts(repo_path):
    """
    Returns a dictionary mapping Python file paths to their line counts.
    """
    repo_path = Path(repo_path)

    line_counts = {}

    for file in repo_path.rglob("*"):
        if file.suffix in {".py", ".pyi"}:
            try:
                with file.open("r", encoding="utf-8") as f:
                    line_count = sum(1 for _ in f)

                relative_path = str(file.relative_to(repo_path))
                line_counts[relative_path] = line_count

            except Exception as e:
                print(f"Could not process {file}: {e}")

    return line_counts

def write_to_file(filename, content):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content + "\n")

file_line_counts = get_python_file_line_counts(repo_path)
mkfile = Path(f"linesOfCode\\{file_name}_line_counts.txt")
write_to_file(f"linesOfCode\\{file_name}_line_counts.txt", str(file_line_counts))
print("ALL DONE")
        
