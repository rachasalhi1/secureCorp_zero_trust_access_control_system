import json
import os
from datetime import datetime

DB_PATH = "users.json"

# ─── lecture ───────────────────────────────────────────

def load_db():
    with open(DB_PATH, "r") as f:
        return json.load(f)

def save_db(db):
    with open(DB_PATH, "w") as f:
        json.dump(db, f, indent=2)


# ─── users ─────────────────────────────────────────────

def get_user_by_username(username):
    db = load_db()
    for user in db["users"]:
        if user["username"] == username:
            return user
    return None

def get_user_by_id(user_id):
    db = load_db()
    for user in db["users"]:
        if user["id"] == user_id:
            return user
    return None


# ─── resources ─────────────────────────────────────────

def get_resource_by_id(resource_id):
    db = load_db()
    for res in db["resources"]:
        if res["id"] == resource_id:
            return res
    return None

def get_all_resources():
    db = load_db()
    return db["resources"]


# ─── roles ─────────────────────────────────────────────

def get_role(role_name):
    db = load_db()
    for role in db["roles"]:
        if role["name"] == role_name:
            return role
    return None


# ─── logs dynamiques ───────────────────────────────────

def log_auth(user_id, action, status, ip="unknown"):
    db = load_db()

    # on génère un id auto
    existing_ids = [entry["id"] for entry in db["auth_logs"]]
    new_id = max(existing_ids) + 1 if existing_ids else 1

    entry = {
        "id":        new_id,
        "user_id":   user_id,
        "action":    action,
        "status":    status,
        "ip":        ip,
        "timestamp": datetime.now().isoformat()
    }

    db["auth_logs"].append(entry)
    save_db(db)
    return entry


def log_access(user_id, resource_id, action, decision, reason):
    db = load_db()

    existing_ids = [entry["id"] for entry in db["access_logs"]]
    new_id = max(existing_ids) + 1 if existing_ids else 1

    entry = {
        "id":          new_id,
        "user_id":     user_id,
        "resource_id": resource_id,
        "action":      action,
        "decision":    decision,
        "reason":      reason,
        "timestamp":   datetime.now().isoformat()
    }

    db["access_logs"].append(entry)
    save_db(db)
    return entry


def get_auth_logs(limit=50):
    db = load_db()
    # retourne les N derniers logs
    return db["auth_logs"][-limit:]


def get_access_logs(limit=50):
    db = load_db()
    return db["access_logs"][-limit:]
