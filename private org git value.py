import os
from datetime import datetime
from github import Github
from git_data import RepositoryData

# Set up authentication with personal access token
token = os.environ['GITHUB_TOKEN']
g = Github(token)

# Set the organization and repositories to retrieve pull requests from
org_name = RepositoryData.data['org_name']
repo_names = RepositoryData.data['']

for repo_name in repo_names:
    # Get the repository object
    repo = g.get_repo(f"{org_name}/{repo_name}")

    # Get all open pull requests in the repository
    pull_requests = repo.get_pulls(state="open")
    # Git Repository
    print(f"{repo_name}")

    # Loop through each pull request and retrieve relevant information
    for pull_request in pull_requests:
        print(f"Pull Request #{pull_request.number} in {repo_name}:")
        print(f"- Created by {pull_request.user.login} on {pull_request.created_at}")
        print(f"- Requested changes by {pull_request.requested_reviewers} on {pull_request.updated_at}")
        print(f"- Approved by {pull_request.merged_by.login} on {pull_request.merged_at}")
        print("Comments:")
        for comment in pull_request.get_issue_comments():
            print(f"- {comment.user.login} commented on {comment.created_at}: {comment.body}")
        print("")

        # Calculate the number of days since the pull request was last updated
        days_since_update = (datetime.utcnow() - pull_request.updated_at).days
        print(f"- Days since last update: {days_since_update}\n")
