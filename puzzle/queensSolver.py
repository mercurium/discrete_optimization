#!/usr/bin/python
# -*- coding: utf-8 -*-

def solveIt(n):
	sol = [0]*n
	for i in xrange(n//2):
		sol[i] = 1+2*i
	for i in xrange(n//2,n):
		sol[i] = (i-n//2) * 2
	print checkIt(sol)
	outputData = str(n) + '\n'
	outputData += ' '.join(map(str, sol))+'\n'
		
	return outputData



# checks if an assignment is feasible
def checkIt(sol):
	n = len(sol)
	for i in xrange(0,n):
		for j in xrange(i+1,n):
			if sol[i] == sol[j] or \
			   sol[i] == sol[j] + (j-i) or \
			   sol[i] == sol[j] - (j-i):
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
		print('This test requires an instance size.  Please select the size of problem to solve. (i.e. python queensSolver.py 8)')

