#!/bin/bash
MOUNT_DIR=$1
if [[ -z "$MOUNT_DIR" || ! -d "$MOUNT_DIR" ]]; then
    echo "Please provide working directory as argument"
    exit 1
fi

echo "Service starts on port 8000"
docker run --name cistatus --rm -it -v $1:/cidata:z -p 8000:8090 dockerhub.io/sshnaidm/sova -d
