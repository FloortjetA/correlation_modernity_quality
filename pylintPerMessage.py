import subprocess
from pathlib import Path

repos_root = Path("pylint/mypyoutlier")

output_root = Path("pylint/outliers/output/mistake")
output_root.mkdir(exist_ok=True)

SKIP_DIRS = {
    "venv",
    ".venv",
    "__pycache__",
    "node_modules",
    "build",
    "dist",
    ".git"
}

for repo in repos_root.iterdir():

    if not repo.is_dir():
        continue

    repo_name = repo.name
    output_file = output_root / f"{repo_name}_pylint.txt"

    print(f"\nScanning repository: {repo_name}")

    with open(output_file, "w", encoding="utf-8") as out:

        out.write(f"Repository: {repo_name}\n")
        out.write("=" * 80 + "\n\n")

        py_files = []

        for py_file in repo.rglob("*.py"):

            if any(part in SKIP_DIRS for part in py_file.parts):
                continue

            py_files.append(py_file)

        print(f"Found {len(py_files)} Python files")

        for i, py_file in enumerate(py_files, start=1):

            print(f"[{i}/{len(py_files)}] {py_file}")

            command = f'pylint "{py_file}" --jobs=1'

            try:
                result = subprocess.run(
                    command,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=120
                )

                out.write("\n")
                out.write("=" * 80 + "\n")
                out.write(f"FILE: {py_file}\n")
                out.write("=" * 80 + "\n")
                out.write(result.stdout)

                if result.stderr:
                    out.write(result.stderr)

            except subprocess.TimeoutExpired:
                out.write(f"\nTIMEOUT on file: {py_file}\n")

            except Exception as e:
                out.write(f"\nERROR on file: {py_file}\n")
                out.write(str(e) + "\n")

    print(f"Saved results to: {output_file}")

print("\nDone.")