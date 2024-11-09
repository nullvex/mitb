#!/bin/bash
sudo apt -y update
sudo apt -y erlang
sudo apt -y install rabbitmq-server
sudo systemctl enable rabbitmq-server
sudo systemctl start rabbitmq-server
sudo rabbitmqctl status
sudo rabbitmq-plugins enable rabbitmq_management
