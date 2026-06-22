import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from pathlib import Path
import re
import numpy as np
from pathlib import PureWindowsPath
from pathlib import Path
import re
import ast

fig = plt.figure()
file_name = "salt"
color_dots = "darkblue"
import re
from pathlib import Path

python_feature_release = {
    "3.15": 26,
    "3.14": 25,
    "3.13": 24,
    "3.12": 23,
    "3.11": 22,
    "3.10": 21,
    "3.9": 20,
    "3.8": 19,
    "3.7": 18,
    "3.6": 16,
    "3.5": 15,
    "3.4": 14,
    "3.3": 12,
    "3.2": 11,
    "3.1": 9,
    "3.0": 8,
    "2.7": 10,
    "2.6": 8,
}

def getAxisCodeQuality(inputFile):
    stats_file = Path(inputFile)
    with open(f"linesOfCode\\{file_name}_line_counts.txt", "r", encoding="utf-8") as f:
        loc_dict = ast.literal_eval(f.read())
    ratings = {}
    total_non_zero_loc_files = sum(1 for loc in loc_dict.values() if loc != 0)
    print(f"Total files with non-zero LOC: {total_non_zero_loc_files}")
            
    current_file = None
    with open(stats_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            file_match = re.match(r"FILE:\s+(.+)", line)
            if file_match:
                current_file = file_match.group(1)
                continue
            rating_match = re.match(
                r"Average rating:\s+([0-9]+(?:\.[0-9]+)?)/10",
                line
            )

            if rating_match and current_file is not None:
                if loc_dict.get(current_file) == 0:
                    continue

                rating = float(rating_match.group(1))
                ratings[current_file] = rating
    return ratings

def versionToWeight(version_string):

    parts = [p.strip() for p in version_string.split(",")]

    if len(parts) >= 2:
        version = parts[1]
    else:
        version = parts[0]

    version = version.lstrip("!")

    return python_feature_release.get(version, 0.0)

def getNormalizedModernityFeatures(filePath):

    results = {}

    current_file = None
    weighted_sum = 0.0
    has_features = False
    loc_dict = {}

    with open(f"linesOfCode\\{file_name}_line_counts.txt", "r", encoding="utf-8") as f:
        loc_dict = ast.literal_eval(f.read())

    def save_current_file(current_file, weighted_sum, has_features):

        if current_file is None:
            return

        if not has_features:
            return

        filename = current_file.split('\\', 1)[1]

        loc = loc_dict.get(filename)

        if loc is None:
            return

        if loc == 0:
            return

        normalized_score = weighted_sum / (loc / 1000)

        results[filename] = normalized_score

    with open(filePath, "r", encoding="utf-8") as f:

        for raw_line in f:

            line = raw_line.strip()

            if line.startswith("FILE: "):

                save_current_file(
                    current_file,
                    weighted_sum,
                    has_features
                )

                current_file = line[len("FILE: "):]
                weighted_sum = 0.0
                has_features = False

                continue

            if line.startswith(("!2", "!3", "2.", "3.")):

                version_match = re.match(
                    r"(.+?):\s*(\d+)$",
                    line
                )

                if version_match:

                    has_features = True

                    version_string = version_match.group(1).strip()
                    count = int(version_match.group(2))

                    weight = versionToWeight(version_string)

                    weighted_sum += weight * count

        save_current_file(
            current_file,
            weighted_sum,
            has_features
        )

    return results

codeQuality = getAxisCodeQuality(f"pylint\\{file_name}\\{file_name}_pylint_stats.txt")
codeNormalizedModernizationFeatures = getNormalizedModernityFeatures(f"vermin\\vermin_stats\\{file_name}_stats.txt")
codeQuality = {k: v for k, v in codeQuality.items() if k in codeNormalizedModernizationFeatures} 
codeNormalizedModernizationFeatures = {k: v for k, v in codeNormalizedModernizationFeatures.items() if k in codeQuality}       
x = list(codeQuality.values())
y = list(codeNormalizedModernizationFeatures.values())
plt.scatter(x, y, s=50, c=color_dots, alpha=0.7)
plt.title('Code Quality vs Normalized Modernization Features')
plt.xlabel('Code Quality (Pylint Average Rating out of 10)')
plt.ylabel('Modernization Features (weighted features per KLOC)')
plt.show()
for file in list(codeNormalizedModernizationFeatures.keys()):
    if codeNormalizedModernizationFeatures.get(file)> 4000:
        print(file)

from scipy.stats import pearsonr, spearmanr
print(type(codeQuality.values()))
print(type(codeNormalizedModernizationFeatures.values()))
pearson_corr, pearson_p = pearsonr(x, y)
spearman_corr, spearman_p = spearmanr(x, y)

print("Spearman:", spearman_corr, spearman_p)