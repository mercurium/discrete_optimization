#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
import random

def length(customer1, customer2):
	return math.sqrt((customer1[1] - customer2[1])**2 + (customer1[2] - customer2[2])**2)

def distances(customers):
	dists = dict()
	for i in xrange(len(customers)):
		for j in xrange(i+1):
			dists[(i,j)] = length(customers[i],customers[j])
			dists[(j,i)] = length(customers[i],customers[j])
	return dists



def two_change(solution, dist):
	edge_dict = dict()
	for i in xrange(len(solution)-1):
		edge_dict[solution[i]] = solution[i+1]
	edge_dict[solution[-1]] = solution[0]
	
	improved = True 
	while improved:
		improved = False
		for i in edge_dict: 
			for j in edge_dict: 
				if i >= j: continue
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
	solution = solution[0:1]
	while edge_dict[solution[-1]] != solution[0]:
		solution.append(edge_dict[solution[-1]])
	return solution 


def solveIt(inputData):
	# Modify this code to run your optimization algorithm

	# parse the input
	lines = inputData.split('\n')

	parts = lines[0].split()
	customerCount = int(parts[0])
	vehicleCount = int(parts[1])
	vehicleCapacity = int(parts[2])
	depotIndex = 0

	customers = []
	for i in range(1, customerCount+1):
		line = lines[i]
		parts = line.split()
		customers.append((int(parts[0]), float(parts[1]),float(parts[2])))

	distance = distances(customers)
		#### Naive solution
	#customerIndexs = set(range(1, customerCount))  # start at 1 to remove depot index

		
	#for v in range(0, vehicleCount):
	#	# print "Start Vehicle: ",v
	#	vehicleTours.append([])
	#	capacityRemaining = vehicleCapacity
	#	while sum([capacityRemaining >= customers[ci][0] for ci in customerIndexs]) > 0:
	#		used = set()
	#		order = sorted(customerIndexs, key=lambda ci: -customers[ci][0])
	#		for ci in order:
	#			if capacityRemaining >= customers[ci][0]:
	#				capacityRemaining -= customers[ci][0]
	#				vehicleTours[v].append(ci)
	#				# print '   add', ci, capacityRemaining
	#				used.add(ci)
	#		customerIndexs -= used

	##################################################
	###########                      #################
	########### Problem solving Start#################
	###########                      #################
	##################################################

	# build a trivial solution
	# assign customers to vehicles starting by the largest customer demands

	best_seen = float('inf')
	error_count = 0
	for iteration in xrange(500000):
		vehicleTours = []
		for v in range(vehicleCount):
			vehicleTours.append([])
		capacityRemaining = [vehicleCapacity] * vehicleCount

		seen = set()
		for vehicle in range(len(vehicleTours)):
			next_loc = random.randint(1,customerCount-1)
			while next_loc in seen:
				next_loc = random.randint(1,customerCount-1)
			vehicleTours[vehicle].append(next_loc)
			capacityRemaining[vehicle] -= customers[next_loc][0]		
			seen.add(next_loc)

		
		not_visited = set(range(1,customerCount)).difference(seen)
		not_visited = list(not_visited)
		random.shuffle(not_visited)
		for city in not_visited:
			min_dist = float('inf')
			min_vehicle = -1 
			for vehicle in range(vehicleCount):
				if capacityRemaining[vehicle] < customers[city][0]:
					continue
				dist = distance[(vehicleTours[vehicle][-1],city)] + distance[(city,0)] - distance[(0,vehicleTours[vehicle][-1])]
				if dist < min_dist:
					min_dist = dist
					min_vehicle = vehicle
			vehicleTours[min_vehicle].append(city)
			capacityRemaining[min_vehicle] -= customers[city][0]

		if iteration % 1024 == 0:
			print iteration

		if min(capacityRemaining) < 0:
			error_count +=1
			continue






		############################################################
		################## Optimizing each cycle        ############
		############################################################
		for tour in xrange(len(vehicleTours)):
			vehicleTours[tour] = two_change(vehicleTours[tour],distance)
			best_obj = sum([distance[(vehicleTours[tour][i],vehicleTours[tour][i+1])] for i in xrange(len(vehicleTours[tour])-1)]) + distance[(vehicleTours[tour][0],vehicleTours[tour][-1])]
			best_vehicle_sol = vehicleTours[tour][:]
			iters = 0
			while iters < 50:
				starter, ender, shift = len(vehicleTours[tour])/4, len(vehicleTours[tour])/2, (iters*17 + iters**2/4)%len(vehicleTours[tour])
				vehicleTours[tour] = best_vehicle_sol[shift:] + best_vehicle_sol[:shift]
				part = vehicleTours[tour][starter:ender]
				random.shuffle(part)
				vehicleTours[tour] = vehicleTours[tour][:starter] + part + vehicleTours[tour][ender:]
				vehicleTours[tour] = two_change(vehicleTours[tour], distance)
				obj = sum([distance[(vehicleTours[tour][i],vehicleTours[tour][i+1])] for i in xrange(len(vehicleTours[tour])-1)]) + distance[(vehicleTours[tour][0],vehicleTours[tour][-1])]
				if obj < best_obj:
					best_obj = obj
					best_vehicle_sol = vehicleTours[tour][:]
			#		print "IMPROVEMENT UNLOCKED!!!", obj 
				iters +=1
			#	print obj, iters, best_obj

			vehicleTours[tour] = best_vehicle_sol





		############################################################
		############### Compute solution cost below: ###############
		############################################################



		obj = 0
		for v in range(0, vehicleCount):
			vehicleTour = vehicleTours[v]
			if len(vehicleTour) > 0:
				obj += length(customers[depotIndex],customers[vehicleTour[0]])
				for i in range(0, len(vehicleTour) - 1):
					obj += length(customers[vehicleTour[i]],customers[vehicleTour[i + 1]])
				obj += length(customers[vehicleTour[-1]],customers[depotIndex])
		if obj < best_seen:
			print iteration, obj, [sum([customers[i][0] for i in vehicle]) for vehicle in vehicleTours], vehicleCapacity
			print [len(x) for x in vehicleTours]
			best_seen = obj
			best_sol = vehicleTours
		if best_seen < 1193:
			break

	vehicleTours = best_sol

	print "there were:", error_count, "errors... out of...", iteration + 1














	###################################################
	############  Computing Answer Value:    ##########
	###################################################







	# checks that the number of customers served is correct
	assert sum([len(v) for v in vehicleTours]) == customerCount - 1

	# calculate the cost of the solution; for each vehicle the length of the route
	obj = 0
	for v in range(0, vehicleCount):
		vehicleTour = vehicleTours[v]
		if len(vehicleTour) > 0:
			obj += length(customers[depotIndex],customers[vehicleTour[0]])
			for i in range(0, len(vehicleTour) - 1):
				obj += length(customers[vehicleTour[i]],customers[vehicleTour[i + 1]])
			obj += length(customers[vehicleTour[-1]],customers[depotIndex])

	# prepare the solution in the specified output format
	outputData = str(obj) + ' ' + str(0) + '\n'
	for v in range(0, vehicleCount):
		outputData += str(depotIndex) + ' ' + ' '.join(map(str,vehicleTours[v])) + ' ' + str(depotIndex) + '\n'

	return outputData


import sys


if __name__ == '__main__':
	if len(sys.argv) > 1:
		fileLocation = sys.argv[1].strip()
		inputDataFile = open(fileLocation, 'r')
		inputData = ''.join(inputDataFile.readlines())
		inputDataFile.close()
		print 'Solving:', fileLocation
		print solveIt(inputData)
	else:

		print 'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/vrp_5_4_1)'

