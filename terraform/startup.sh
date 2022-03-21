#!/bin/bash
exec > >(tee /var/log/user-data.log|logger -t user-data -s 2>/dev/console) 2>&1
cd /home/ec2-user/
yum update -y
sudo -u ec2-user curl -O https://bootstrap.pypa.io/get-pip.py
sudo -u ec2-user python3 get-pip.py --user
yum install git -y
sudo -u ec2-user git clone https://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@github.com/Elias-Strauss/fast-flat-bot.git
sudo -u ec2-user ./.local/bin/pip install -r fast-flat-bot/requirements.txt
sudo -u ec2-user nohup python3 fast-flat-bot/main.py &