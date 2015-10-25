#!/bin/bash

echo "Creating virtualenv..."
echo " $ virtualenv env"
virtualenv env
echo "Attaching to env..."
echo " $ source env/bin/activate"
source env/bin/activate
echo "Restoring packages..."
pip install -r packages_requirements.txt
echo -e "\U1F37B Complete!"

