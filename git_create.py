import sys

import argparse

from os import getcwd

from os.path import basename
from os.path import exists

from getpass import getpass

from subprocess import check_output
from subprocess import CalledProcessError

from requests import post
from requests import get
from requests import RequestException

from json import dumps

from contextlib import contextmanager

POST_RESPONSE_CODE = 201
GET_RESPONSE_CODE = 200


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
def safe_get_request(url, auth):
    """Sends HTTP GET request.

    Safetly sends HTTP GET request and handles exceptions.

    Args:
        url (str): The URL to send request to
        auth (tuple): The username and password

    Yields:
        requests.models.Request: The request object

    Raises:
        RequestException: If an error occurs in the request
        SystemExit: If an error occurs, exit system

    """

    get_request = get(url=url, auth=auth)

    try:
        yield get_request
    except RequestException as err:
        print(err)
        sys.exit(0)
    finally:
        get_request.close()


def main():
    """ Main function

    Everything is run from here

    Raises:
        KeyboardInterrupt: If Ctrl-C is pressed

    """

    # Collect command line arguements
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p", "--private", action="store_true", help="private repository"
    )
    parser.add_argument(
        "-s",
        "--ssh",
        action="store_true",
        help="switching from https to ssh remote url. Using git@github.com... instead of https://github.com...",
    )
    parser.add_argument("-n", "--name", type=str, help="name of remote repository")
    args = parser.parse_args()

    # Get username from git config
    try:
        username = check_output(
            ["git", "config", "user.name"], universal_newlines=True
        ).strip()
    except CalledProcessError:
        print(username)
        sys.exit(0)
    except FileNotFoundError:
        print("Git is not installed")
        print("Make sure you install git before running this program")
        sys.exit(0)

    # Repository name is the folder we are currently in
    repo_name = args.name if args.name else basename(getcwd())

    try:

        description = input("description: ")

        # The payload to send off to the HTTP POST request
        payload = {
            "name": repo_name,
            "description": description,
            "private": args.private,
            "has_issues": True,
            "has_projects": True,
            "has_wiki": True,
        }

        while True:

            password = getpass("password: ")

            # Pick SSH or HTTPS url
            url = (
                "https://%s@github.com/%s/%s.git" % (username, username, repo_name)
                if not args.ssh
                else "git@github.com:%s/%s.git" % (username, repo_name)
            )

            with safe_post_request(
                url="https://api.github.com/user/repos",
                payload=dumps(payload),
                auth=(username, password),
            ) as response:

                # Only valid if we receive 201 response
                if response.status_code == POST_RESPONSE_CODE:
                    setup_default_repo(
                        url=url, auth=(username, password), repo_name=repo_name
                    )
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

    except KeyboardInterrupt:
        print("\nProgram interrupted, exiting...\n", end="")
        sys.exit(0)


def setup_default_repo(url, auth, repo_name):
    """Sets up default remote repo

    Simulates default repo, similarily when you create a repo online.

    Args:
        url (str): Thr URL of the remote repository to create
        auth (tuple): The username and password
        repo_name (str): The name of the repository to create

    """

    # The git commands required to setup remote repo
    git_commands = [
        ["git", "init"],
        ["git", "add", "."],
        ["git", "commit", "-m", "first commit"],
        ["git", "remote", "add", "origin", url],
        ["git", "push", "-u", "origin", "master"],
    ]

    # If no README exists, create a default
    if not exists("README.md"):
        with open("README.md", mode="w") as f:
            f.write("# %s" % repo_name)

    # Run git commands
    for command in git_commands:
        try:
            output = check_output(command, universal_newlines=True).strip()
        except KeyboardInterrupt:
            print("\nProgram interrupted, exiting...\n", end="")
            sys.exit(0)
        except CalledProcessError:
            print(output)
            sys.exit(0)

    # Send HTTP GET request to see if repository now exists
    username, _ = auth
    with safe_get_request(
        url="https://api.github.com/repos/%s/%s" % (username, repo_name), auth=auth
    ) as response:
        if response.status_code == GET_RESPONSE_CODE:
            print("\nSuccess!\nCreated %s\n" % url, end="")
        else:
            print("\nError!\n%s not created\n" % url, end="")


if __name__ == "__main__":
    main()
