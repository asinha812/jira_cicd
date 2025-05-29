import requests
from requests.auth import HTTPBasicAuth
import json
import os
import sys
from datetime import datetime

# Jira endpoint & authentication
url = f"{os.environ['JIRA_BASE_URL']}/rest/api/3/issue"
auth = HTTPBasicAuth(os.environ['JIRA_USER_EMAIL'], os.environ['JIRA_API_TOKEN'])

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

# GitHub environment data
REPO = os.environ.get("GITHUB_REPOSITORY", "unknown-repo")
SHA = os.environ.get("COMMIT_SHA", "")[:7]
ACTOR = os.environ.get("GITHUB_ACTOR", "unknown")
BRANCH = os.environ.get("GITHUB_REF_NAME", "main")
COMMIT_MSG = os.environ.get("COMMIT_MSG", "No commit message provided.")
COMMIT_AUTHOR = os.environ.get("COMMIT_AUTHOR", "unknown@noreply.github.com")
AFFECTED_SERVICE = os.environ.get("AFFECTED_SERVICE", "Unknown")
DATE = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
IMAGE_TAG = f"ghcr.io/{REPO}:sha-{SHA}"

# Summary for ticket
summary = f"{SHA} - {COMMIT_MSG}"

# ADF (Atlassian Document Format) description body
description = {
    "version": 1,
    "type": "doc",
    "content": [
        {"type": "paragraph", "content": [{"type": "text", "text": "Deployment Request to Production"}]},
        {"type": "paragraph", "content": [{"type": "text", "text": f"Repository: {REPO}"}]},
        {"type": "paragraph", "content": [{"type": "text", "text": f"Branch: {BRANCH}"}]},
        {"type": "paragraph", "content": [{"type": "text", "text": f"Commit: {SHA}"}]},
        {"type": "paragraph", "content": [{"type": "text", "text": f"Image Tag: {IMAGE_TAG}"}]},
        {"type": "paragraph", "content": [{"type": "text", "text": f"Affected Service: {AFFECTED_SERVICE}"}]},
        {"type": "paragraph", "content": [{"type": "text", "text": "Implementation Plan: The image is released into the production environment"}]},
        {"type": "paragraph", "content": [{"type": "text", "text": "Backout Plan: There is a roll back to the prior image"}]},
        {"type": "paragraph", "content": [{"type": "text", "text": "Test Plan: Business verification to be carried out after deployment"}]},
        {"type": "paragraph", "content": [{"type": "text", "text": f"Requested By: {ACTOR}"}]},
        {"type": "paragraph", "content": [{"type": "text", "text": f"Requested On: {DATE}"}]}
    ]
}

# Final Jira payload
payload = {
    "fields": {
        "project": {
            "key": "TCM"  # 🔁 Replace with actual project key
        },
        "issuetype": {
            "name": "[System] Change"  # 🔁 Must match your Jira issue type
        },
        "summary": summary,
        "description": description,
        "reporter": {
            "emailAddress": COMMIT_AUTHOR
        },
        # Custom fields below need to match your Jira schema IDs
        "customfield_12345": AFFECTED_SERVICE,  # 🔁 Replace with actual custom field ID for Affected Service
        "customfield_67890": "The image is released into the production environment",  # Implementation Plan
        "customfield_67891": "There is a roll back to the prior image",               # Backout Plan
        "customfield_67892": "Business verification to be carried out after deployment" # Test Plan
    }
}

# Send request
response = requests.post(url, data=json.dumps(payload), headers=headers, auth=auth)

# Debug output
if response.status_code >= 200 and response.status_code < 300:
    issue_key = response.json().get("key")
    print(f"✅ Created Jira issue: {issue_key}")
    
    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output:
        with open(github_output, "a") as f:
            f.write(f"issue_key={issue_key}\n")
else:
    print("❌ Jira issue creation failed")
    print(f"Status code: {response.status_code}")
    print(f"Response: {response.text}")
    sys.exit(1)