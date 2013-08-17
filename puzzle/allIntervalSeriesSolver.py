#!/usr/bin/python
# -*- coding: utf-8 -*-

def solveIt(n):
	# Modify this code to run your puzzle solving algorithm
	
	
	sol = [0] * n
	for i in xrange(1,n,2):
		sol[i] = n - ((i-1)/2) -1
	for i in xrange(0,n,2):
		sol[i] = i/2

	# prepare the solution in the specified output format
	# if no solution is found, put 0s
	outputData = str(n) + '\n'
	outputData += ' '.join(map(str, sol))+'\n'
	
	return outputData



# checks if an assignment is feasible
def checkIt(sol):
	n = len(sol)
	
	items = set(sol)
	if len(items) != n:
		return False
	
	deltas = set([abs(sol[i]-sol[i+1]) for i in range(0,n-1)])
	if len(deltas) != n-1:
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
		print('This test requires an instance size.  Please select the size of problem to solve. (i.e. python allIntervalSeriesSolver.py 5)')

