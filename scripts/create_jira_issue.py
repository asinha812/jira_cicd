import requests
from requests.auth import HTTPBasicAuth
import json
import os
import sys
from datetime import datetime

# Jira API endpoint
url = f"{os.environ['JIRA_BASE_URL']}/rest/api/3/issue"

# Auth setup
API_TOKEN = os.environ['JIRA_API_TOKEN']
auth = HTTPBasicAuth(os.environ['JIRA_USER_EMAIL'], API_TOKEN)

# Request headers
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

# Inputs from GitHub Actions
REPO = os.environ.get("GITHUB_REPOSITORY", "unknown-repo")
SHA = os.environ.get("GITHUB_SHA", "")[:7]
ACTOR = os.environ.get("GITHUB_ACTOR", "unknown")
BRANCH = os.environ.get("GITHUB_REF_NAME", "main")
IMAGE_TAG = f"ghcr.io/{REPO}:sha-{SHA}"
DATE = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

# Summary line
summary = f"[PROD DEPLOYMENT] Approval Request for Commit {SHA} - {REPO.split('/')[-1]}"

# Jira ADF description body
description = {
    "version": 1,
    "type": "doc",
    "content": [
        {"type": "paragraph", "content": [{"type": "text", "text": "Deployment Request to Production"}]},
        {"type": "paragraph", "content": [{"type": "text", "text": f"Repository: {REPO}"}]},
        {"type": "paragraph", "content": [{"type": "text", "text": f"Branch: {BRANCH}"}]},
        {"type": "paragraph", "content": [{"type": "text", "text": f"Commit: {SHA}"}]},
        {"type": "paragraph", "content": [{"type": "text", "text": f"Image Tag: {IMAGE_TAG}"}]},
        {"type": "paragraph", "content": [{"type": "text", "text": " "} ]},
        {"type": "paragraph", "content": [{"type": "text", "text": "Please approve this deployment by commenting:"}]},
        {"type": "paragraph", "content": [{"type": "text", "text": "- Approved"}]},
        {"type": "paragraph", "content": [{"type": "text", "text": "- Approved for Prod"}]},
        {"type": "paragraph", "content": [{"type": "text", "text": "- Or reject via: Reject / Deny"}]},
        {"type": "paragraph", "content": [{"type": "text", "text": f"Requested On: {DATE}"}]},
        {"type": "paragraph", "content": [{"type": "text", "text": f"Requested By: {ACTOR}"}]}
    ]
}

# Final payload
payload = json.dumps({
    "fields": {
        "project": {
            "key": "ACT"  # Replace with your actual project key
        },
        "issuetype": {
            "id": "10523"  # Replace with your actual issue type ID
        },
        "summary": summary,
        "description": description
    }
})

# API call
response = requests.post(url, data=payload, headers=headers, auth=auth)

# Handle response
if response.status_code >= 200 and response.status_code < 300:
    data = response.json()
    issue_key = data.get("key")
    print(f"Created Jira issue: {issue_key}")
    
    # Output to GitHub Actions
    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output:
        with open(github_output, "a") as f:
            f.write(f"issue_key={issue_key}\n")
    else:
        print("GITHUB_OUTPUT environment variable not set.")
else:
    print(f"Failed to create Jira issue. Status code: {response.status_code}")
    print(response.text)
    sys.exit(1)