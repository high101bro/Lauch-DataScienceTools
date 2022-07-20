#!/bin/bash
dstools=$(curl -X GET https://hub.docker.com/v2/repositories/afcai2c)
echo $dstools | cut -d ',' -f 1-1000 | grep afcai2c
#for i in $dstools; do
#    echo $i
#done
