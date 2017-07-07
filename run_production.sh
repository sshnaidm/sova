#!/bin/bash
MOUNT_DIR=$1
if [[ -z "$MOUNT_DIR" || ! -d "$MOUNT_DIR" ]]; then
    echo "Please provide working directory as argument"
    exit 1
fi

docker run --name cistatus -v $1:/cidata:z -d -p 8000:8090 dockerhub.io/sshnaidm/sova -p
