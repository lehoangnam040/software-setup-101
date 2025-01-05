#!/bin/bash

sudo chown -R 1000:1000 /defaults
sudo chown -R 1000:1000 /etc/s6-overlay/

sudo bash /etc/s6-overlay/s6-rc.d/init-nginx/run
sudo bash /etc/s6-overlay/s6-rc.d/init-video/run
sudo bash /etc/s6-overlay/s6-rc.d/init-kasmvnc-config/run

bash /etc/s6-overlay/s6-rc.d/svc-kasmvnc/run &
bash /etc/s6-overlay/s6-rc.d/svc-de/run &

service nginx reload
cd /kclient
node index.js
