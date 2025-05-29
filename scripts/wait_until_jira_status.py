import argparse, os, time
import requests

parser = argparse.ArgumentParser()
parser.add_argument('--issue', required=True)
parser.add_argument('--status', required=True)
args = parser.parse_args()

url = f"{os.environ['JIRA_BASE_URL']}/rest/api/3/issue/{args.issue}"
auth = (os.environ['JIRA_USER_EMAIL'], os.environ['JIRA_API_TOKEN'])

print(f"⏳ Waiting for issue {args.issue} to reach status '{args.status}'")

while True:
    response = requests.get(url, auth=auth, headers={'Accept': 'application/json'})
    current_status = response.json()['fields']['status']['name']
    print(f"🔍 Current status: {current_status}")
    if current_status == args.status:
        print(f"✅ Reached status '{args.status}'.")
        break
    elif current_status in ['Rejected', 'Cancelled']:
        print(f"❌ Aborted due to status '{current_status}'.")
        exit(1)
    time.sleep(30)