import re

filename = "pylint\erpnext\erpnext_pylint_stats.txt"

ratings = []

with open(filename, "r", encoding="utf-8") as f:
    for line in f:
        match = re.search(r"Average rating:\s*([0-9.]+)/10", line)
        if match:
            ratings.append(float(match.group(1)))

if ratings:
    avg_rating = sum(ratings) / len(ratings)
    print(f"Found {len(ratings)} ratings")
    print(f"Overall average rating: {avg_rating:.2f}/10")
else:
    print("No ratings found.")