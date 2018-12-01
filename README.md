# git-create-repo

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Creates local and remote git repository from command line. Tool is intented for **Python 3.5+**

## Install

`pip install git-create-repo`

## Usage

`git_create [-p] [-u username]`

Make sure you are in the folder you want to create a repository in. Before running, `cd` into your desired folder. 

#### Create public repository

`git_create`

#### Create private repository

`git_create -p`

You can also specify your username with `-u`. Otherwise the username from `git config user.name` will be used. 

#### Next steps

You will be prompted to enter your password and a description. The description can be skipped by simply pressing `enter`. If your password is incorrect, you will have to run the program again.

If the above is successful, you will now a repository created on your Github account. 

## Note

* This will also create a default `README.md` file including the name of your repository if none exist. 
* It is also suggested to create your own `.gitignore`, so you can ignore what files you don't want commited beforehand. 