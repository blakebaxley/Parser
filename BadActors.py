#!/usr/bin/python

import sys

if len(sys.argv) != 2 or sys.argv[1] not in ("b","c","t","a"):
	print("\x1b[0;30;43m"
		"How to use the Slow Query Log Bad Actor Parser:\n" 
		"The Bad Actor Parser returns the top 10 accounts from the slow query log that are affecting the mysql server in one of three ways.\n"
		"You can choose which of the following attributes to sort by by passing one of the following command line arguments\n"
		"b: list the top 10 accounts with the highest total bytes_sent\n"
		"c: list the top 10 accounts with the highest total query coutns\n"
		"t: list the top 10 accounts with the highest total query_time\n"
		"a: All The Lists!"
		"\x1b[0m")

else:

	import parser
	class AccountTotal:
		def __init__(self, account_id, count, query_time, io_bytes):
			self.accountid = account_id
			self.count = count
			self.time = query_time
			self.bytes = io_bytes
	
		def __str__(self):
			return "\nAccount %s had %s queries with a total CPU time of %s and %s total bytes sent. " % (self.accountid, self.count, self.time, self.bytes)
	
		def __repr__(self):
			return str(self)
	
	def CountSort(AccountTotal):
		return AccountTotal.count
	
	def TimeSort(AccountTotal):
		return AccountTotal.time
	
	def ByteSort(AccountTotal):
		return AccountTotal.bytes
	
	Totals = []
	iterables = {}
	for x in parser.Queries:
	    iterables.setdefault(x.account, []).append(x)
	
	for AccountID in iterables.values():
		AID = AccountID[0].account
		Count = 0
		QueryTime = 0
		BytesSent = 0
	
		for Query in AccountID:
			Count += 1
			QueryTime += Query.time
			BytesSent += Query.bytes
	
		Totals.append(AccountTotal(AID, Count, QueryTime, BytesSent))

	if sys.argv[1] in ("c", "a"):
		print("\nTop 10 accounts by Query Count:\n")
		print(sorted(Totals, key=CountSort, reverse=True)[:10])
	if sys.argv[1] in ("t", "a"):
		print("\nTop 10 accounts by Query Time:\n")
		print(sorted(Totals, key=TimeSort, reverse=True)[:10])
	if sys.argv[1] in ("b", "a"):
		print("\nTop 10 accounts by Bytes Sent:\n")
		print(sorted(Totals, key=ByteSort, reverse=True)[:10])	