#!/bin/sh

var="$mode"

if [ var == "DEV" ]
then
    pip install -r /tmp/requirements-dev.txt
    pip install -r /tmp/requirements.txt
    
else
    pip install -r /tmp/requirements.txt

fi

rm -rf /tmp



