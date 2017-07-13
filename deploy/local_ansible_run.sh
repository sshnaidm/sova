#!/bin/bash
CUR_DIR=$(dirname ${BASH_SOURCE[0]:-$0})
ansible-playbook -i "localhost," -c local $CUR_DIR/playbook.yml -vv
