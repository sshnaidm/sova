#!/bin/bash

function install_crontab {
    pkill crond
    crontab -l > /tmp/old_crontab
    diff -q >/dev/null /app/crontab /tmp/old_crontab || cat /app/crontab | crontab -
    crond -L /cidata/logs/cron.log
}

while getopts 'hdp' flag; do
  	case "${flag}" in
        h)
            echo "options:"
            echo "-h        show brief help"
            echo "-d        debug mode, flask debug server"
            echo "-p        production mode with uwsgi"
            exit 0
        ;;
        d)
            touch /debug1
        	;;
        p)
            touch /prod
        	;;
        *)
      	    break
        ;;
  	esac
  done

mkdir -p /cidata/logs
if [ -e /debug1 ]; then
	echo "Running app in debug mode!"
	exec python flaskapp.py
elif [ -e /prod ]; then
    echo "Running app in production mode!"
    touch /cidata/index.html
    install_crontab
    exec uwsgi --ini /uwsgi.ini
else
    exec /bin/bash
fi
