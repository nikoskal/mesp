# Mobile Enviromental Sensing Platform (MESP)

## Prerequisites
The service is intended to run on Raspian Stretch (ver > 9.0)

It can also run without Kafka support on Raspbian Jessie

## Requirements
- python2.7
- pip

## Install
You need to have installed systemd [1] on your system

```
$ ./install.sh
```

## Enable autostart
```
# systemctl enable agent.service
```
