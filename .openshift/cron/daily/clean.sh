#!/usr/bin/env bash
find $OPENSHIFT_DATA_DIR -type d -mtime +20 -exec rm -rf "{}" \;