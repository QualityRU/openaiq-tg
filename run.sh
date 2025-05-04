#!/bin/bash
screen -LRR -dmS openiq -c /etc/screenrc venv/bin/python3 main.py
echo "OpenAIQ запущен в фоне!"