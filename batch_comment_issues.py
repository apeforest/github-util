"""
Adding comments to a batch of Github issues
Uses basic authentication (Github username + password) to retrieve Issues
from a repository that username has access to. Supports Github API v3.
"""
import json
import sys

from github import Github


def get_labels(repo, names):
    labels = []
    for name in names:
        try:
            labels.append(repo.get_label(name))
        except Exception as ex:
            print("Error: invalid label " + name)

    return labels


def get_issues(repo, config):
    assignee = config['assignee']
    labels = get_labels(repo, config['labels'])
    state = config['state']
    creator = config['creator']

    return repo.get_issues(assignee=assignee, labels=labels, state=state,
                           creator=creator)


def batch_comment_issues(issues, config):
    for issue in issues:
        issue.create_comment(config['message'])


def main():

    with open('config.json') as f:
        config = json.load(f)
        github = Github(config['user'], config['password'])
        repo = github.get_repo(config['owner'] + '/' + config['repository'])
        issues = get_issues(repo, config)
        batch_comment_issues(issues, config)

    return 0


if __name__ == "__main__":
    sys.exit(main())



