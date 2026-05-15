#!/bin/bash

mkdir -p comandos downloads utils

pip install -q requests colorama
pip install -q git+https://github.com/PixelCrew-Team/TodLib.git

if [ ! -f "config.json" ]; then
    echo '{"phone_number": "", "password": "", "allowed_senders": [], "log_file": "bot.log"}' > config.json
fi

python3 bot.py
