import os
from os.path import join
from datetime import datetime
from github import Github

from git_data import RepositoryData
from apscheduler.schedulers.blocking import BlockingScheduler
from send_email import attach_logs_remainder, check_logs


def git_status(repo='tests_repo', logs_attached=False):
    # Fetch day/name of the folder
    today = datetime.today()
    day = today.strftime("%d_%b_%Y")

    # Create a folder for all data to be saved if not existing already
    location = RepositoryData.data['path']
    if not os.path.isdir(location):
        os.mkdir(location)

    # set up the path where file will be created
    folder = RepositoryData.data['path'] + day

    # Organization base Git url to fetch api
    org_url = RepositoryData.data['base_url']

    # Set up authentication with personal access token
    token = RepositoryData.data['git_token']

    # initialize GitHub object with organization's Git token and base URL
    git = Github(login_or_token=token, base_url=org_url)

    # Set the organization and repositories to retrieve pull requests from
    org_name = RepositoryData.data['org_name']
    repo_names = RepositoryData.data[repo]

    # Extensions for logs verification
    extensions = RepositoryData.data['extensions']

    for repo_name in repo_names:
        # Get the repository object
        repositories = git.get_repo(f"{org_name}/{repo_name}")

        # Get all open pull requests in the repository
        pull_requests = repositories.get_pulls(state="open")

        # Git Repository name
        name_of_file = repo_name + ".txt"
        file_path = join(folder, name_of_file)

        # Create a folder with current date as name for all data to be saved if not existing already
        if not os.path.isdir(folder):
            os.mkdir(folder)

        with open(file_path, 'w') as repo_data:

            # Loop through each pull request and retrieve relevant information
            for pull_request in pull_requests:
                reviews_list = ['Reviews:\n']
                reviews = pull_request.get_reviews()
                for rvw in reviews:
                    reviews_list.append(f'{rvw.user.login}: {rvw.state}\n')
                data = [f"Pull Request #{pull_request.number} in {repo_name}:",
                        f"- Created by {pull_request.user.login} on "
                        f"{pull_request.created_at}",
                        f"- Requested changes by "
                        f"{pull_request.requested_reviewers} on "
                        f"{pull_request.updated_at}",
                        # f"- Approved by {pull_request.merged_by.login}"
                        # f" on {pull_request.merged_at}",
                        "Comments:"]
                comments = []
                for comment in pull_request.get_issue_comments():
                    comments.append(f"- {comment.user.login} commented on "
                                    f"{comment.created_at}: {comment.body}")
                data.extend(comments)
                if logs_attached:
                    # if logs are not attached mail will be triggered to user who raised PR
                    employee_mail_id = f'{pull_request.user.login}'.lower() + RepositoryData.data['mail_domain']
                    if not check_logs(extensions=extensions, comments=comments):
                        attach_logs_remainder(receiver_mail_id=employee_mail_id,
                                              pr_number=f'{pull_request.number}', repo=f'{repo_name}')
                data.extend(reviews_list)

                # Calculate the number of days since the pull request was last updated
                days_since_update = (datetime.utcnow() - pull_request.updated_at) \
                    .days
                last_update = f"- Days since last update: {days_since_update}"
                data.append(last_update)
                for line in data:
                    repo_data.write(line + '\n')


scheduler = BlockingScheduler()
scheduler.add_job(git_status(), 'interval', hours=24)
scheduler.start()
