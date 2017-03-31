#!/bin/bash

case "$1" in 
start)
   gunicorn -c /root/crawling-task/gunicorn_wsgi.conf crawling_task_wsgi:app
   ;;
stop)
   kill `cat /var/run/gunicorn/crawler_app.pid`
   rm /var/run/gunicorn/crawler_app.pid
   ;;
restart)
   $0 stop
   $0 start
   ;;
status)
   if [ -e /var/run/gunicorn/crawler_app.pid ]; then
      echo crawler_app is running, pid=`cat /var/run/gunicorn/crawler_app.pid`
   else
      echo crawler_app is NOT running
      exit 1
   fi
   ;;
*)
   echo "Usage: $0 {start|stop|status|restart}"
esac

exit 0 