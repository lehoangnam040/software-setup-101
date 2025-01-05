#!/bin/bash

chown 1000:1000 /defaults
sudo chown -R 1000:1000 /etc/s6-overlay/

sudo bash /etc/s6-overlay/s6-rc.d/init-nginx/run
sudo bash /etc/s6-overlay/s6-rc.d/init-video/run
sudo bash /etc/s6-overlay/s6-rc.d/init-kasmvnc-config/run

bash /etc/s6-overlay/s6-rc.d/svc-kasmvnc/run &
sudo bash /etc/s6-overlay/s6-rc.d/svc-nginx/run &
bash /etc/s6-overlay/s6-rc.d/svc-de/run &

cd /kclient
node index.js
