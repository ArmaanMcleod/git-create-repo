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
    """Handles keyboard interrupt.

    Makes sure system exits on keyboard interrupt.

    Raises:
        KeyboardInterrupt: If a keyboard interrupt occurs
        SystemExit: If an error occurs, exit system

    """
    
    try:
        yield
    except KeyboardInterrupt:
        print("\nProgram interrupted, exiting...\n", end="")
    finally:
        sys.exit(0)


def main():
    """ Main function

    Everything is run from here

    Raises:
        KeyboardInterrupt: If Ctrl-C is pressed

    """

    # Collect command line arguements
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--private", action="store_true")
    parser.add_argument("-u", "--username", type=str)
    parser.add_argument("-s", "--ssh", action="store_true")
    parser.add_argument("-n", "--name", type=str)
    args = parser.parse_args()

    with handle_keyboard_interrupt():

        description = input("description: ")

        while True:

            password = getpass("password: ")

            # Get username from git config
            github_username = check_output(
                ["git", "config", "user.name"], universal_newlines=True
            ).strip()

            if not github_username and not args.username:
                print("No valid username found")
                print(
                    "Either set with git config --global user.name <your username here>"
                )
                print("Or pass username with --username <your username here>")
                sys.exit(0)

            username = args.username if args.username else github_username

            # Repository name is the folder we are currently in
            repo_name = args.name if args.name else basename(getcwd())

            # Pick SSH or HTTPS url
            url = (
                "https://github.com/%s/%s.git" % (username, repo_name)
                if not args.ssh
                else "git@github.com:%s/%s.git" % (username, repo_name)
            )

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
                    setup_default_repo(url=url, username=username, repo_name=repo_name)
                    break
                else:
                    message = response.json()["message"].lower().strip()
                    print("ERROR:", message)

                    if message.startswith("bad credentials"):
                        print("Make sure your password is correct\n")

                    elif message.startswith("repository creation failed"):
                        print(
                            "Make sure the repository 'https://github.com/%s/%s.git' doesn't already exist"
                            % (username, repo_name)
                        )
                        break



def setup_default_repo(url, username, repo_name):
    """Sets up default remote repo

    Simulates default repo, similarily when you create a repo online.

    Args:
        url (str): Thr URL of the remote repository to create
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
    run(["git", "commit", "-m", "first commit"])

    # Add origin to remote
    run(["git", "remote", "add", "origin", url])

    # Push to remote repo and set upstream to master
    run(["git", "push", "-u", "origin", "master"])

    print("\nSuccess!\nCreated %s\n" % url, end="")


if __name__ == "__main__":
    main()
