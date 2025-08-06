import os 
from dotenv import load_dotenv

load_dotenv()

class settings:
    GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
    GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
    REDIRECT_URI = os.getenv("REDIRECT_URI")
    MONGO_URI = os.getenv("MONGO_URI")
    
    
settings = settings()
