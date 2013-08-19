#!/usr/bin/python
# -*- coding: utf-8 -*-
import random
import time
import sys
call_count = 0
lim = 17
clique_size = 12
sys.setrecursionlimit(1500)

def branch_and_bound(pos, solution, nodeCount, edge_dict, order, lim):
	
	global call_count
	call_count += 1
	if call_count %1024 == 0:
		print call_count
	largest_seen = max(solution)
	if largest_seen  < lim and min(solution) >= 0:  #the done case =P
		return solution 
	if largest_seen >= lim:  #if we got bigger than we wanted...
		return -1
	

	for i in xrange(nodeCount):
		if solution[i] == -1:
			set_check = set([solution[c] for c in edge_dict[i]])
			set_check.add(-1)
			if set_check == set(range(-1,largest_seen+1)):
				largest_seen +=1
				if largest_seen == lim:
					return -1
				solution[i] = largest_seen
				print "will shortcut later", pos


	next_val = order[pos]
	
	if solution[next_val] != -1:
		return branch_and_bound(pos+1,solution, nodeCount,edge_dict,order,lim)
	
	temp_set = set([ solution[c] for c in edge_dict[next_val]])
	
	for color in xrange(largest_seen+2):
		if color not in temp_set:
			new_sol = solution[:]
			new_sol[next_val] = color
			ans = branch_and_bound(pos+1,new_sol, nodeCount,edge_dict,order, lim)
			if ans != -1:
				return ans
	
	return -1   #none of the colors above work for it...

def find_clique(sol,nodeCount, eds, size, items, order):
	if size == len(items):
		return sol, items
	next_sol = sol[:]
	for i in order[len(items):]: 
		if sum([(1 if i in eds[item] else 0) for item in items]) == len(items):
			next_sol[i] = len(items)
			new_items = set(items)
			new_items.add(i)
			ans = find_clique(next_sol, nodeCount, eds, size, new_items, order)
			if ans != -1:
				return ans
	return -1


def solveIt(inputData):
	START = time.time()
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
	eds = dict()
	for i in xrange(nodeCount): edge_dict[i] = set()
	for edge in edges:
		edge_dict[edge[0]].add(edge[1])
		edge_dict[edge[1]].add(edge[0])

	for i in xrange(nodeCount):
		edge_dict[i] = sorted(list(edge_dict[i]))
		eds[i] = set(edge_dict[i])
	###################################################################
	#########  Above this is creating the dictionary of edges... ######
	###################################################################

	
	global lim, call_count, clique_size



	connection_amount = [(len(eds[i]),i) for i in range(nodeCount)]
	connection_amount.sort()
	connections = [x[1] for x in connection_amount[::-1]]


	solution = [-1] * nodeCount
	solution, clique = find_clique(solution, nodeCount, eds, clique_size, set(), connections)
	print solution
	print clique


	connection_val = []
	for i in xrange(nodeCount):
		if solution[i] != -1:
			connection_val.append( (nodeCount*clique_size,i))
		else:
			connectivity = sum([ max(0,min(solution[a],1)) for a in edge_dict[i] ])
			connection_val.append( (connectivity, i))

	connection_val.sort()
	connection_val = connection_val[::-1]
	print "connection values:", connection_val, '\n'
	order = [x[1] for x in connection_val]
	print "order", order, '\n'
	solution = branch_and_bound(0, solution, nodeCount, edge_dict, order, lim) 

	print "solution:", solution, '\n'
	print "We made:", call_count, "calls in total"
	print "This one took us:", time.time() - START



	#############################################################
	################  Below this is just processing #############
	#############################################################

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

