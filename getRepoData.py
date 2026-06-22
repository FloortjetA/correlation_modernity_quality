import requests
import time
import subprocess
import os

TOKEN = "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"
HEADERS = {"Authorization": f"token {TOKEN}"}

BASE_DIR = "./python_repos"
os.makedirs(BASE_DIR, exist_ok=True)

def search_repos(query, page):
    url = "https://api.github.com/search/repositories"
    params = {
        "q": query,
        "per_page": 100,
        "page": page
    }
    
    r = requests.get(url, headers=HEADERS, params=params)
    
    if r.status_code != 200:
        print("Error:", r.json())
        return {"items": []}
    
    return r.json()

def is_active(repo_full_name):
    url = f"https://api.github.com/repos/{repo_full_name}/stats/commit_activity"
    
    for _ in range(3):
        r = requests.get(url, headers=HEADERS)
        
        if r.status_code == 202:
            time.sleep(2)
            continue
        
        if r.status_code != 200:
            return False
        
        data = r.json()
        if not data:
            return False
        
        total_commits = sum(week["total"] for week in data[-52:])
        return total_commits >= 10 
    
    return False

def is_suspicious(repo):
    if repo["stargazers_count"] < 20:
        return True
    if repo["fork"]:
        return True
    if not repo["description"]:
        return True
    return False

def clone_repo(repo):
    url = repo["clone_url"]
    name = repo["name"]
    path = os.path.join(BASE_DIR, name)

    if not os.path.exists(path):
        subprocess.run(["git", "clone", url, path])

query = "language:Python created:<2018-04-20 pushed:>2025-04-20"

for page in range(1, 11):  
    data = search_repos(query, page)

    for repo in data.get("items", []):
        full_name = repo["full_name"]

        if is_active(full_name) and (not is_suspicious(repo)):
            clone_repo(repo)

    time.sleep(2) 