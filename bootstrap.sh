#!/bin/bash

# Much experiment. Many OSX. Wow.

sudo pip install --upgrade setuptools
sudo pip install virtualenv
sudo pip install virtualenvwrapper

brew install ffmpeg
brew install mongodb
brew install redis
brew install nginx
brew install uwsgi
brew install ImageMagick

mongod &
redis-server &
sudo nginx

source `which virtualenvwrapper.sh`

touch hippocampus/allowed

mkvirtualenv mongo
