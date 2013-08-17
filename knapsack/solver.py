#!/usr/bin/python
# -*- coding: utf-8 -*-

import string
approx = False
import time

optimal = 0


def solveIt(inputData):
	global optimal
	start = time.time()
	# Modify this code to run your optimization algorithm

	# parse the input
	lines = inputData.split('\n')

	firstLine = lines[0].split()
	items = int(firstLine[0])
	capacity = int(firstLine[1])

	values = []
	weights = []

	for i in range(1, items+1):
		line = lines[i]
		parts = line.split()

		values.append(int(parts[0]))
		weights.append(int(parts[1]))

	#-----------------Don't need to worry about content above here ----------------

	w_v = [0]* len(values) #weight_value pairs

	#w/v, weight, value, index
	w_v = [(values[i]*1.0/weights[i], weights[i], values[i],i) for i in xrange(items)]
	w_v = sorted(w_v)[::-1][:items]

	value,weight = 0,0
	taken = [0] * len(values)



	value_temp = 0
	weight_temp = 0

	for i in xrange(0,len(w_v)):
		if weight_temp + w_v[i][1] <= capacity:
			value_temp += w_v[i][2]
			weight_temp += w_v[i][1]


	optimal = value_temp



	#takes in where we are, how much weight we've taken, value gained so far.
	def knapsack(index,value,weight): 
		global optimal
		if weight > capacity:
			return 0,[]
		else:
			optimal = max(value,optimal)
		if index == items:
			optimal = max(value,optimal)
			return value,[]
		if (capacity-weight) * w_v[index][0] + value < optimal:
			return 0,[]

		a = knapsack(index+1,value,weight)
		b,c = knapsack(index+1,value+w_v[index][2], weight+w_v[index][1])
		return max(a,(b,[index]+c))


	value,indices = knapsack(0,0,0)
	
	for i in indices:
		taken[w_v[i][3]] = 1

	print "Time Taken:", time.time() - start

	outputData = str(value) + ' ' + str(1) + '\n'
	# prepare the solution in the specified output format
	outputData += ' '.join(map(str, taken))
	return outputData


import sys
sys.setrecursionlimit(20000)

if __name__ == '__main__':
	if len(sys.argv) > 1:
		fileLocation = sys.argv[1].strip()
		inputDataFile = open(fileLocation, 'r')
		inputData = ''.join(inputDataFile.readlines())
		inputDataFile.close()
		print solveIt(inputData)
	else:
		print 'This test requires an input file.	Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)'

