#!/bin/bash

case "$1" in 
start)
   gunicorn -c /Users/zhouy/CareerFrog/hiking/code/applications/gunicorn_wsgi.conf crawling_task_wsgi:app
   ;;
stop)
   kill `cat /Users/zhouy/CareerFrog/hiking/code/applications/run/gunicorn/crawler_app.pid`
   rm /Users/zhouy/CareerFrog/hiking/code/applications/run/gunicorn/crawler_app.pid
   ;;
restart)
   $0 stop
   $0 start
   ;;
status)
   if [ -e /Users/zhouy/CareerFrog/hiking/code/applications/run/gunicorn/crawler_app.pid ]; then
      echo crawler_app is running, pid=`cat /Users/zhouy/CareerFrog/hiking/code/applications/run/gunicorn/crawler_app.pid`
   else
      echo crawler_app is NOT running
      exit 1
   fi
   ;;
*)
   echo "Usage: $0 {start|stop|status|restart}"
esac

exit 0 
