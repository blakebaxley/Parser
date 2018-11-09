#!/usr/bin/python

# Import RegEx module
import re 
from decimal import Decimal

class QueryLog:
	def __init__(self, account_id, query_time, io_bytes, query, locked, rows):
		self.account = account_id
		self.time = query_time
		self.bytes = io_bytes
		self.query = query
		self.locktime = locked
		self.rows = rows

	def __str__(self):
		return "\nAccount %s ran a query that took %s and sent %s bytes" % (self.account, self.time, self.bytes)

	def __repr__(self):
		return str(self)

# Get log file to work on
file = input("Which file do you want to parse?   ")
Logfile = open(file, "r")
# Perform filtering in the log file
Logs = Logfile.read().split('# Time:')
Queries = []
for Log in Logs: 
	accnt = 0
	qtime = 0
	byte = 0
	query = 0
	locked = 0
	rows = 0
	Log = Log.split("  ")
	for Line in Log:
		
		acct = re.search('(?<=accountId=)(.*?\s)', Line)
		if acct is not None:
			accnt = int(acct.group(1))
			query = Line
		qt = re.search('(?<=Query_time:)(.*)', Line)
		if qt is not None:
			qtime = Decimal(qt.group(1))
		bt = re.search('(?<=Bytes_sent:)(.*)', Line)
		if bt is not None:
			byte = int(bt.group(1))
		lk = re.search('(?<=Lock_time:)(.*)', Line)
		if lk is not None:
			locked = Decimal(lk.group(1))
		ex = re.search('(?<=Rows_examined:)(.*)', Line)
		if ex is not None:
			rows = int(ex.group(1))
	
	if accnt is not 0:
		 Queries.append(QueryLog(accnt, qtime, byte, query, locked, rows))
		
			
