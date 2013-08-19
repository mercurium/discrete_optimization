#!/usr/bin/python
# -*- coding: utf-8 -*-
import random
def solveIt(inputData):
	# Modify this code to run your optimization algorithm

	# parse the input
	lines = inputData.split('\n')

	firstLine = lines[0].split()
	nodeCount = int(firstLine[0])
	edgeCount = int(firstLine[1])

	edges = []
	for i in range(1, edgeCount + 1):
		line = lines[i]
		parts = line.split()
		edges.append((int(parts[0]), int(parts[1]))) #end of boiler plate input parsing

	#creating a dictionary of edges. edge_dict[i] = set of nodes that i shares an edge with
	edge_dict = dict()
	for i in xrange(nodeCount): edge_dict[i] = set()
	for edge in edges:
		edge_dict[edge[0]].add(edge[1])
		edge_dict[edge[1]].add(edge[0])

	for i in xrange(nodeCount):
		edge_dict[i] = sorted(list(edge_dict[i]))
	###################################################################
	#########  Above this is creating the dictionary of edges... ######
	###################################################################


	solution = [-1] * nodeCount
	if generating:
		lst = range(nodeCount)
		random.shuffle(lst)
	else:
		lst = range(nodeCount) 

	for i in lst: 
		temp_set = set()
		for j in xrange(len(edge_dict[i])):
			temp_set.add(solution[edge_dict[i][j]])
		for color in xrange(nodeCount):
			if color not in temp_set:
				solution[i] = color
				break

	#print lst
	"""boiler plate provided output."""
	# prepare the solution in the specified output format
	outputData = str(max(solution)+1) + ' ' + str(0) + '\n'
	outputData += ' '.join(map(str, solution))
	return outputData


import sys

if __name__ == '__main__':
	if len(sys.argv) > 1:
		fileLocation = sys.argv[1].strip()
		inputDataFile = open(fileLocation, 'r')
		inputData = ''.join(inputDataFile.readlines())
		inputDataFile.close()
		print solveIt(inputData)
		print
	else:
		print 'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)'

