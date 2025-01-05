
### **Learning Purposes, Ongoing develop**

# Build docker image that act like a real ubuntu

## Motivation

- Using https://github.com/linuxserver/docker-webtop/ but it requires run Docker-in-Docker (Dind) which requires `privileged` that quite dangerous to me
- So I want a docker image that:
  - can run with runtime `sysbox-runc` https://github.com/nestybox/sysbox
  - have docker engine inside
  - using kasmvnc to access in browser, refer to webtop to do that

## Quickstart

- Install `sysbox-runc` (refer: https://github.com/nestybox/sysbox/blob/master/docs/user-guide/install-package.md)
- Build

```
docker buildx build --pull -t ubuntu:amd64-jammy-xfce-kasmvnc --platform=linux/amd64 --load .
```

- Run

```
docker compose up -d
```

- Start services

```
docker exec -it myubuntu bash
root@16f9cd84c169:/$ su admin
admin@16f9cd84c169:/$ /start.sh
```

- Test
  - Go to http://localhost:3000 
  - open terminal
  - try to pull and start a docker image

## Future improvement

- For now, start docker didn't start kasmvnc services -> I'll try to improve that
  - I tried s6-overlay but it requires running as PID 1 -> cannot run docker engine
