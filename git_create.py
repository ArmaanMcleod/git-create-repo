import sys

import argparse

from os import getcwd

from os.path import basename
from os.path import exists

from getpass import getpass

from subprocess import check_output
from subprocess import run

from requests import post
from requests import RequestException

from json import dumps

from contextlib import contextmanager

RESPONSE_CODE = 201


@contextmanager
def safe_post_request(url, payload, auth):
    """Sends HTTP POST request.

    Safetly sends HTTP POST request and handles exceptions.

    Args:
        url (str): The URL to post to
        payload (str): The data payload to send off
        auth (tuple): The username and password

    Yields:
        requests.models.Request: The request object

    Raises:
        RequestException: If an error occurs in the request
        SystemExit: If an error occurs, exit system

    """

    post_request = post(url=url, data=payload, auth=auth)

    try:
        yield post_request
    except RequestException as err:
        print(err)
        sys.exit(0)
    finally:
        post_request.close()


@contextmanager
def handle_keyboard_interrupt():
    """Handles keyboard interrupts.

    Checks for keyboard interrupts and exits on exception.

    Raises:
        KeyboardInterrupt: If a keyboard interrupt has occured
        SystemExit: If an error occurs, exit system

    """

    try:
        yield
    except KeyboardInterrupt:
        print("\nInterrupted")
        sys.exit(0)


def main():
    """ Main function

    Everything is run from here

    """

    # Collect command line arguements
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--private", action="store_true")
    parser.add_argument("-u", "--username", type=str)
    args = parser.parse_args()

    password = getpass("password: ")
    description = input("description: ")

    # Get username from git config
    github_username = check_output(
        ["git", "config", "user.name"], universal_newlines=True
    ).strip()

    if not github_username and not args.username:
        print("No valid username found")
        print("Either set with git config --global user.name <your username here>")
        print("Or pass username with --username <your username here>")
        sys.exit(0)

    username = args.username if args.username else github_username

    # Repository name is the folder we are currently in
    repo_name = basename(getcwd())

    # The payload to send off to the HTTP POST request
    payload = {
        "name": repo_name,
        "description": description,
        "private": args.private,
        "has_issues": True,
        "has_projects": True,
        "has_wiki": True,
    }

    with safe_post_request(
        url="https://api.github.com/user/repos",
        payload=dumps(payload),
        auth=(username, password),
    ) as response:

        # Only valid if we receive 201 response
        if response.status_code == RESPONSE_CODE:
            setup_default_repo(username=username, repo_name=repo_name)
        else:
            print("An error has occured")
            print(response.json()["message"])


def setup_default_repo(username, repo_name):
    """Sets up default remote repo

    Simulates default repo, similarily when you create a repo online.

    Args:
        username (str): Your Github username
        repo_name (str): The name of the repository to create

    """

    # If no README exists, create a default
    if not exists("README.md"):
        with open("README.md", mode="w") as f:
            f.write("# %s" % repo_name)

    # Initialise local repository
    run(["git", "init"])

    # Add files
    run(["git", "add", "."])

    # First commit
    run(["git", "commit", "-m", '"first commit"'])

    # Add origin via HTTPS
    run(
        [
            "git",
            "remote",
            "add",
            "origin",
            "https://github.com/%s/%s.git" % (username, repo_name),
        ]
    )

    # Push to remote repo and set upstream to master
    run(["git", "push", "-u", "origin", "master"])


if __name__ == "__main__":
    with handle_keyboard_interrupt():
        main()
