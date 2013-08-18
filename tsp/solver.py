#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
from heapq import *
import resource
resource.setrlimit(resource.RLIMIT_AS, (2**32, 2**32))
import random

def length(point1, point2):
	return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def distance(points):
	dist = dict()
	for i in xrange(len(points)):
		for j in xrange(i+1):
			d = length(points[i],points[j])
			dist[(i,j)] = d
			dist[(j,i)] = d
	return dist

def kruskal(points, nodeCount): #returns a list of the MST edges.
	mst = [] #initializing the priority queue, grabbing all the first items first.
	seen = set([0])
	heap = []
	for i in xrange(1,nodeCount):
		heappush(heap, (length(points[0],points[i]),'0',str(i)))

	while len(seen) != nodeCount:
		item = heappop(heap)
		val,start,end = item
		start, end = int(start), int(end)
		if end not in seen:
			for i in xrange(0,nodeCount):
				if i != end and i not in seen:
					heappush(heap, (length(points[end],points[i]),str(end),str(i)))
			seen.add(end)
			mst+= [(start,end)]
	return mst


def get_approx_sol(points, nodeCount):
	mst = kruskal(points, nodeCount)

	desc = dict()
	for i in xrange(nodeCount):
		desc[i] = [] 

	for edge in mst:
		desc[edge[0]] += [edge[1]]
	solution,stacks = [0], [0]
	while len(solution) < nodeCount:
		if len(desc[stacks[-1]]) == 0:
			stacks.pop()
			continue
		new_val = desc[stacks[-1]].pop()
		stacks.append(new_val)
		solution.append(new_val)
	return solution

def greedy(points, nodeCount,dist): #NOTE, this code doesn't currently work T.T... sigh greedy algorithm fail.
	heap = []
	for i in xrange(nodeCount):
		for j in xrange(i):
			heappush( heap, (  dist[(i,j)] , str(i), str(j) ) ) 
	seen = [0] * nodeCount
	count = 0
	edge_dict = dict()
	for i in xrange(nodeCount):
		edge_dict[i] = []

	while count < nodeCount:
		item = heappop(heap)
		val, i,j = item
		i,j = int(i),int(j)
		if seen[i] < 2 and seen[j] < 2:
			edge_dict[i].append(j)
			edge_dict[j].append(i)
			seen[i] +=1
			seen[j] +=1
			count +=1
			print i,j, count, seen
	print edge_dict
	solution = [0]
	seen = set([0])
	while len(solution) < nodeCount:
		m,n = edge_dict[solution[-1]]
		if m not in seen: solution.append(m)
		else: solution.append(n)
	return solution

def nearest_neighbor(points, nodeCount):
	solution = [0]
	seen = set([0])
	while len(solution) < nodeCount:
		min_num = -1
		min_val = float('inf')
		for i in xrange(nodeCount):
			if i in seen:
				continue
			if length(points[solution[-1]],points[i]) < min_val:
				min_val = length(points[solution[-1]],points[i]) # dist[(solution[-1],i)]
				min_num = i
		print len(solution)
		solution.append(min_num)
		seen.add(min_num)
	
	return solution

def two_change(solution,points, dist):
	edge_dict = dict()
	for i in xrange(len(solution)-1):
		edge_dict[solution[i]] = solution[i+1]
	edge_dict[solution[-1]] = solution[0]
	
	improved = True 
	while improved:
		improved = False
		for i in xrange(len(solution)):
			for j in xrange(i+1,len(solution)):
 				if len(set([i, j, edge_dict[i],edge_dict[j]])) < 4:
					continue 

				e1,e2 = (i,edge_dict[i]),(j,edge_dict[j])
				n1,n2 = (e1[0],e2[0]), (e1[1],e2[1])

				cur_dist = dist[e1] + dist[e2]
				new_dist = dist[n1] + dist[n2]
				if cur_dist <= new_dist:
					continue

				next_val = edge_dict[e1[1]]
				temp = e1[1]
				old_temp = e1[1]
				while next_val != e2[0]:
					temp = edge_dict[next_val]
					edge_dict[next_val] = old_temp
					old_temp = next_val
					next_val = temp
				edge_dict[next_val] = old_temp
				edge_dict[n1[0]] = n1[1]
				edge_dict[n2[0]] = n2[1]
				improved = True
				break
			if improved:
				break
	solution = [0]
	while edge_dict[solution[-1]] != 0:
		solution.append(edge_dict[solution[-1]])
	return solution 


def solveIt(inputData):
	# Modify this code to run your optimization algorithm

	# parse the input
	lines = inputData.split('\n')

	nodeCount = int(lines[0])

	points = []
	for i in range(1, nodeCount+1):
		line = lines[i]
		parts = line.split()
		points.append((float(parts[0]), float(parts[1])))

	#-------------------------Don't need to worry about anything above this line-------------#

	if len(points) < 2000:

		dist = distance(points)
		solution = get_approx_sol(points, nodeCount)[::-1]
		solution = two_change(solution,points, dist) 
		best_obj = sum([dist[(solution[i],solution[i+1])] for i in xrange(nodeCount-1)]) + dist[(solution[0],solution[-1])]
		best_sol = solution[:]
		print solution, best_obj
		iters = 0
		while iters < 2000:# and best_obj > 37600:
			starter, ender, shift = nodeCount/4, nodeCount/3, (iters*17 + iters**2/4)%nodeCount
			solution = best_sol[shift:] + best_sol[:shift]
			part = solution[starter:ender]
			random.shuffle(part)
			solution = solution[:starter] + part + solution[ender:]
			solution = two_change(solution,points, dist)
			obj = sum([dist[(solution[i],solution[i+1])] for i in xrange(nodeCount-1)]) + dist[(solution[0],solution[-1])]
			if obj < best_obj:
				best_obj = obj
				best_sol = solution[:]
				print "IMPROVEMENT UNLOCKED!!!", obj 
			iters +=1
			print obj, iters, best_obj

		solution = best_sol
	else:
		solution = nearest_neighbor(points, nodeCount) #range(nodeCount)
		best_obj = sum([length(points[solution[i]],points[solution[i+1]]) for i in xrange(nodeCount -1)]) + length(points[solution[0]],points[solution[-1]])

	################################################### Going to try switching sets of two edges around.

	obj = best_obj

	# prepare the solution in the specified output format
	outputData = str(obj) + ' ' + str(0) + '\n'
	outputData += ' '.join(map(str, solution))

	return outputData


import sys
if __name__ == '__main__':
	if len(sys.argv) > 1:
		fileLocation = sys.argv[1].strip()
		inputDataFile = open(fileLocation, 'r')
		inputData = ''.join(inputDataFile.readlines())
		inputDataFile.close()
		#start = time.time()
		print solveIt(inputData)[:50]
	else:
		print 'This test requires an input file. Please select one from the data directory. (i.e. python solver.py ./data/tsp_51_1)'

