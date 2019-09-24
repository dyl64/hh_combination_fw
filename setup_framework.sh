#!/usr/bin/env bash

# Copy setup_local.sh templates to relevant folders and set WSCombiner path

WSCOMBINER_PATH=""

echo "Setup script for the HH combination framework. This setup needs to be used only before the first usage!"
echo ""
echo "Please give the path to yout local version of the WSCombiner: "

read WSCOMBINER_PATH

echo "Copy './setup_local_template.sh' to './setup_local.sh'"
cp setup_local_template.sh setup_local.sh
echo "Copy './setup_local_template.sh' to './submodules/RooStatTools/setup_local.sh'"
cp setup_local_template.sh ./submodules/RooStatTools/setup_local.sh
echo "Set WSCombiner path in both setup_local.sh files"
sed -i "s+PATH_TO_WSCOMBINER+${WSCOMBINER_PATH}+g" ./setup_local.sh
sed -i "s+PATH_TO_WSCOMBINER+${WSCOMBINER_PATH}+g" ./submodules/RooStatTools/setup_local.sh
echo "Framework is set up now!"