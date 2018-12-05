# git-create-repo

[![PyPI version](https://badge.fury.io/py/git-create-repo.svg)](https://badge.fury.io/py/git-create-repo)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Creates local and remote git repository from command line. This tool is intended for **Python 3**.

## Install

`pip install git-create-repo`

Or

`python setup.py install`

Also make sure you have [git](https://git-scm.com/downloads) installed. 

## Usage

`git_create.py [-h] [-p] [-s] [-n NAME]`

#### Arguments

```
-h, --help            show this help message and exit
-p, --private         private repository
-s, --ssh             switching from https to ssh remote url. Using
                      git@github.com... instead of https://github.com...
-n NAME, --name NAME  name of remote repository
  ```

Make sure you `cd` into the correct folder you want to create a repository in.

#### Create public repository

`git_create`

#### Create private repository

`git_create -p`

#### Adding Remote repository name

You can specify a different name for the remote repository with `-n`. Otherwise the local repo name will be used. 

#### Switching Remote URL

By default, remotes are added by HTTPS. You can change this to SSH by adding `-s`, assuming you have your SSH keys setup. 

#### Github Username

The tool simply fetches the username from `git config user.name`. If you don't have this set, the tool with prompt you to enter it beforehand. 

#### Next steps

* You will be prompted to enter your password and a description. The description can be skipped by simply pressing `enter`. If your password is incorrect, you will be prompted again.

* If the above is successful, you will now have a repository created on your Github account. 

## Note

* This will create a default `README.md` file including the name of your repository if none exist. 
* It is also suggested to create your own `.gitignore`, so you can ignore what files you don't want commited beforehand. All files get committed otherwise. 

## Development

### Windows

#### Installing Development Dependencies:

* Run `build install`

#### Testing Script

* Use `test` folder generated from `build test` to run script. This is to ensure your actual git repository is not compromised. 

The other build targets are used to upload to Pypi. 

### Linux

#### Installing Development Dependencies

* Ensure you have [GNU Make](https://www.gnu.org/software/make/) installed. You can install this with `sudo apt-get install make`. 

* To install development dependences, run `make install`.

#### Testing Script

* Use `test` folder generated from `make test` to run script. This is to ensure your actual git repository is not compromised. 

The other build targets are used to upload to Pypi. 

## Future
* Other features that can make this tool more usable. 
* Please let me know in the issues tab.