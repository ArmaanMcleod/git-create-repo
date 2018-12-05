from setuptools import setup, find_packages
from os import path

from io import open

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="git-create-repo",
    version="0.1.4",
    description="Creates local and remote repository from command line",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/OpticGenius/git-create-repo",
    author="Armaan McLeod",
    author_email="opticgenius@hotmail.com",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        'Programming Language :: Python :: 3',
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    keywords="git repository python remote",
    py_modules=["git_create"],
    packages=find_packages(exclude=[]),
    install_requires=["requests"],
    extras_require={},
    package_data={},
    data_files=[],
    entry_points={"console_scripts": ["git_create=git_create:main"]},
    project_urls={
        "Bug Reports": "https://github.com/OpticGenius/git-create-repo/issues",
        "Source": "https://github.com/OpticGenius/git-create-repo",
    },
)
