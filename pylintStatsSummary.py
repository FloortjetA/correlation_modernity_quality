import re
from pathlib import Path
from collections import Counter

input_dir = Path("pylint/repo")

stats_dir = Path("pylint/repo")
stats_dir.mkdir(exist_ok=True)

print("Looking for files in:")
print(input_dir.resolve())

files = list(input_dir.glob("*"))

print(f"Found {len(files)} files")

if not files:
    print("NO FILES FOUND!")
    exit()

message_pattern = re.compile(r":\s*([FEWCR])\d{4}:")
rating_pattern = re.compile(
    r"Your code has been rated at ([0-9]+(?:\.[0-9]+)?)/10"
)

for output_file in files:

    if not output_file.is_file():
        continue

    print(f"\nProcessing: {output_file.name}")

    counter = Counter()
    ratings = []

    with open(output_file, "r", encoding="utf-8", errors="ignore") as f:

        for line in f:

            line = line.strip()

            if ".pylintrc" in line:
                continue

            if "Unknown option value for '--disable'" in line:
                continue

            msg_match = message_pattern.search(line)

            if msg_match:
                counter[msg_match.group(1)] += 1

            rating_match = rating_pattern.search(line)

            if rating_match:
                ratings.append(float(rating_match.group(1)))
                

    total_messages = sum(counter.values())

    avg_rating = (
        sum(ratings) / len(ratings)
        if ratings
        else 0.0
    )

    stats_file = stats_dir / f"{output_file.stem}_stats.txt"

    print(f"Writing: {stats_file}")

    with open(stats_file, "w", encoding="utf-8") as out:

        out.write(f"Statistics for: {output_file.name}\n")
        out.write("=" * 50 + "\n\n")

        out.write("Message counts:\n")
        out.write("-" * 20 + "\n")

        for category in ["F", "E", "W", "C", "R"]:
            out.write(f"{category}: {counter.get(category, 0)}\n")

        out.write("\n")
        out.write(f"Total messages: {total_messages}\n")
        out.write(f"Average rating: {avg_rating:.2f}/10\n")

    print("Done writing file.")

print("\nALL DONE")