#!/usr/bin/python
# -*- coding: utf-8 -*-
import random
def naive_solution(solution, warehouseCount,customerCount,warehouses,customerSizes,customerCosts, capacityRemaining):
	
	warehouseIndex = 0
	for c in range(0, customerCount):
		if capacityRemaining[warehouseIndex] >= customerSizes[c]:
			solution[c] = warehouseIndex
			capacityRemaining[warehouseIndex] -= customerSizes[c]
		else:
			warehouseIndex += 1
			assert capacityRemaining[warehouseIndex] >= customerSizes[c]
			solution[c] = warehouseIndex
			capacityRemaining[warehouseIndex] -= customerSizes[c]
	return (solution, capacityRemaining)


def one_switch(solution, warehouseCount,customerCount,warehouses,customerSizes,customerCosts, capacityRemaining):

	usage_count = dict()   ### Keeping track of which warehouses are used.
	for i in range(warehouseCount): usage_count[i] = 0
	for i in solution: usage_count[i] += 1

	###this setup seems to be hurting my later solution... o.O;;
	for iteration in range(3): #just in case a new place opens up that's better...
		for c in xrange(customerCount):
			cust = customerCosts[c]
			current_cost = cust[solution[c]]
			if usage_count[solution[c]] == 1:
				current_cost += warehouses[solution[c]][1]

			for w in xrange(warehouseCount):
				new_cost = cust[w] + (warehouses[w][1] if usage_count[w] == 0 else 0)
				if new_cost <  current_cost+1 and capacityRemaining[w] > customerSizes[c]:
					capacityRemaining[solution[c]] += customerSizes[c]
					solution[c] = w
					capacityRemaining[w] -= customerSizes[c]
					usage_count[w] +=1
					#print "Improvement from moving", c, "to", w
	return solution, capacityRemaining, usage_count

def swap_pairs(solution, warehouseCount,customerCount,warehouses,customerSizes,customerCosts, capacityRemaining, usage_count):
	for c1 in range(customerCount):
		for c2 in range(c1):
			if min(capacityRemaining) < 0: break
			#print c1,c2
			if (customerCosts[c1][solution[c2]] + customerCosts[c2][solution[c1]] - random.random() >=  \
			   customerCosts[c1][solution[c1]] + customerCosts[c2][solution[c2]]): 
				continue
			if capacityRemaining[solution[c1]] + customerSizes[c1] - customerSizes[c2] >= 0 and \
			   capacityRemaining[solution[c2]] + customerSizes[c2] - customerSizes[c1] >= 0:
				capacityRemaining[solution[c1]] += customerSizes[c1] - customerSizes[c2]
				capacityRemaining[solution[c2]] += customerSizes[c2] - customerSizes[c1]
				solution[c1],solution[c2] = solution[c2],solution[c1]

				used = [0]*warehouseCount
				for wa in solution:
					used[wa] = 1

				# calculate the cost of the solution
				obj = sum([warehouses[x][1]*used[x] for x in range(0,warehouseCount)])
				for c in range(0, customerCount):
					obj += customerCosts[c][solution[c]]
				#print "improvement?", c1, c2, obj ,customerCosts[c1][solution[c2]] + customerCosts[c2][solution[c1]] - customerCosts[c1][solution[c1]] - customerCosts[c2][solution[c2]]  # to see the amount of gain we've made.
	return solution, capacityRemaining, usage_count


def best_guess_placing(solution, warehouseCount,customerCount,warehouses,customerSizes,customerCosts, capacityRemaining, usage_count):
	for iteration in range(100):
		improved = False
		improvements = []
		for w in range(warehouseCount):  # Find out where we can put each customer that's the best. Computing expected gain.
			improvements += [[0] * customerCount]
			for c in xrange(customerCount):
				if solution[c] == -1: improvements[w][c] = 10**6 - customerCosts[c][w]  #put people who haven't been placed yet first.
				elif solution[c] == w:
					improvements[w][c] = 0
					continue
				else: improvements[w][c] = customerCosts[c][solution[c]] - customerCosts[c][w] 
				improvements[w][c] = max(improvements[w][c],0)
		order = range(warehouseCount)
		random.shuffle(order)	
		for w in order: #xrange(warehouseCount-1,-1,-1):
			warehouse = improvements[w]
			warehouse_gain = sum(warehouse)
			if usage_count[w] == 0: warehouse_gain -= warehouses[w][1]  #If nobody's using that warehouse yet, we need to open it.
			if warehouse_gain > warehouses[w][1]:
				improv = [(improvements[w][c],c) for c in range(customerCount)]
				improv.sort()
				improv = improv[::-1]

				for c in xrange(customerCount):
					if warehouse[improv[c][1]] == 0: #Once we stop seeing improvement, quit
						break
					if capacityRemaining[w] > customerSizes[improv[c][1]]: #We can't do anything if we can't fit it... =/
						improved = True
						if solution[improv[c][1]] != -1:
							usage_count[solution[improv[c][1]]] -= 1
							capacityRemaining[solution[improv[c][1]]] += customerSizes[improv[c][1]]
						usage_count[w] += 1
						solution[improv[c][1]] = w
						capacityRemaining[w] -= customerSizes[improv[c][1]]
				if improved: break
		
		used = [0]*warehouseCount
		for wa in solution:
			used[wa] = 1

		# calculate the cost of the solution
		obj = sum([warehouses[x][1]*used[x] for x in range(0,warehouseCount)])
		for c in range(0, customerCount):
			obj += customerCosts[c][solution[c]]
		#print iteration, obj, sum([(1 if c == -1 else 0) for c in solution]) # to see the amount of gain we've made.
	
		if not improved:
			break
	return solution, capacityRemaining, usage_count, obj

def solveIt(inputData):
	# Modify this code to run your optimization algorithm

	# parse the input
	lines = inputData.split('\n')

	parts = lines[0].split()
	warehouseCount = int(parts[0])
	customerCount = int(parts[1])

	warehouses = []
	for i in range(1, warehouseCount+1):
		line = lines[i]
		parts = line.split()
		warehouses.append((int(parts[0]), float(parts[1])))

	customerSizes = []
	customerCosts = []

	lineIndex = warehouseCount+1
	for i in range(0, customerCount):
		customerSize = int(lines[lineIndex+2*i])
		customerCost = map(float, lines[lineIndex+2*i+1].split())
		customerSizes.append(customerSize)
		customerCosts.append(customerCost)

	###################################################
	############Problem solving start #################
	###################################################


	""" Variables:
	warehouseCount, customerCount
	warehouses (capacity, costs per warehouse)
	customerSizes (demand/customer)
	customerCosts (cost to go to each warehouse)
	"""

	best_solution_val = float('inf')
	for iteration in range(100):

		solution = [-1] * customerCount
		capacityRemaining = [w[0] for w in warehouses]
		usage_count = dict()   ### Keeping track of which warehouses are used.
		for i in range(warehouseCount): usage_count[i] = 0

		solution, capacityRemaining, usage_count,obj = best_guess_placing(solution, warehouseCount,customerCount,warehouses,customerSizes,customerCosts, capacityRemaining, usage_count)
		print "Step 1 done"
		#solution, capacityRemaining, usage_count = swap_pairs(solution, warehouseCount,customerCount,warehouses,customerSizes,customerCosts, capacityRemaining, usage_count)
				   
		solution, capacityRemaining, usage_count = one_switch(solution, warehouseCount,customerCount,warehouses,customerSizes,customerCosts, capacityRemaining)
		print "Step 2 done", iteration, best_solution_val
		
		if min(capacityRemaining) < 0: print "ERROR", iteration, capacityRemaining	
		if obj < best_solution_val:
			best_solution_val = obj
			best_sol = solution
			print obj, iteration
		if iteration % 128 == 0: print iteration

	solution = best_sol

	###################################################
	################  Problem solving end    ##########
	###################################################

	used = [0]*warehouseCount
	for wa in solution:
		used[wa] = 1

	# calculate the cost of the solution
	obj = sum([warehouses[x][1]*used[x] for x in range(0,warehouseCount)])
	for c in range(0, customerCount):
		obj += customerCosts[c][solution[c]]

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
		print 'Solving:', fileLocation
		print solveIt(inputData)
	else:
		print 'This test requires an input file. Please select one from the data directory. (i.e. python solver.py ./data/wl_16_1)'

