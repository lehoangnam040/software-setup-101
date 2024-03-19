## Build and run nexus

```
$ docker build -t my-nexus3:3.59.0 .
```

```
$ mkdir -p ./nexus-data/etc/
$ sudo vim ./nexus-data/etc/nexus.properties
application-port-ssl=8443
nexus-args=${jetty.etc}/jetty.xml,${jetty.etc}/jetty-http.xml,${jetty.etc}/jetty-requestlog.xml,${jetty.etc}/jetty-https.xml

$ chown -R 200 ./nexus-data/
$ docker compose up -d
```

## Edit /etc/hosts
```
$ sudo vim /etc/hosts
...
127.0.0.1       nexus.local
```

## Setup cert local

```
$ docker exec -it -u root:root nexus3 bash
[root@5d6f58562699 sonatype]# keytool -printcert -sslserver nexus.local:8443 -rfc > nexus.crt
[root@5d6f58562699 sonatype]# cat nexus.crt

$ cd /usr/local/share/ca-certificates/
$ sudo vim nexus_local.crt # from nexus.crt above

$ sudo update-ca-certificates
Updating certificates in /etc/ssl/certs...
rehash: warning: skipping ca-certificates.crt,it does not contain exactly one certificate or CRL
1 added, 0 removed; done.
Running hooks in /etc/ca-certificates/update.d...
done.
```

## Test apt without trusted=yes
```
$ sudo vim /etc/apt/sources.list.d/registry-local-test.list
deb [arch=amd64] https://nexus.local:8443/repository/apt-test/ bionic main

$ sudo vim /etc/apt/auth.conf.d/registry-local-test.conf
machine nexus.local:8443
login admin 
password ...

$ sudo apt-get update
Get:1 https://nexus.local:8443/repository/apt-test bionic InRelease [1.365 B]
Get:2 https://nexus.local:8443/repository/apt-test bionic/main amd64 Packages [761 B]
```

## Test docker https with insecure-registry
```
$ docker login nexus.local:9443
Username: admin
Password: ...
WARNING! Your password will be stored unencrypted in /home/ubuntu/.docker/config.json.
Configure a credential helper to remove this warning. See
https://docs.docker.com/engine/reference/commandline/login/#credentials-store
Login Succeeded

$ docker pull
$ docker push
```

## Ref
- https://github.com/atSistemas/docker-nexus3-ssl
- https://shashanksrivastava.medium.com/how-to-secure-sonatype-nexus-using-a-self-signed-certificate-use-it-as-a-secure-docker-registry-dbea20556300
- https://github.com/rwibawa/nexus3
- https://support.sonatype.com/hc/en-us/articles/217542177-Using-Self-Signed-Certificates-with-Nexus-Repository-and-Docker-Daemon