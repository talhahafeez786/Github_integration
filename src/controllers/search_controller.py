from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from helpers.mongodb import (
    users_collection,
    organizations_collection,
    repos_collection,
    commits_collection,
    pulls_collection,
    issues_collection,
    changelogs_collection,
)

from bson import Regex

collections = {
    "github_users": users_collection,
    "github_organizations": organizations_collection,
    "github_repos": repos_collection,
    "github_commits": commits_collection,
    "github_pulls": pulls_collection,
    "github_issues": issues_collection,
    "github_changelogs": changelogs_collection,
}

async def global_search(request: Request, q: str):
    if not q:
        raise HTTPException(status_code=400, detail="Missing 'q' query parameter")

    results = {}
    regex = Regex(f".*{q}.*", "i")  # case-insensitive

    for name, collection in collections.items():
        # Get one document to sample fields
        sample = await collection.find_one()
        if not sample:
            continue

        or_query = []
        for key, value in sample.items():
            if isinstance(value, str):
                or_query.append({key: regex})

        if not or_query:
            continue

        cursor = collection.find({"$or": or_query}).limit(10)
        items = []
        async for doc in cursor:
            doc["_id"] = str(doc["_id"])
            items.append(doc)

        if items:
            results[name] = items

    return JSONResponse(content=results)
