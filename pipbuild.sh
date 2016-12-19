#!/usr/bin/env bash

PACKAGE="txcelery-py3"

set -o nounset
set -o errexit
#set -x

if [ -n "$(git status --porcelain)" ]; then
    echo "There are uncomitted changes, please make sure all changes are comitted" >&2
    exit 1
fi

if ! [ -f "setup.py" ]; then
    echo "setver.sh must be run in the directory where setup.py is" >&2
    exit 1
fi

VER="${1:?You must pass a version of the format 0.0.0 as the only argument}"

if git tag | grep -q "${VER}"; then
    echo "Git tag for version ${VER} already exists." >&2
    exit 1
fi

echo "Setting version to $VER"

# Update the package version
sed -i "s;.*version.*;__version__ = '${VER}';" txcelery/__init__.py

# Upload to test pypi
if [[ ${VER} == *"dev"* ]]; then
    python setup.py sdist
    git reset --hard

else
    python setup.py sdist upload -r pypitest
    # Reset the commit, we don't want versions in the commit
    git commit -a -m "Updated to version ${VER}"

    git tag ${VER}
    git push
    git push --tags
fi



echo "If you're happy with this you can now run :"
echo
echo "python setup.py sdist upload -r pypi"
echo