#!/bin/bash
source ../venv/bin/activate
#rq worker -u redis://redistogo:436473da6c8d57832bbf8ac3235490a0@sculpin.redistogo.com:10283
rq worker -u redis://:passtest@redis-15555.c10.us-east-1-2.ec2.cloud.redislabs.com:15555/0
