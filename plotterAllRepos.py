import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from pathlib import Path
import re
import numpy as np
from pathlib import Path
import re

fig = plt.figure()
ouliers = {
    8.39 : 98.34271514169454, # erpnext
    8.27 : 315.2351413259099 # frappe
    }
locPerRepo = {
    "aiohttp": 91742,
    "airflow": 1349685,
    "angr": 288394,
    "ansible": 142939,
    "aws-cli": 113515,
    "awx": 159644,
    "beets": 81315,
    "calibre": 510921,
    "ccxt": 822328,
    "celery": 99302,
    "certbot": 74960,
    "cupy": 217328,
    "django": 516893,
    "django-cms": 71791,
    "electrum": 142654,
    # "erpnext": 330782,
    "espnet": 351309,
    # "frappe": 182486,
    "freqtrade": 139903,
    "great_expectations": 2697,
    "hypothesis": 100267,
    "ipython": 84789,
    "jumpserver": 103024,
    "keras": 308516,
    "kitty": 81762,
    "kivy": 119631,
    "lutris": 70829,
    "matplotlib": 289749,
    "mitmproxy": 89663,
    "moto": 782246,
    "mypy": 259472,
    "netbox": 323579,
    "nltk": 144253,
    "Nuitka": 514057,
    "numba": 309296,
    "numpy": 320074,
    "OctoPrint": 101381,
    "odoo": 1162650,
    "optuna": 68747,
    "pandas": 667640,
    "Pillow": 75876,
    "pip": 173255,
    "pymc": 100989,
    "pytest": 105993,
    "pytorch": 2410090,
    "qutebrowser": 116635,
    "ray": 1194993,
    "readthedocs.org": 134378,
    "robotframework": 111273,
    "saleor": 830556,
    "salt": 887491,
    "scikit-learn": 437211,
    "scipy": 587456,
    "scrapy": 78451,
    "sentry": 1541935,
    "spaCy": 138211,
    "spyder": 260853,
    "sqlmap": 81320,
    "statsmodels": 452660,
    "sympy": 793291,
    "wagtail": 244227,
    "xonsh": 96172,
    "youtube-dl": 169575,
    "zulip": 190335,
}

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

sortedReposByContributors = {
"hundreds": ["aiohttp", "angr", "aws-cli", "awx", "beets", 
    "calibre", "ccxt", "certbot", "cupy", "django-cms", "electrum", 
    "espnet", "frappe", "freqtrade", "great_expectations", 
    "hypothesis", "jumpserver", "kitty", "kivy", 
    "lutris", "mitmproxy", "moto", "mypy", "netbox", 
    "nltk", "Nuitka", "numba", "OctoPrint", "optuna", 
    "Pillow", "pip", "pymc", "qutebrowser", 
    "readthedocs.org", "robotframework", "saleor", 
    "scrapy", "spaCy", "spyder", "sqlmap", "statsmodels", 
    "wagtail", "xonsh", "youtube-dl"], # hundreds of contributors
"thousands": ["airflow", "ansible", "celery", "django", 
    "erpnext", "ipython", "keras", "matplotlib", "numpy", 
    "odoo", "pandas", "pytest", "pytorch", "ray", 
    "salt", "scikit-learn", "scipy", "sentry", 
    "sympy", "zulip"] # thousands of contributors
}

def getAxisCodeQuality(inputDir, locPerRepo, reposIncluded=None):

    stats_dir = Path(inputDir)

    results = {}

    stats_files = sorted(stats_dir.glob("*_stats.txt"))

    for stats_file in stats_files:

        if reposIncluded and stats_file.stem.replace("_pylint_stats", "") not in reposIncluded:
            continue
        repo_name = stats_file.stem.replace("_pylint_stats", "")

        if repo_name not in locPerRepo:
            print(f"Skipping {repo_name}: no LOC entry found")
            continue

        ratings = []

        with open(stats_file, "r", encoding="utf-8") as f:

            for line in f:

                line = line.strip()

                match = re.match(
                    r"Average rating:\s+([0-9]+(?:\.[0-9]+)?)/10",
                    line
                )

                if match:

                    rating = float(match.group(1))
                    ratings.append(rating)

        if not ratings:
            print(f"Skipping {repo_name}: no ratings found")
            continue

        average_rating = sum(ratings) / len(ratings)

        results[repo_name] = average_rating

    return results

def versionToWeight(version_string):

    parts = [p.strip() for p in version_string.split(",")]

    if len(parts) >= 2:
        version = parts[1]
    else:
        version = parts[0]

    version = version.lstrip("!")

    return python_feature_release.get(version, 0.0)


def getNormalizedModernityFeatures(
    stats_dir,
    loc_dict,
    reposIncluded
):

    stats_dir = Path(stats_dir)

    results = {}

    stats_files = sorted(stats_dir.glob("*_stats.txt"))

    for stats_file in stats_files:

        repo_name = stats_file.stem.replace("_stats", "")

        if repo_name not in loc_dict:
            print(f"Skipping {repo_name}: no LOC info")
            continue

        if repo_name not in reposIncluded:
            print(f"Skipping {repo_name}: not in included repos")
            continue

        weighted_sum = 0.0

        with open(stats_file, "r", encoding="utf-8") as f:

            current_feature_count = None

            for line in f:

                line = line.strip()

                feature_match = re.match(
                    r".+\(total:\s*(\d+)\)",
                    line
                )

                if feature_match:
                    current_feature_count = int(
                        feature_match.group(1)
                    )
                    continue

                version_match = re.match(
                    r"(.+?):\s*(\d+)",
                    line
                )

                if version_match:

                    version_string = version_match.group(1).strip()
                    count = int(version_match.group(2))

                    weight = versionToWeight(version_string)

                    weighted_sum += weight * count

        loc = loc_dict[repo_name]

        if loc == 0:
            print(f"Skipping {repo_name}: LOC is 0")
            continue

        normalized_score = weighted_sum / (loc / 1000)

        results[repo_name] = normalized_score

    return results
codeQuality = getAxisCodeQuality("pylint/pylint_stats", locPerRepo, sortedReposByContributors["thousands"]+sortedReposByContributors["hundreds"])
codeNormalizedModernizationFeatures = getNormalizedModernityFeatures("vermin/vermin_stats", locPerRepo, sortedReposByContributors["thousands"]+sortedReposByContributors["hundreds"])
x = list(codeQuality.values())
y = list(codeNormalizedModernizationFeatures.values())
fixed_frappe_x = list(ouliers.keys())[1]
fixed_frappe_y = list(ouliers.values())[1]
fixed_erpnext_x = list(ouliers.keys())[0]
fixed_erpnext_y = list(ouliers.values())[0]
print("Code Quality:", codeQuality.values())
print("Normalized Modernization Features:", codeNormalizedModernizationFeatures.values())
plt.scatter(
    fixed_frappe_x, fixed_frappe_y,
    s=50, c='pink', alpha=1,
    edgecolors='darkred',
    label='frappe'
)

plt.scatter(
    fixed_erpnext_x, fixed_erpnext_y,
    s=50, c='lightgreen', alpha=1,
    edgecolors='darkgreen',
    label='erpnext'
)

plt.scatter(x, y, s=50, c='darkblue', alpha=0.7, label='Other projects')

plt.xlabel('Code Quality (Pylint Average Rating out of 10)')
plt.ylabel('Modernization Features (weighted features per KLOC)')
plt.legend()
plt.show()

from scipy.stats import pearsonr, spearmanr

pearson_corr, pearson_p = pearsonr(list(codeQuality.values()), list(codeNormalizedModernizationFeatures.values()))
spearman_corr, spearman_p = spearmanr(list(codeQuality.values()), list(codeNormalizedModernizationFeatures.values()))

print("Spearman:", spearman_corr, spearman_p)