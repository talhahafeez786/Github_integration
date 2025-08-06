import httpx
from helpers.mongodb import (
    integration_collection,
    organizations_collection,
    repos_collection,
    commits_collection,
    pulls_collection,
    issues_collection,
    changelogs_collection,
    users_collection,
)

GITHUB_API_BASE = "https://api.github.com"

async def get_auth_token():
    user = await integration_collection.find_one()
    return user["token"] if user else None

async def fetch_from_github(endpoint, token):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{GITHUB_API_BASE}{endpoint}",
            headers={"Authorization": f"token {token}"}
        )
        response.raise_for_status()
        return response.json()

async def fetch_and_store_repo_data(repo, token):
    owner = repo["owner"]["login"]
    repo_name = repo["name"]

    # Commits
    try:
        commits = await fetch_from_github(f"/repos/{owner}/{repo_name}/commits", token)
        if commits:
            await commits_collection.insert_many(commits)
    except Exception as e:
        print(f"Skipping commits for {repo_name}: {e}")

    # Pull requests
    try:
        pulls = await fetch_from_github(f"/repos/{owner}/{repo_name}/pulls", token)
        if pulls:
            await pulls_collection.insert_many(pulls)
    except Exception as e:
        print(f"Skipping pulls for {repo_name}: {e}")

    # Issues
    try:
        issues = await fetch_from_github(f"/repos/{owner}/{repo_name}/issues", token)
        if issues:
            await issues_collection.insert_many(issues)
    except Exception as e:
        print(f"Skipping issues for {repo_name}: {e}")

    # Changelogs (issue events)
    try:
        changelogs = await fetch_from_github(f"/repos/{owner}/{repo_name}/issues/events", token)
        if changelogs:
            await changelogs_collection.insert_many(changelogs)
    except Exception as e:
        print(f"Skipping changelogs for {repo_name}: {e}")

async def sync_github_data():
    token = await get_auth_token()
    if not token:
        return {"error": "No token found"}

    # 1. Fetch user info
    try:
        user = await fetch_from_github("/user", token)
        await users_collection.delete_many({})
        await users_collection.insert_one(user)
    except Exception as e:
        return {"error": f"Failed to fetch user info: {str(e)}"}

    # 2. Fetch personal repositories
    try:
        user_repos = await fetch_from_github("/user/repos", token)
        await repos_collection.delete_many({})
        if user_repos:
            await repos_collection.insert_many(user_repos)
        else:
            print("No personal repositories found.")
    except Exception as e:
        print(f"Error fetching personal repos: {e}")
        user_repos = []

    for repo in user_repos:
        await fetch_and_store_repo_data(repo, token)

    # 3. Fetch organizations
    try:
        orgs = await fetch_from_github("/user/orgs", token)
        if orgs:
            await organizations_collection.delete_many({})
            await organizations_collection.insert_many(orgs)
        else:
            print("User does not belong to any organization.")
    except Exception as e:
        print(f"Error fetching organizations: {e}")
        orgs = []

    # 4. Fetch data for each organization
    for org in orgs:
        org_login = org["login"]

        # Get org repos
        try:
            org_repos = await fetch_from_github(f"/orgs/{org_login}/repos", token)
            if org_repos:
                await repos_collection.insert_many(org_repos)
        except Exception as e:
            print(f"Skipping org repos for {org_login}: {e}")
            continue

        for repo in org_repos:
            await fetch_and_store_repo_data(repo, token)

        # Get org members
        try:
            members = await fetch_from_github(f"/orgs/{org_login}/members", token)
            if members:
                await users_collection.insert_many(members)
        except Exception as e:
            print(f"Skipping org members for {org_login}: {e}")

    return {"message": "Sync complete (personal + orgs)"}
