#!/bin/bash

sudo apt install -y python3.8
sudo apt install -y python3-pip
sudo -H pip3 install Django==2.2.10
sudo apt install -y python3.8-dev libmysqlclient-dev
sudo -H pip3 install mysqlclient

if [ ! -d "/etc/logfilterd" ]; then
    sudo mkdir /etc/logfilterd
fi

sudo cp rules/ /etc/logfilterd/ -r
sudo cp IDSclient/ /etc/logfilterd/ -r
sudo cp logfilterd.py /etc/logfilterd/
sudo cp logfilterd-clear.py /etc/logfilterd/
sudo cp logfilterd-runserver.py /etc/logfilterd/
sudo cp config.py /etc/logfilterd/
sudo cp logfilterd.service /etc/systemd/system
sudo cp logfilterd-clear.service /etc/systemd/system
sudo cp logfilterd-runserver.service /etc/systemd/system

python3.8 /etc/logfilterd/IDSclient/manage.py migrate

sudo systemctl daemon-reload
sudo systemctl enable logfilterd.service
sudo systemctl enable logfilterd-clear.service
sudo systemctl enable logfilterd-runserver.service
sudo systemctl start logfilterd.service
sudo systemctl start logfilterd-clear.service
sudo systemctl start logfilterd-runserver.service

python3.8 /etc/logfilterd/IDSclient/manage.py migrate
