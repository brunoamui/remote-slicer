import argparse as ap

cfg_dict = {"redis": {"host": 'redis-15555.c10.us-east-1-2.ec2.cloud.redislabs.com',
                      "port": 15555,
                      "password": "passtest"}}

cfg = ap.Namespace(**cfg_dict)
