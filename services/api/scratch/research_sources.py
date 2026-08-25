import urllib.request
import json
import time

def check_github_repo(repo):
    url = f"https://api.github.com/repos/{repo}"
    req = urllib.request.Request(url, headers={"User-Agent": "Bhoomi-Researcher"})
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode())
            lic = data.get("license")
            lic_spdx = lic.get("spdx_id") if lic else "None"
            desc = data.get("description", "")
            print(f"Repo: {repo} | License: {lic_spdx} | Desc: {desc[:60]}...")
            return data
    except Exception as e:
        print(f"Repo {repo} error: {e}")
        return None

def search_github_repos(query):
    url = f"https://api.github.com/search/repositories?q={urllib.parse.quote(query)}&sort=stars&order=desc"
    req = urllib.request.Request(url, headers={"User-Agent": "Bhoomi-Researcher"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            print(f"\n--- Search results for '{query}' (Total: {data.get('total_count')}) ---")
            for item in data.get("items", [])[:8]:
                full_name = item.get("full_name")
                lic = item.get("license")
                lic_name = lic.get("spdx_id") if lic else "None"
                stars = item.get("stargazers_count")
                desc = item.get("description") or ""
                print(f"  * {full_name} ({stars} stars) [License: {lic_name}]: {desc[:70]}")
    except Exception as e:
        print(f"Search error for {query}: {e}")

import urllib.parse
search_github_repos("rice pest disease dataset")
search_github_repos("rice leaf disease dataset")
search_github_repos("paddy pest dataset")
