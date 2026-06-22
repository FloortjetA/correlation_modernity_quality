import os
import subprocess
from pathlib import Path

repos_root = Path("python_repos")

output_root = Path("vermin/vermin_outputs")
output_root.mkdir(exist_ok=True)

for repo in repos_root.iterdir():
    if repo.is_dir():

        repo_name = repo.name
        output_file = output_root / f"{repo_name}_output.txt"

        print(f"Running vermin on: {repo_name}")

        command = f'vermin -vvv "{repo}"'

        with open(output_file, "w", encoding="utf-8") as out:

            subprocess.run(
                command,
                shell=True,
                stdout=out,
                stderr=subprocess.STDOUT,
                text=True
            )

        print(f"Saved output to: {output_file}")

print("Done.")