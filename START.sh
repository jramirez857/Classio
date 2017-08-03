#!/bin/bash
ip=$(hostname -I)

cd /home/pi/Classio/Classio/

screen -S redis -d -m "redis-server" &

screen -S daphne -d -m "sudo" "daphne" "config_classio.asgi:channel_layer" "--port" "80" "-b" $ip &

screen -S django -d -m "python3" "manage.py" "runworker" &


