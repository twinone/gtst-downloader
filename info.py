#!/usr/bin/python

import json
import time
from datetime import datetime
from urllib2 import urlopen

MAX_OUTPUT = 5

ak = '8926'
url = 'http://www.rtl.nl/system/s4m/vfd/version=2/d=pc/output=json/ak=' + ak + '/pg=1/cf=allow%20uitzending'


def comp(a):
	return int(a['display_date'])

def daysago(timestamp):
	now = time.time()
	today = now - (now%86400) + 86400
	days = int(today-timestamp) / 86400
	if days < 0: return 'In ' + str(-days) + ' days'
	if days == 0: return 'Today'
	if days == 1: return 'Yesterday'
	return str(days) + ' days ago'


def get_data(num):
	"""Gets the latest num episodes sorted in increasing date order"""
	now = time.time()
	data = json.loads(urlopen(url).read())['material']
	data[:] = [x for x in data if x['display_date'] < now]
	data.sort(key=comp)
	data = data[-num:]
	return data

def get_last():
	return get_data(1)[0]


def print_latest(num=MAX_OUTPUT):
	"""Convenience function that lists the last num episodes"""
	data = get_data(num)
	now = time.time()
	print "-----------------------------------------------------"
	for item in data:
		ts = item['display_date']
		dt = datetime.fromtimestamp(ts)
		print "UUID:", item['uuid']
		print "Date:", dt.strftime('%a %b %d'), '('+daysago(ts)+')'
		print "-----------------------------------------------------"

if __name__ == "__main__":
	print 'Showing latest', MAX_OUTPUT, 'episodes:'
	print_latest()