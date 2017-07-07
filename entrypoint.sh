#!/bin/bash

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

if [ -e /debug1 ]; then
	echo "Running app in debug mode!"
	exec python flaskapp.py
elif [ -e /prod ]; then
    echo "Running app in production mode!"
    exec uwsgi --ini /uwsgi.ini
else
    exec /bin/bash
fi
