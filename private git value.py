from datetime import datetime, timezone

from github import Github

# Replace with your own GitHub personal access token
access_token = 'your_access_token_here'

# Replace with your organization and repository name
org_name = 'your_organization_name_here'
repo_name = 'your_repository_name_here'

g = Github(access_token)

# Get the organization and repository objects
org = g.get_organization(org_name)
repo = org.get_repo(repo_name)

# Get all open pull requests for the repository
pulls = repo.get_pulls(state='open')

# Loop through each pull request and display relevant updates
for pull in pulls:
    print('Pull Request:', pull.title)
    print('Opened By:', pull.user.login)
    print('Opened At:', pull.created_at)

    # Get the latest review and display reviewer and approval status
    latest_review = pull.get_reviews().reversed[0]
    print('Latest Review By:', latest_review.user.login)
    print('Latest Review Status:', latest_review.state)
    print('Latest Review At:', latest_review.submitted_at)

    # Get the latest review comment and display commenter and content
    latest_comment = pull.get_review_comments().reversed[0]
    print('Latest Comment By:', latest_comment.user.login)
    print('Latest Comment Content:', latest_comment.body)
    print('Latest Comment At:', latest_comment.created_at)

    # Get the latest pull request update and display updater and time elapsed
    latest_update = max(pull.updated_at, latest_review.submitted_at, latest_comment.created_at)
    time_elapsed = datetime.now(timezone.utc) - latest_update
    print('Latest Update By:', pull.updated_by.login)
    print('Latest Update At:', latest_update)
    print('Days Since Latest Update:', time_elapsed.days)
    print('---------------------------------------')