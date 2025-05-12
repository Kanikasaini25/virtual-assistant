import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
# MongoDB Configuration
MONGO_URL = os.getenv("MONGODB_URL")
mongo_client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=5000)
# PostgreSQL Configuration
PG_DB_URL = "postgresql://kanika:kanikasaini@localhost:5432/recipe_db"


# Model Configuration
LLM_MODEL_ID = "gpt-4.1-mini"
PDF_PATH = "Recipe-Book.pdf"
TABLE_NAME = "recipe"
