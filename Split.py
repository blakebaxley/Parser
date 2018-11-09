#!/usr/bin/python

import sys

if len(sys.argv) != 2 or sys.argv[1] not in ("b","t","a"):
	print("\x1b[0;30;43m"
		"How to use the Slow Query Log Shard Split Parser:\n" 
		"The Shard Split Parser will attempt to split the accounts that appear in the Slow Query Log into 2 roughly equal shards based on one of two attributes.\n"
		"You can choose which of the following attributes to split by by passing one of the following command line arguments\n"
		"b: Split by total bytes_sent\n"
		"t: Split by total query_time\n"
		"a: If niether of the other options looks good, this will return all accounts and let you decide."
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
	
	def Distribute(Totals):
		Shards = [[] for i in range(2)]
		Measurement = [[0, i] for i in range(2)]
		for item in Totals:
			idx = Measurement[0][1]
			Shards[idx].append(item)
			Measurement[0][0] += item[1]
			Measurement = sorted(Measurement)
		return Shards
	
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
	
	if sys.argv[1] is "t":
		TimeLst = []
		
		for account in Totals:
			TimeTup = (account.accountid, account.time)
			TimeLst.append(TimeTup)
		
		SplitShards = Distribute(TimeLst)
		
		ShardId = 1
		for shard in SplitShards:
			CPUTime = sum(x[1] for x in shard)
			print("\nAccounts for Shard %s" % (ShardId))
			print([x[0] for x in shard])
			print("Total CPU Time for shard:  %s" % (CPUTime) )
			ShardId += 1

	if sys.argv[1] is "b":
		ByteLst = []
		
		for account in Totals:
			ByteTup = (account.accountid, account.bytes)
			ByteLst.append(ByteTup)
		
		SplitShards = Distribute(ByteLst)
		
		ShardId = 1
		for shard in SplitShards:
			TotBytes = sum(x[1] for x in shard)
			print("\nAccounts for Shard %s" % (ShardId))
			print([x[0] for x in shard])
			print("Total Bytes Sent for shard:  %s" % (TotBytes) )
			ShardId += 1

	if sys.argv[1] is "a":
		print(Totals)
		