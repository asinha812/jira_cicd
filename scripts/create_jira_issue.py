import requests
from requests.auth import HTTPBasicAuth
import json
import os
import sys

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

# Issue payload
payload = json.dumps({
    "fields": {
        "description": {
            "content": [
                {
                    "content": [
                        {
                            "text": "My first jira ticket",
                            "type": "text"
                        }
                    ],
                    "type": "paragraph"
                }
            ],
            "type": "doc",
            "version": 1
        },
        "project": {
            "key": "ACT"  # Change to your actual Jira project key
        },
        "issuetype": {
            "id": "10523"  # Make sure this issue type ID is correct
        },
        "summary": "First JIRA Ticket",
    },
    "update": {}
})

# API call
response = requests.post(url, data=payload, headers=headers, auth=auth)

# Handle response
if response.status_code >= 200 and response.status_code < 300:
    data = response.json()
    issue_key = data.get("key")
    print(f"✅ Created Jira issue: {issue_key}")
    
    # Output to GitHub Actions
    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output:
        with open(github_output, "a") as f:
            f.write(f"issue_key={issue_key}\n")
    else:
        print("⚠️ GITHUB_OUTPUT environment variable not set.")

else:
    print(f"❌ Failed to create Jira issue. Status code: {response.status_code}")
    print(response.text)
    sys.exit(1)