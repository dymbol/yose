yose (Comes from spanish "yo sé" -> I know)

Status page generated statically (by cron for example)

Simple status page of:
  - services
  - websites
  - backup

External tools:
  - generates Prometheus metrics
  - notifies Zabbix

Used technolgies:
  - Python3
  - jinja2
  - bootstrap  

Example cron:
  - /usr/local/bin/pipenv run generate.py  

Current look:

![alt text](https://dymbol.github.io/yose.png)

Visual concept is based on: https://demo.cachethq.io/
