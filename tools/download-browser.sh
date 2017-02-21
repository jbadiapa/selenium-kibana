#!/bin/bash
# curl -O -L https://github.com/mozilla/geckodriver/releases/download/v0.14.0/geckodriver-v0.14.0-linux64.tar.gz
# tar xvfz geckodriver-v0.14.0-linux64.tar.gz
if [ ! -f chromedriver ]; then
 curl -O -L https://chromedriver.storage.googleapis.com/2.27/chromedriver_linux64.zip
 unzip -u chromedriver_linux64.zip
fi
