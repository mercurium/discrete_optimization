#!/usr/bin/python
# -*- coding: utf-8 -*-
import random
generating = True 

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
		edges.append((int(parts[0]), int(parts[1])))

	#creating a dictionary of edges. edge_set[i] = set of nodes that i shares an edge with
	edge_set = dict()
	for i in xrange(nodeCount): edge_set[i] = set()
	for edge in edges:
		edge_set[edge[0]].add(edge[1])
		edge_set[edge[1]].add(edge[0])

	#Since sometimes we get better results with random lsts, generate new ones for good luck... lol
	if generating:
		lst = range(nodeCount)	
		random.shuffle(lst)
	else:
		lst = range(nodeCount)
 

	for dist in xrange(10,min(200,nodeCount),20): #group the nodes that have the most similar edges first
		for j in lst:#xrange(nodeCount-1,0,-1):
			if type(edge_set[j]) == type(3): #if we merged in this node, skip it
				continue
			for i in xrange(j):
				#neither node, i or j have been merged (shows if it's an int)
				# also they are not a part of each other's edge set.
				if type(edge_set[i]) != type(3) and len(edge_set[i]^edge_set[j]) <dist \
				 and i not in edge_set[j] and j not in edge_set[i]: 
					#the following line to see which nodes get merged together
#					print i,j, 'halloooo', len(edge_set[i]^edge_set[j]) 
					edge_set[i] = edge_set[i].union(edge_set[j]) #all edges get added
					edge_set[j] = i #node j disappears, gets merged into i.

					#for other nodes, add i to adjacent node list
					for k in xrange(nodeCount): 
						if type(edge_set[k]) != type(3) and j in edge_set[k]:
							edge_set[k].add(i)
					break
	
	solution = [0] * nodeCount
	color = 0
	for i in xrange(nodeCount): #only increment color for those that are not merged in
		if type(edge_set[i]) == type(set([1])):
			solution[i] = color
			color +=1
		else: #for other nodes that were merged, they get the color that they were merged into.
			solution[i] = solution[edge_set[i]]

	if generating: #if we're randomly guessing order, print out the list
		print lst

	#boiler plate provided output.
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

