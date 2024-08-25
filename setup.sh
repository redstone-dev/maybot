#! /bin/bash

python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt

mkdir ./data
mkdir ./data/config

wget "https://redstone-dev.github.io/maybot/default.env"
cat default.env > .env
rm -f default.env

wget "https://redstone-dev.github.io/maybot/default_bot_settings.json"
cat default_bot_settings.json > ./data/config/default_settings.json
rm -f default_bot_settings.json

echo "(!) please fill in the blank values in .env and bot_settings.json to get maybot to work."
echo "... more information is available at https://github.com/redstone-dev/maybot/wiki/Initial-configuration-of-maybot"