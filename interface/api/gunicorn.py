#!/usr/bin/env python
user = 'www-data'
group = user

bind = '0.0.0.0:9000'
# loglevel = 'debug'
loglevel = 'info'
reload = True
workers = 1  # multiprocessing.cpu_count() * 2 + 1

def when_ready(server):
    print('Gunicorn ready!')
