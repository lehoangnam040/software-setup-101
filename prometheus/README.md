## Setup mount volumes

```
sudo rm -rf /mnt/prometheus-data
sudo mkdir -p /mnt/prometheus-data
sudo chown 65534:65534 /mnt/prometheus-data
```

```
sudo rm -rf /mnt/alertmanager-data
sudo mkdir -p /mnt/alertmanager-data
sudo chown 65534:65534 /mnt/alertmanager-data
```