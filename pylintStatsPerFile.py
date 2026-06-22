import ast
import re
from pathlib import Path
from collections import Counter

repo_name = "scikit-learn"
file_name = f"{repo_name}_pylint"
loc_file = f"linesOfCode\\{repo_name}_line_counts.txt"

with open(
    loc_file,
    "r",
    encoding="utf-8",
) as f:
    loc_dict = ast.literal_eval(f.read())

input_file = Path(
    f"pylint/outliers/output/{file_name}.txt"
)

stats_dir = Path(f"pylint/{repo_name}")
stats_dir.mkdir(exist_ok=True)

message_pattern = re.compile(
    r"^(.*?):\d+(?::\d+)?:\s*([FEWCR])\d{4}:"
)

rating_pattern = re.compile(
    r"Your code has been rated at\s+([-+]?\d+(?:\.\d+)?)/10"
)

file_counters = {}
file_ratings = {}

current_file = None
current_counter = Counter()

with open(input_file, "r", encoding="utf-8", errors="ignore") as f:
    for raw_line in f:
        line = raw_line.strip()
        if ".pylintrc" in line:
            continue

        if "Unknown option value for '--disable'" in line:
            continue

        if line.startswith(
            f"FILE: "
        ):
            current_file = line[6:].strip().split(
                f"{repo_name}\\", 1
            )[-1]

            if loc_dict.get(current_file, 0) == 0:
                current_file = None
                current_counter = Counter()
                continue

            print(f"Processing file: {current_file}")

            current_counter = Counter()
            continue

        if current_file is None:
            continue

        msg_match = message_pattern.match(line)

        if msg_match:
            category = msg_match.group(2)
            current_counter[category] += 1
            continue

        rating_match = rating_pattern.search(line)

        if rating_match:
            rating = float(rating_match.group(1))
            file_counters[current_file] = current_counter.copy()
            file_ratings[current_file] = rating

            current_file = None
            current_counter = Counter()

print(
    "Files without ratings:",
    set(file_counters.keys()) - set(file_ratings.keys())
)
print("Counters:", len(file_counters))
print("Ratings:", len(file_ratings))

stats_file = stats_dir / f"{input_file.stem}_stats.txt"

print(f"Writing: {stats_file}")

with open(stats_file, "w", encoding="utf-8") as out:
    out.write(
        f"Statistics for: {input_file.name}\n"
    )
    out.write("=" * 80 + "\n\n")

    all_files = sorted(file_ratings.keys())

    ratings = []

    for filepath in all_files:
        counter = file_counters.get(
            filepath,
            Counter()
        )

        total_messages = sum(counter.values())

        rating = file_ratings[filepath]
        ratings.append(rating)

        out.write(f"FILE: {filepath}\n")
        out.write("-" * 80 + "\n")

        for category in ["F", "E", "W", "C", "R"]:
            out.write(
                f"{category}: "
                f"{counter.get(category, 0)}\n"
            )

        out.write(
            f"Total messages: "
            f"{total_messages}\n"
        )

        out.write(
            f"Average rating: "
            f"{rating:.2f}/10\n\n"
        )

    overall_avg = (
        sum(ratings) / len(ratings)
        if ratings
        else 0.0
    )

    out.write("=" * 80 + "\n")
    out.write(
        f"Overall average rating: "
        f"{overall_avg:.2f}/10\n"
    )

print("Done writing file.")
print("ALL DONE")