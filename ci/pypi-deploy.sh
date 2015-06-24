#!/bin/bash

echo "[server-login]" > ~/.pypirc
echo "username:" ${PYPI_USER} >> ~/.pypirc
echo "password:" ${PYPI_PASSWORD} >> ~/.pypirc

version=`python -c 'from w3af_api_client import __VERSION__;print __VERSION__,'`
curl -f -s -S -k -X GET -I https://pypi.python.org/packages/source/w/w3af-api-client/w3af-api-client-$version.tar.gz

if [[ $? -eq 0 ]]
then
    echo "Current package version is already at PyPi. If your intention was to"
    echo "release a new version, you'll have to increase the version number."
else
    echo "Uploading $version version to PyPi"
    python setup.py sdist upload
fi

exit 0