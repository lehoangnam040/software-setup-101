# Deploy Elastic search

https://www.elastic.co/guide/en/elasticsearch/reference/8.5/docker.html

- Pull image
```
docker pull docker.elastic.co/elasticsearch/elasticsearch:8.5.0
```

- Run on server that run elasticsearch
```
$ echo "vm.max_map_count=262144" | sudo tee -a /etc/sysctl.conf
```

```
$ sudo mkdir -p /mnt/es-data
$ sudo chmod g+rwx /mnt/es-data
$ sudo chgrp 0 /mnt/es-data
```