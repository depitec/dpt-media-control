#!/bin/bash

# this script folder
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

function getLatestVersion() {
	latest_version=$(curl -s "https://api.github.com/repos/$1/releases/latest" | jq -r '.tag_name')
	echo $latest_version
}

if [[ $@ != *--skip-uv-install* ]]; then
	# install needed packages
	echo "### Installing needed packages"
	echo ""
	apt-get install curl jq -y > /dev/null
	# install uv
	echo "### Installing uv"
	echo ""
	echo "Getting latest version of uv"
	latest_uv_version=$(getLatestVersion "astral-sh/uv")
	echo "Downloading uv $latest_uv_version"
	curl -OL "https://github.com/astral-sh/uv/releases/download/$latest_uv_version/uv-aarch64-unknown-linux-gnu.tar.gz"

	echo "Extracting uv"
	tar -xzf uv-aarch64-unknown-linux-gnu.tar.gz

	echo "moving uv to /usr/local/bin"
	mv uv-aarch64-unknown-linux-gnu/uv /usr/local/bin/
	mv uv-aarch64-unknown-linux-gnu/uvx /usr/local/bin/
	rm -rf uv-aarch64-unknown-linux-gnu*
	echo ""
else
	echo "Skipping uv installation"
	echo ""
fi

if [[ $@ != *--skip-service-install* ]]; then
	echo "### Installing Service"
	echo ""

	echo "Creating service file"
	# make a tmp copy of the service
	cp $SCRIPT_DIR/setup/dpt-media-control.service $SCRIPT_DIR/setup/dpt-media-control.service.tmp

	# replace <<THIS_USER>> with User with id 1000
	USER=$(getent passwd 1000 | cut -d: -f1)
	sed -i "s|<<THIS_USER>>|$USER|g" $SCRIPT_DIR/setup/dpt-media-control.service.tmp

	# replace <<THIS_PYTHON>> with path to thisdir/.venv/bin/python
	sed -i "s|<<THIS_PYTHON>>|$SCRIPT_DIR/.venv/bin/python|g" $SCRIPT_DIR/setup/dpt-media-control.service.tmp

	# replace <<THIS_DIR>> with $SCRIPT_DIR in dpt-media-control.service.tmp
	sed -i "s|<<THIS_DIR>>|$SCRIPT_DIR|g" $SCRIPT_DIR/setup/dpt-media-control.service.tmp

	# move and overwrite if needed the servic
	mv $SCRIPT_DIR/setup/dpt-media-control.service.tmp /etc/systemd/system/dpt-media-control.service

	systemctl daemon-reload
	systemctl enable dpt-media-control.service

else
	echo "Skipping service installation"
	echo ""
fi

echo "### Done"
