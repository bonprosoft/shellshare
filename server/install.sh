#!/bin/bash

BASEDIR=`dirname $0`
BASEDIR=`(cd "$BASEDIR"; pwd)`

echo "Creating virtualenv..."
echo " $ virtualenv env"
virtualenv $BASEDIR/env
echo "Attaching to env..."
echo " $ source env/bin/activate"
source $BASEDIR/env/bin/activate
echo "Restoring packages..."
pip install -r $BASEDIR/packages_requirements.txt
echo -e " \U1F37B Complete!"


