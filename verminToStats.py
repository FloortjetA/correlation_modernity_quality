import re
from pathlib import Path
from collections import defaultdict, Counter

input_dir = Path("vermin/vermin_outputs")

stats_dir = Path("vermin/vermin_stats")
stats_dir.mkdir(exist_ok=True)

patterns = [
    r"'([^']+)' module requires (.+)$",
    r"'([^']+)' member requires (.+)$",
    r"([A-Za-z\-]+(?:\([^)]+\))?) requires (.+)$",
    r"(f-strings) require (.+)$",
]

for output_file in input_dir.glob("*_output.txt"):

    file_stats = defaultdict(lambda: defaultdict(Counter))

    current_file = None

    with open(output_file, "r", encoding="latin-1", errors="ignore") as f:
        for line in f:
            line = line.rstrip()

            if "\\python_repos\\" in line:
                match = re.search(r"python_repos\\(.+)$", line)

                if match:
                    current_file = match.group(1)
                    _ = file_stats[current_file]

                continue

            if current_file is None:
                continue

            for pattern in patterns:
                match = re.search(pattern, line)

                if match:
                    feature = match.group(1)
                    requirement = match.group(2)

                    file_stats[current_file][feature][requirement] += 1
                    break

    repo_name = output_file.stem.replace("_output", "")
    stats_file = stats_dir / f"{repo_name}_stats.txt"

    with open(stats_file, "w", encoding="utf-8") as out:

        out.write(f"Feature statistics for repository: {repo_name}\n")
        out.write("=" * 80 + "\n\n")

        for filename in sorted(file_stats):

            out.write(f"FILE: {filename}\n")
            out.write("-" * 80 + "\n")

            if not file_stats[filename]:
                out.write("No modernity features found.\n\n")
                continue

            for feature in sorted(file_stats[filename]):

                total = sum(file_stats[filename][feature].values())

                out.write(f"{feature} (total: {total})\n")

                for requirement, count in (
                    file_stats[filename][feature].most_common()
                ):
                    out.write(f"    {requirement}: {count}\n")

                out.write("\n")

            out.write("\n")

    print(f"Saved statistics to: {stats_file}")

print("Done.")