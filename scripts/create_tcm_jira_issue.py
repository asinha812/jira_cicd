import os
import json
import requests
from datetime import datetime, timezone

# Environment variables (from GitHub Actions or secrets)
JIRA_BASE_URL = os.environ["JIRA_BASE_URL"]
ACCESS_TOKEN = os.environ["JIRA_ACCESS_TOKEN"]
# SERVICE_DESK_ID = os.environ["JIRA_SERVICE_DESK_ID"]
# REQUEST_TYPE_ID = os.environ["JIRA_REQUEST_TYPE_ID"]

COMMIT_SHA = os.environ["COMMIT_SHA"]
COMMIT_MSG = os.environ["COMMIT_MSG"]
COMMIT_AUTHOR = os.environ["COMMIT_AUTHOR"]
AFFECTED_SERVICE = os.environ["AFFECTED_SERVICE"]

DATE = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

# Jira Service Management API endpoint
url = f"{JIRA_BASE_URL}/rest/servicedeskapi/servicedesk/11/requesttype"

# Authorization header
headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# Request payload (fields must be mapped correctly to request type fields)
payload = {
    "serviceDeskId": 11,
    "requestTypeId": 10038,
    "requestFieldValues": {
        "summary": f"[PROD] {COMMIT_SHA[:7]} - {COMMIT_MSG}",
        "description": (
            f"Commit: {COMMIT_SHA}\n"
            f"Author: {COMMIT_AUTHOR}\n"
            f"Affected Service: {AFFECTED_SERVICE}\n\n"
            f"Implementation Plan: The image is released into the production environment\n"
            f"Backout Plan: There is a roll back to the prior image\n"
            f"Test Plan: Business verification to be carried out after deployment\n\n"
            f"Requested: {DATE}"
        )
    },
    "raiseOnBehalfOf": COMMIT_AUTHOR
}

# API call to create the request
response = requests.post(url, headers=headers, data=json.dumps(payload))

# Check result
if response.status_code in [200, 201]:
    issue_key = response.json().get("issueKey")
    print(f"✅ Created JSM request: {issue_key}")
    
    # Export key to GitHub Actions
    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output:
        with open(github_output, "a") as f:
            f.write(f"issue_key={issue_key}\n")
else:
    print(f"❌ Jira Service Management request failed")
    print(f"Status code: {response.status_code}")
    print(response.text)
    exit(1)