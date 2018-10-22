#!/bin/bash

chmod 664 ./agent.service
PWD=$(pwd)
sudo ln -s $PWD/agent.service /etc/systemd/system/agent.service
sudo systemctl daemon-reload
