from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from datetime import datetime
from bdd.manager_bdd import log_access, get_user_by_username
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

CLEARANCE_LEVELS = {
    "public": 0,
    "confidential": 1,
    "secret": 2
}


def load_policies():
    with open("policy_engine/policy_engine.json", "r") as f:
        data = json.load(f)
    return data["policies"], data["default"]


def compute_dynamic_flags(user, resource):
    flags = {}

    flags["user.department_equals_resource"] = (
        user.get("department", "").lower() ==
        resource.get("department", "").lower()
    )

    current_hour = datetime.now().hour
    flags["environment.outside_working_hours"] = (
        current_hour < 8 or current_hour >= 18
    )

    user_level = CLEARANCE_LEVELS.get(user.get("clearance", "public").lower(), 0)
    resource_level = CLEARANCE_LEVELS.get(resource.get("classification", "public").lower(), 0)

    flags["user.clearance_sufficient"] = (user_level >= resource_level)

    return flags


def check_condition(key, expected, user, resource, flags):

    # dynamic flags
    if key in flags:
        return flags[key] == expected

    parts = key.split(".")
    if len(parts) != 2:
        return False

    category, attribute = parts

    if category == "user":
        actual = user.get(attribute)
    elif category == "resource":
        actual = resource.get(attribute)
    else:
        return False

    if isinstance(expected, list):
        return actual in expected

    return actual == expected

def evaluate_policies(user, resource):
    policies, default_effect = load_policies()
    flags = compute_dynamic_flags(user, resource)

    policies_sorted = sorted(policies, key=lambda p: p.get("priority", 99))

    allowed_actions = set()

    for policy in policies_sorted:
        conditions = policy.get("conditions", {})
        match = True

        for key, expected in conditions.items():
            if not check_condition(key, expected, user, resource, flags):
                match = False
                break

        if match:
            for action in policy.get("allowed_actions", []):
                allowed_actions.add(action)

    if not allowed_actions:
        return "DENY", []

    return "ALLOW", list(allowed_actions)

class PDPHandler(BaseHTTPRequestHandler):

    def _send_response(self, code, data):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_POST(self):
        if self.path != "/decide":
            self._send_response(404, {"error": "not found"})
            return

        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)

        try:
            data = json.loads(body)
        except:
            self._send_response(400, {"error": "invalid JSON"})
            return

        user = data["user"]
        resource = data["resource"]
       
        if not user or not resource:
            self._send_response(400, {"error": "missing user/resource"})
            return

        decision, allowed_actions = evaluate_policies(user, resource)

        user_obj = get_user_by_username(user.get("username"))
        user_id = user_obj["id"] if user_obj else None

        log_access(
          user_id,
         resource.get("id"),
          "AUTHZ_CHECK",
          decision,
          f"allowed_actions={allowed_actions}"
)




        response = {
                    "success":"access_granted",
                     
                }

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        self.wfile.write(json.dumps(response).encode())
        





    def do_GET(self):
        if self.path == "/health":
            self._send_response(200, {
                "status": "PDP running",
                "time": datetime.now().isoformat()
            })
        else:
            self._send_response(404, {"error": "not found"})


if __name__ == "__main__":
    server = HTTPServer(("localhost", 5001), PDPHandler)
    print("PDP running on http://localhost:5001")
    server.serve_forever()
