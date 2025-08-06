from motor.motor_asyncio import AsyncIOMotorClient
from config import settings

client = AsyncIOMotorClient(settings.MONGO_URI)
db = client["github_integration_db"]  
integration_collection = db["github_integration"]
organizations_collection = db["github_organizations"]
repos_collection = db["github_repos"]
commits_collection = db["github_commits"]
pulls_collection = db["github_pulls"]
issues_collection = db["github_issues"]
changelogs_collection = db["github_changelogs"]
users_collection = db["github_users"]
