import requests
from requests.auth import HTTPBasicAuth
import json
import os

url = f"{os.environ['JIRA_BASE_URL']}/rest/api/3/issue"

API_TOKEN = os.environ['JIRA_API_TOKEN']

auth = HTTPBasicAuth(os.environ['JIRA_USER_EMAIL'], API_TOKEN)

headers = {
  "Accept": "application/json",
  "Content-Type": "application/json"
}

payload = json.dumps( {
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
      "key": "ACT"
    },
    "issuetype": {
      "id": "10523"
    },
    "summary": "First JIRA Ticket",
  },
  "update": {}
} )

response = requests.request(
   "POST",
   url,
   data=payload,
   headers=headers,
   auth=auth
)

print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))