from flask import Flask, request, jsonify
import json
from datetime import datetime
from BDD.manager_bdd import log_access, get_user_by_username

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


app = Flask(__name__)

CLEARANCE_LEVELS = {
    "public": 0,
    "confidential": 1,
    "secret": 2
}

def load_policies():
    with open("policy_engine/policy_engine.json","r")as f:
        data = json.load(f)
    return data["policies"], data["default"]

def compute_dynamic_flags(user, resource, environment):
    flags = {}
    user_dept = user.get("department", "").lower()
    resource_dept = resource.get("department", "").lower()
    flags["user.department_equals_resource"] = (user_dept == resource_dept)

    current_hour = datetime.now().hour
    flags["environment.outside_working_hours"] = (current_hour < 8 or current_hour >= 18)

    user_clearance = user.get("clearance", "public").lower()
    resource_classification = resource.get("classification", "public").lower()
    user_level = CLEARANCE_LEVELS.get(user_clearance, 0)
    resource_level = CLEARANCE_LEVELS.get(resource_classification, 0)
    flags["user.clearance_sufficient"] = (user_level >= resource_level)

    return flags

def check_condition(key, expected, user, resource, environment, action, flags):
    if key == "action":
        if isinstance(expected, list):
            return action.lower() in [a.lower() for a in expected]
        else:
            return action.lower() == expected.lower()

    if key in flags:
        return flags[key] == expected

    parts = key.split(".")
    if len(parts) != 2:
        return False

    category, attribute = parts[0], parts[1]

    if category == "user":
        actual = user.get(attribute, "")
    elif category == "resource":
        actual = resource.get(attribute, "")
    elif category == "environment":
        actual = environment.get(attribute, "") if environment else ""
    else:
        return False

    if isinstance(expected, list):
        return actual in expected
    else:
        return actual == expected

def evaluate_policies(user, resource, action, environment):
    policies, default_effect = load_policies()
    policies_sorted = sorted(policies, key=lambda p: p.get("priority", 99))
    flags = compute_dynamic_flags(user, resource, environment)

    for policy in policies_sorted:
        conditions = policy.get("conditions", {})
        all_match = True

        for key, expected in conditions.items():
            if not check_condition(key, expected, user, resource, environment, action, flags):
                all_match = False
                break

        if all_match:
            effect = policy.get("effect", "DENY")
            return effect, policy.get("description", "matched: " + policy.get("id", "?"))

    return default_effect, "no policy matched, applying default"


@app.route("/decide", methods=["POST"])
def decide():
    data = request.get_json()

    if not data:
        return jsonify({"error": "no data provided"}), 400

    user        = data.get("user", {})
    resource    = data.get("resource", {})
    action      = data.get("action", "read")
    environment = data.get("environment", {})

    if not user or not resource:
        return jsonify({"error": "user and resource are required"}), 400

    decision, reason = evaluate_policies(user, resource, action, environment)

    # ← ici : les 4 lignes sont bien DANS la route, après evaluate_policies()
    user_obj = get_user_by_username(user.get("username"))
    user_id  = user_obj["id"] if user_obj else None
    log_access(user_id, resource.get("id"), action, decision, reason)

    return jsonify({
        "decision": decision,
        "reason":   reason,
        "user":     user.get("username"),
        "resource": resource.get("id"),
        "action":   action
    })


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "PDP running", "time": datetime.now().isoformat()})


if __name__ == "__main__":
    app.run(port=5001, debug=True)
