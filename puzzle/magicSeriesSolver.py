#!/usr/bin/python
# -*- coding: utf-8 -*-
import string
def solveIt(n):
	# Modify this code to run your puzzle solving algorithm
	
	# define the sol of all the variables (0..n-1)
	sol = [0]*n
	
	sol[0] = n-4
	sol[1] = 2
	sol[2] = 1
	sol[n-4] = 1	
	print checkIt(sol)
	sol = [str(i) for i in sol]	
	# prepare the solution in the specified output format
	# if no solution is found, put 0s
	outputData = str(n) + '\n' + string.join(sol,' ') 
		
	return outputData



# checks if an assignment is feasible
def checkIt(sol):
	n = len(sol)
	count = {}
	for i in xrange(0,n):
		count[i] = 0
	for i in xrange(0,n):
		count[sol[i]] += 1
	for i in xrange(0,n):
		if sol[i] != count[i]:
			return False
	return True


import sys

if __name__ == "__main__":
	if len(sys.argv) > 1:
		try:
			n = int(sys.argv[1].strip())
		except:
			print sys.argv[1].strip(), 'is not an integer'
		print 'Solving Size:', n
		print(solveIt(n))

	else:
		print('This test requires an instance size.  Please select the size of problem to solve. (i.e. python magicSeriesSolver.py 5)')

