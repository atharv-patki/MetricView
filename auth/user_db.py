import json
import os

USER_DB_FILE = "auth/users.json"

# Create user function
def create_user(email, password):
    users = {}
    if os.path.exists(USER_DB_FILE):
        with open(USER_DB_FILE, "r") as f:
            try:
                users = json.load(f)
                # If it's in old format (string), convert to dict
                for key in list(users):
                    if isinstance(users[key], str):
                        users[key] = {"password": users[key]}
            except json.JSONDecodeError:
                users = {}

    if email in users:
        return False  # User already exists

    users[email] = {"password": password}

    with open(USER_DB_FILE, "w") as f:
        json.dump(users, f, indent=4)

    return True

# Verify user function
def verify_user(email, password):
    if not os.path.exists(USER_DB_FILE):
        return False

    with open(USER_DB_FILE, "r") as f:
        users = json.load(f)
    
    return email in users and users[email]["password"] == password
