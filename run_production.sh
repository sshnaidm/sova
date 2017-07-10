#!/bin/bash
MOUNT_DIR=$1
if [[ -z "$MOUNT_DIR" || ! -d "$MOUNT_DIR" ]]; then
    echo "Please provide working directory as argument"
    exit 1
fi

docker run --name cistatus -v $1:/cidata:z -d -p 80:8090 --restart always docker.io/sshnaidm/sova -p
