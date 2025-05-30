import os
import json
import requests
from base64 import b64encode

JIRA_USER_EMAIL = os.environ["JIRA_USER_EMAIL"]
JIRA_API_TOKEN = os.environ["JIRA_API_TOKEN"]
JIRA_BASE_URL = os.environ["JIRA_BASE_URL"]
COMMIT_SHA = os.environ["COMMIT_SHA"]
COMMIT_MSG = os.environ["COMMIT_MSG"]
COMMIT_AUTHOR = os.environ["COMMIT_AUTHOR"]
AFFECTED_SERVICE = os.environ["AFFECTED_SERVICE"]

# Jira IDs for dropdowns
FIELDS = {
    "serviceDeskId": "11",
    "requestTypeId": "162",
    "changeType": "10005",      # Normal
    "urgency": "10009",         # Medium
    "risk": "10012",            # Upgrade
    "impact": "10001",          # Significant / Large
    "affectedService": "ari:cloud:graph::service/19f11163-c04c-434c-99a6-431be0298091/8a5f384c-7580-11ef-980f-1201f16ed41f"
}

payload = {
    "serviceDeskId": FIELDS["serviceDeskId"],
    "requestTypeId": FIELDS["requestTypeId"],
    "requestFieldValues": {
        "summary": f"CI/CD Deployment Request - {COMMIT_SHA[:7]}",
        "description": f"Commit: {COMMIT_SHA}\nMessage: {COMMIT_MSG}\nAuthor: {COMMIT_AUTHOR}",
        "customfield_10005": {"id": FIELDS["changeType"]},
        "customfield_10006": {"id": FIELDS["urgency"]},
        "customfield_10007": {"id": FIELDS["risk"]},
        "customfield_10004": {"id": FIELDS["impact"]},
        "customfield_10043": [{"id": FIELDS["affectedService"]}],
        "customfield_10054": "Automated implementation plan via CI/CD pipeline.",
        "customfield_10055": "Standard backout procedure applies.",
        "customfield_10056": "Deployment validated by automated tests."
    }
}

auth = b64encode(f"{JIRA_USER_EMAIL}:{JIRA_API_TOKEN}".encode()).decode()
headers = { 
    "Authorization": f"Basic {auth}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

url = f"{JIRA_BASE_URL}/rest/servicedeskapi/request"
response = requests.post(url, headers=headers, json=payload)

if response.status_code == 201:
    issue_key = response.json()["issueKey"]
    print(f"✅ Created Jira ticket: {issue_key}")
    # Set GitHub Action output
    print(f"::set-output name=issue_key::{issue_key}")
else:
    print("❌ Failed to create Jira ticket")
    print(response.status_code)
    print(response.text)
    exit(1)