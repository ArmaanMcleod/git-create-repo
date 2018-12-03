@echo off

if not "%~1" == "" (goto :%1 2>nul)
goto :default

:test
mkdir test
xcopy /y git_create.py test
cd test
goto:eof

:clean
rmdir /s /q test
rmdir /s /q build
rmdir /s /q dist
rmdir /s /q git_create_repo.egg-info
goto:eof

:install
pip install -r requirements.txt
goto:eof

:sandbox
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
pip install --extra-index-url https://testpypi.python.org/pypi git-create-repo
goto:eof

:setup
python setup.py sdist
python setup.py bdist_wheel
goto:eof

:upload
twine upload dist/*
goto:eof

:uninstall
pip uninstall git-create-repo -y
goto:eof

:default
echo USAGE: build.bat (rule)
echo Build Script rules:
echo test - Create test directory.
echo clean - Clean extra directories generated.
echo install - Install dependencies.
echo sandbox - Install test pypi package.
echo setup - Setup source distribution and wheel.
echo upload - Upload source distribution and wheel to PyPi.
echo uninstall - Uninstalls Pypi package.