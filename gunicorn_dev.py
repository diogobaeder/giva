from os import environ

from local_settings import BIND


USER = environ.get('USER')


bind = BIND
workers = 2
errorlog = "/home/{}/logs/gunicorn_giva_error.log".format(USER)
accesslog = "/home/{}/logs/gunicorn_giva_access.log".format(USER)
loglevel = "error"
proc_name = "giva"
pidfile = 'giva.pid'
