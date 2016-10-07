#!/bin/bash
source ../venv/bin/activate
rq worker -u redis://redistogo:436473da6c8d57832bbf8ac3235490a0@sculpin.redistogo.com:10283
