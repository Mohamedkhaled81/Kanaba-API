#!/bin/sh

pip install --upgrade pip

if [ "$mode" = "DEV" ];then
    pip install -r /tmp/requirements-dev.txt
    pip install -r /tmp/requirements.txt
else
    pip install -r /tmp/requirements.txt
fi

rm -f /tmp/requirements-dev.txt /tmp/requirements.txt



