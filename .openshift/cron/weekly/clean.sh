#!/usr/bin/env bash
find $OPENSHIFT_DATA_DIR -type d -mtime +30 -exec rm -rf "{}" \;