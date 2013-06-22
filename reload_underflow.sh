ps aux|grep uwsgi|awk '{print $2}'|xargs kill -9
uwsgi -H /srv/underflow.sunnykale.com/www/underflow/venv -s 127.0.0.1:9001 -M -w underflow:app -d /srv/underflow.sunnykale.com/logs/uwsgi.log
