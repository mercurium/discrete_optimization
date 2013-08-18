#!/usr/bin/python
# -*- coding: utf-8 -*-

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

	# build a trivial solution
	# pack the warehouses one by one until all the customers are served

	solution = [-1] * customerCount
	capacityRemaining = [w[0] for w in warehouses]

	warehouseIndex = 0
	#for c in range(0, customerCount):
	#	if capacityRemaining[warehouseIndex] >= customerSizes[c]:
	#		solution[c] = warehouseIndex
	#		capacityRemaining[warehouseIndex] -= customerSizes[c]
	#	else:
	#		warehouseIndex += 1
	#		assert capacityRemaining[warehouseIndex] >= customerSizes[c]
	#		solution[c] = warehouseIndex
	#		capacityRemaining[warehouseIndex] -= customerSizes[c]

	################################################### 
	############### Above is naive solution ###########
	################################################### 

	usage_count = dict()   ### Keeping track of which warehouses are used.
	for i in range(warehouseCount): usage_count[i] = 0
	#for i in solution: usage_count[i] += 1

	#this setup seems to be hurting my later solution... o.O;;
	#for iteration in range(3): #just in case a new place opens up that's better...
	#	for c in xrange(customerCount):
	#		cust = customerCosts[c]
	#		current_cost = cust[solution[c]]
	#		if usage_count[solution[c]] == 1:
	#			current_cost += warehouses[solution[c]][1]

	#		for w in xrange(warehouseCount):
	#			new_cost = cust[w] + (warehouses[w][1] if usage_count[w] == 0 else 0)
	#			if new_cost <  current_cost and capacityRemaining[w] > customerSizes[c]:
	#				solution[c] = w
	#				capacityRemaining[w] -= customerSizes[c]
	#				usage_count[w] +=1




	###################################################	
	###################################################	
	###################################################	
	
	for iteration in range(100):
		improved = False
		improvements = []
		for w in range(warehouseCount): 
			improvements += [[0] * customerCount]
			#improvements += [[ (customerCosts[c][solution[c]] - customerCosts[c][w] )  for c in range(customerCount) ] ]
			for c in xrange(customerCount):
				if solution[c] == -1:
					improvements[w][c] = 10**5 - customerCosts[c][w]
				elif solution[c] == w:
					improvements[w][c] = 0
					continue
				else:
					improvements[w][c] = customerCosts[c][solution[c]] - customerCosts[c][w] 
				improvements[w][c] = max(improvements[w][c],0)
	
		for w in xrange(warehouseCount):
			warehouse = improvements[w]
			warehouse_gain = sum(warehouse)

			if warehouse_gain > warehouses[w][1]:
				improv = [(improvements[w][c],c) for c in range(customerCount)]
				improv.sort()
				improv = improv[::-1]

				for c in xrange(customerCount):
					if warehouse[improv[c][1]] == 0:
						break
					if capacityRemaining[w] > customerSizes[improv[c][1]]:
						improved = True
						if solution[improv[c][1]] != -1: usage_count[solution[improv[c][1]]] -= 1
						usage_count[w] += 1
						solution[improv[c][1]] = w
						capacityRemaining[w] -= customerSizes[improv[c][1]]
				#print warehouse_gain, warehouses[w][1], w
				if improved: break
		
		used = [0]*warehouseCount
		for wa in solution:
			used[wa] = 1

		# calculate the cost of the solution
		obj = sum([warehouses[x][1]*used[x] for x in range(0,warehouseCount)])
		for c in range(0, customerCount):
			obj += customerCosts[c][solution[c]]
		print iteration, obj
	
		if not improved:
			break


	
















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

