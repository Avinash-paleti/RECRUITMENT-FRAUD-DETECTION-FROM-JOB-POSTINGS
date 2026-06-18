from pymongo import MongoClient
import os

# ---------- CONFIGURATION ----------

# Local MongoDB (default)
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")

DB_NAME = "fraudshield_db"

# ---------- CONNECTION ----------

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

# ---------- COLLECTIONS ----------

users_col = db["users"]          # Stores registered users
predictions_col = db["predictions"]  # Stores prediction results

# ---------- OPTIONAL: INDEXES ----------

users_col.create_index("username", unique=True)
predictions_col.create_index("created_at")