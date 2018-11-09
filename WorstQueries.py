#!/usr/bin/python

import sys

if len(sys.argv) != 2 or sys.argv[1] not in ("b","l","r","t","a"):
	print("\x1b[0;30;43m"
		"How to use the Slow Query Log Worst Queries Parser:\n" 
		"The Worst Queries Parser returns the top 10 queries from the slow query log that are affecting the mysql server in one of four ways.\n"
		"You can choose which of the following attributes to sort by by passing one of the following command line arguments\n"
		"b: list the top 10 queries with the highest bytes_sent\n"
		"l: list the top 10 queries with the highest locktime\n"
		"r: list the top 10 queries with the highest number of examined rows\n"
		"t: list the top 10 queries with the highest query_time\n"
		"a: All The Lists!"
		"\x1b[0m")

else:
	
	import parser
	
	class LongQuery:
		def __init__(self, query_time, io_bytes, query, locked, rows):
			self.time = query_time
			self.bytes = io_bytes
			self.query = query
			self.locktime = locked
			self.rows = rows
	
		def __str__(self):
			return "\n Query:  %s \n Examined %s rows \n Locked rows for %s seconds \n Took %s " % (self.query, self.rows, self.locktime, self.time)
	
		def __repr__(self):
			return str(self)
	
	def TimeSort(LongQuery):
		return LongQuery.time
	
	def ByteSort(LongQuery):
		return LongQuery.bytes
	
	def LockSort(LongQuery):
		return LongQuery.locktime
	
	def RowSort(LongQuery):
		return LongQuery.rows
	
	LongQueries = []
	
	for q in parser.Queries:
		LongQueries.append(LongQuery(q.time, q.bytes, q.query, q.locktime, q.rows))
		

	if sys.argv[1] in ("l", "a"):
		print("\nTop 10 queries by Lock Time:\n")
		print(sorted(LongQueries, key=LockSort, reverse=True)[:10])
	if sys.argv[1] in ("t", "a"):
		print("\nTop 10 queries by Query Time:\n")
		print(sorted(LongQueries, key=TimeSort, reverse=True)[:10])
	if sys.argv[1] in ("b", "a"):
		print("\nTop 10 queries by Bytes Sent:\n")
		print(sorted(LongQueries, key=ByteSort, reverse=True)[:10])	
	if sys.argv[1] in ("r", "a"):
		print("\nTop 10 queries by Rows Examined:\n")
		print(sorted(LongQueries, key=RowSort, reverse=True)[:10])	
	