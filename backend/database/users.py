
import json
import os



USER_DB_PATH = "users.json"
# Helper to load users from JSON
def load_users():
    if not os.path.exists(USER_DB_PATH):
        return []
    with open(USER_DB_PATH, "r") as f:
        return json.load(f)

# Helper to save users to JSON
def save_users(users):
    with open(USER_DB_PATH, "w") as f:
        json.dump(users, f, indent=2)