#!/usr/bin/python
# -*- coding: utf-8 -*-

def solveIt(n):
	
	sol = [0]* n
	for i in xrange(n):
		sol[i] = [0] * n
	x,y = 0,0
	for i in xrange(1,n**2+1):
		sol[x][y] = i
		new_x,new_y = (x+1)%n,(y+1)%n
		if sol[new_x][new_y] != 0:
			x,y = x, (y-1)%n
		else:
			x,y = new_x, new_y

	# prepare the solution in the specified output format
	# if no solution is found, put 0s
	outputData = str(n) + '\n'
	for i in range(0,n):
		outputData += ' '.join(map(str, sol[i*n:(i+1)*n]))+'\n'
	
	return outputData




# checks if an assignment is feasible
# because sol is an array (not a matrix), checks are more cryptic
import math
def checkIt(sol):
	n = int(math.sqrt(len(sol)))
	m = n*(n*n+1)/2
	
	#for i in range(0,n):
	#	print sol[i*n:(i+1)*n]
	
	items = set(sol)
	if len(items) != len(sol):
		#print len(items),len(sol) 
		return False
	
	for i in range(0,n):
		#print 'row',i,sol[i*n:(i+1)*n]
		if sum(sol[i*n:(i+1)*n]) != m:
			return False
		#print 'column',i,sol[i:len(sol):n]
		if sum(sol[i:len(sol):n]) != m:
			return False
		if i < n-1:
			if sol[i*n+i] > sol[(i+1)*n+(i+1)]:
				return False 
	
	#print 'diag 1',i,[sol[i*n+i] for i in range(0,n)]
	if sum([sol[i*n+i] for i in range(0,n)]) != m:
		return False
	#print 'diag 2',i,[sol[i*n+(n-i-1)] for i in range(0,n)]
	if sum([sol[i*n+(n-i-1)] for i in range(0,n)]) != m:
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
		print('This test requires an instance size.  Please select the size of problem to solve. (i.e. python magicSquareSolver.py 3)')

