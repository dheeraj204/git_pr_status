import requests
import json

# Specify the repository owner and name
owner = "<owner>"
repo = "<repo>"

# Define the API endpoint for the repository's pull requests
api_endpoint = f"https://api.github.com/repos/{owner}/{repo}/pulls"

# Make a GET request to the API endpoint
response = requests.get(api_endpoint)

# Check if the request was successful
if response.status_code == 200:
    # Parse the response as JSON
    prs = json.loads(response.text)

    # Loop through the pull requests and print the requested information
    for pr in prs:
        print(f"Pull Request #{pr['number']}: {pr['title']}")

        # Get the conversation for the pull request
        conversation_url = pr['url'] + "/reviews"
        conversation_response = requests.get(conversation_url)
        if conversation_response.status_code == 200:
            conversation = json.loads(conversation_response.text)
            print("Conversation:")
            for comment in conversation:
                print(f"- {comment['user']['login']}: {comment['body']}")

        # Get the requested changes for the pull request
        requested_changes_url = pr['url'] + "/requested_reviewers"
        requested_changes_response = requests.get(requested_changes_url)
        if requested_changes_response.status_code == 200:
            requested_changes = json.loads(requested_changes_response.text)
            if len(requested_changes['users']) > 0:
                print("Requested Changes:")
                for user in requested_changes['users']:
                    print(f"- {user['login']}")

        # Get the approved reviews for the pull request
        approved_reviews_url = pr['url'] + "/reviews"
        approved_reviews_response = requests.get(approved_reviews_url)
        if approved_reviews_response.status_code == 200:
            approved_reviews = json.loads(approved_reviews_response.text)
            approved_reviewers = set()
            for review in approved_reviews:
                if review['state'] == "APPROVED":
                    approved_reviewers.add(review['user']['login'])
            if len(approved_reviewers) > 0:
                print("Approved Reviews:")
                for user in approved_reviewers:
                    print(f"- {user}")

        print("-----")
else:
    print("Error: Failed to retrieve pull requests.")
