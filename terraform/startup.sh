#!/bin/bash
yum update -y
curl -O https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py --user
yum install git
git clone https://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@github.com/Elias-Strauss/fast-flat-bot.git
 ./.local/bin/pip install requirements.txt