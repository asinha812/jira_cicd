import os
import requests
import json

url = f"{os.environ['JIRA_BASE_URL']}/rest/api/3/issue"
auth = (os.environ['JIRA_USER_EMAIL'], os.environ['JIRA_API_TOKEN'])

data = {
    "fields": {
        "project": { "key": "TCM" },
        "summary": f"{os.environ['COMMIT_SHA']} - {os.environ['COMMIT_MSG']}",
        "description": os.environ['COMMIT_MSG'],
        "issuetype": { "name": "[System] Change" },
        "reporter": { "emailAddress": os.environ['COMMIT_AUTHOR'] },
        "customfield_12345": os.environ['AFFECTED_SERVICE'],  # Replace with real custom field ID
        "customfield_impl_plan": "The image is released into the production environment",
        "customfield_backout_plan": "There is a roll back to the prior image",
        "customfield_test_plan": "Business verification to be carried out after deployment"
    }
}

response = requests.post(url, auth=auth, headers={'Content-Type': 'application/json'}, data=json.dumps(data))
response.raise_for_status()
issue_key = response.json()["key"]
print(f"::set-output name=issue_key::{issue_key}")