#!/bin/sh

coverage run -m unittest discover -s tests -p "test_*.py" -v
coverage html
sudo cp -r htmlcov /var/www/sublim.nl/httpdocs/
