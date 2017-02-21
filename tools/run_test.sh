#!/bin/bash
TESTPATH=`dirname $(readlink -f $0)`
PATH=$PATH:.
xvfb-run -e error.log python selenium-kibana/kibana_test.py --ip 192.168.33.51
