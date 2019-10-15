#!/bin/sh
#
# This is a script for starting wsgi service at system startup time
#
# The following file ndx_app.ini (/var/webserver/localhost)
# has to be configured properly for the  services to work.
#
#
prog=wsgi

APPLICATION_NAME=application
APPLICATION_INI_FILE=server_app.ini
DAEMONIZE=--daemonize2
LOG_TO=/var/log/serverpi/log
WSGI_USER=www-data
WSGI_GROUP=www-data
PROCESSES=5

DIR=/var/www/backend

OPTIONS="--uid $WSGI_USER --gid $WSGI_GROUP \
         --ini $APPLICATION_INI_FILE --processes $PROCESSES \
         $DAEMONIZE $APPLICATION_NAME --logto $LOG_TO"

start() {
    # We don't want uwsgi logs to accumulate, delete them at every start:
    rm -rf /var/log/serverpi
    mkdir -p /var/log/serverpi
    chown $WSGI_USER:$WSGI_GROUP /var/log/serverpi
    cd $DIR
    uwsgi $OPTIONS
    if [ $? -ne 0 ]; then
        exit 1
    fi

    exit 0
}

stop() {
    kill 9 `pidof uwsgi`
    if [ $? -ne 0 ]; then
        exit 1
    fi
}

force_reload() {
    stop
    start
}

case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    force-reload)
        force_reload
        ;;
    restart)
        stop
        start
        ;;

    *)
        echo "$Usage: $prog {start|stop|force-reload|restart}"
        exit 2
esac
