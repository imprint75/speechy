#!/bin/sh

echo "***** START *****"
echo "Install Python3 packages"

sudo apt-get install python3-pip -y

sudo `which pip3` install virtualenv
virtualenv --no-site-packages venv

venv/bin/pip install -r /srv/speechy/requirements.txt