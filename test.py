import os
from os.path import join
from datetime import datetime
from github import Github
from past.builtins import raw_input

from data import RepositoryData

today = datetime.today()
day = today.strftime("%d_%b_%Y")

# set up the path where file will be created
folder = RepositoryData.data['path']+day

# Set up authentication with personal access token
token = os.environ[RepositoryData.data['git_token']]
g = Github(token)

# Set the organization and repositories to retrieve pull requests from
org_name = RepositoryData.data['org_name']
repo_names = RepositoryData.data['tests_repo']

for repo_name in repo_names:
    # Get the repository object
    repo = g.get_repo(f"{org_name}/{repo_name}")

    # Get all open pull requests in the repository
    pull_requests = repo.get_pulls(state="open")
    # Git Repository
    name_of_file = raw_input(repo_name+".txt")
    file_path = join(folder, name_of_file)
    if not os.path.isdir(folder):
        os.mkdir(folder)
    with open(file_path, 'w') as repo_data:

        # Loop through each pull request and retrieve relevant information
        for pull_request in pull_requests:
            data = [f"Pull Request #{pull_request.number} in {repo_name}:",
                    f"- Created by {pull_request.user.login} on {pull_request.created_at}",
                    f"- Requested changes by {pull_request.requested_reviewers} on {pull_request.updated_at}",
                    f"- Approved by {pull_request.merged_by.login} on {pull_request.merged_at}", "Comments:"]
            comments = []
            for comment in pull_request.get_issue_comments():
                comments.append(f"- {comment.user.login} commented on {comment.created_at}: {comment.body}")
            data.append(comments)

            # Calculate the number of days since the pull request was last updated
            days_since_update = (datetime.utcnow() - pull_request.updated_at).days
            last_update = f"- Days since last update: {days_since_update}"
            data.append(last_update)
            for line in data:
                repo_data.write(line+'\n')
