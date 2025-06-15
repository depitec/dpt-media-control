#!/bin/bash

# check for sudo and exit if root user
if [ $USER == "root" ]; then
	echo "This script should not be run as root"
	exit
fi

echo "### Installing requirements"
echo ""
# run uv as user
/usr/local/bin/uv sync
echo ""
