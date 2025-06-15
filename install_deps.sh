#!/bin/bash

# check for sudo and exit if root user
if [ $USER == "root" ]; then
	echo "This script should not be run as root"
	exit
fi

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

echo "### Installing requirements"
echo ""
# run uv as user
/usr/local/bin/uv sync
echo ""

echo "### Copy necessary files"

# copy template_config to ~/.config/dpt-media-control/config.toml

cp -r $SCRIPT_DIR/template_config $HOME/.config/dpt-media-control/config.toml