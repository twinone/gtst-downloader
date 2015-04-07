#!/bin/bash

# Checks time in Amsterdam (CEST)
# I know it's ugly. Sorry.
curl -s http://www.timeanddate.com/time/zones/cest |grep "CEST time now" -A5|grep hrmn|cut -d">" -f3|cut -d"<" -f1
