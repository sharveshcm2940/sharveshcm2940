"""Fetch contribution calendar + top repos for USER into data/*.json (stdlib only)."""
import os, json, urllib.request

USER = os.environ.get("GH_USER", "sharveshcm2940")
TOKEN = os.environ["GH_TOKEN"]
H = {"Authorization": f"bearer {TOKEN}", "User-Agent": "readme-cards"}

q = """query($u:String!){user(login:$u){contributionsCollection{contributionCalendar{
totalContributions weeks{contributionDays{date contributionCount}}}}}}"""
req = urllib.request.Request("https://api.github.com/graphql",
    data=json.dumps({"query": q, "variables": {"u": USER}}).encode(), headers=H)
cal = json.load(urllib.request.urlopen(req))["data"]["user"]["contributionsCollection"]["contributionCalendar"]
days = [{"date": d["date"], "count": d["contributionCount"]}
        for w in cal["weeks"] for d in w["contributionDays"]]

req = urllib.request.Request(f"https://api.github.com/users/{USER}/repos?per_page=100&sort=pushed", headers=H)
repos = [r for r in json.load(urllib.request.urlopen(req)) if not r["fork"]]
repos = [{"name": r["name"], "desc": r["description"] or "", "lang": r["language"] or "",
          "stars": r["stargazers_count"], "forks": r["forks_count"], "url": r["html_url"]} for r in repos]

os.makedirs("data", exist_ok=True)
json.dump({"total": cal["totalContributions"], "days": days}, open("data/contributions.json", "w"))
json.dump(repos, open("data/repos.json", "w"))
print(f"{len(days)} days, {len(repos)} repos")
