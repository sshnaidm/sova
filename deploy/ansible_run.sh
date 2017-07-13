#!/bin/bash
CUR_DIR=$(dirname ${BASH_SOURCE[0]:-$0})
ansible-playbook -i $CUR_DIR/hosts $CUR_DIR/playbook.yml -vv
