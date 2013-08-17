#!/usr/bin/python
# -*- coding: utf-8 -*-

import string
approx = False

def solveIt(inputData):
  # Modify this code to run your optimization algorithm

  # parse the input
  lines = inputData.split('\n')

  firstLine = lines[0].split()
  items = int(firstLine[0])
  capacity = int(firstLine[1])

  values = []
  weights = []

  for i in range(1, items+1):
    line = lines[i]
    parts = line.split()

    values.append(int(parts[0]))
    weights.append(int(parts[1]))

  if approx:
    items /= 100
    weights = [w/100+1 for w in weights]

  # a trivial greedy algorithm for filling the knapsack
  # it takes items in-order until the knapsack is full


  if False: #items >= 300:
    w_v = [0]* len(values) #weight_value pairs
    for i in xrange(len(values)):
      w_v[i] = (values[i]*1.0/weights[i],weights[i],values[i],i)
    
    w_v.sort()
    w_v = w_v[::-1]
    items = len(values)


    value = 0
    weight = 0
    taken = [0] * len(values)

    for i in xrange(0,len(w_v)):
      if weight + w_v[i][1] <= capacity:
        taken[w_v[i][3]] = 1
        value += w_v[i][2]
        weight += w_v[i][1]
    outputData = str(value) + ' ' + str(0) + '\n'

  else:
    taken = [0] * (items)
    k = dict()
    
    for j in xrange(2): #base cases of 0 items left/weight left
      k[(0, j)] = (0,taken)
    for w in xrange(capacity + 1):
      k[(w, 0)] = (0,taken)



    for j in xrange(1, items):
      for w in xrange(1, capacity + 1):
        if weights[j] > w: 
          k[(w, j%2)] = k[(w, (j-1)%2)] #since we're not adding the item, no change
        else:
          if k[(w,(j-1)%2)][0] >=k[(w-weights[j], (j-1)%2)][0] + values[j]:
            k[(w,j%2)] = k[w, (j-1)%2]
          else:
            k[(w,j%2)] = (k[(w-weights[j], (j-1)%2)][0] + values[j], \
              k[(w-weights[j], (j-1)%2)][1][:] )
            k[(w,j%2)][1][j] = 1

 
    
    value = k[(capacity, (items - 1)%2)][0]
    taken = k[(capacity, (items - 1)%2)][1]
    outputData = str(value) + ' ' + str(1) + '\n'
    print sum(taken)
  # prepare the solution in the specified output format
  outputData += ' '.join(map(str, taken))
  return outputData


import sys

if __name__ == '__main__':
  if len(sys.argv) > 1:
    fileLocation = sys.argv[1].strip()
    inputDataFile = open(fileLocation, 'r')
    inputData = ''.join(inputDataFile.readlines())
    inputDataFile.close()
    print solveIt(inputData)
  else:
    print 'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)'

