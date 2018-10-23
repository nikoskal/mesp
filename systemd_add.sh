#!/bin/bash

PWD=$(pwd)
# Edit Unit file
CMD=$PWD"/py/agent.py -f "$PWD"/conf/agent.ini"
STR=`awk -v var="$CMD" '{if(/ExecStart=/) {print$0var}}' $PWD/conf/agent.service`
echo $STR
sed -i "s:ExecStart=:$STR:g" $PWD/conf/agent.service

# Link Unit file to systemd dir
echo "Linking file "$PWD"/py/agent.py to systemd directory"
chmod 664 conf/agent.service
sudo ln -s $PWD/conf/agent.service /etc/systemd/system/agent.service
sudo systemctl daemon-reload
echo "Done!"
