"""
Table Top Blocks-world .
Author: Rosario Scalise, April 30, 2016
"""

from __future__ import print_function
from pyhop import *
from bidict import bidict

"""
List all operators and methods
Check here to see that everything is loaded correctly
"""

import tableTopBlocks_operators
print('')
print_operators()

import tableTopBlocks_methods
print('')
print_methods()



"""
Define Init State, Goal State, and run planner

Init:
(1,3) : b1
(2,3) : b2
(3,3) : b3
(4,3) : b4
(5,3) : b5
(1,5) : b6
(2,5) : b7
(3,5) : b8
(4,5) : b9
(5,5) : b10
(2,2) : robot

Goal:
createRect((3,3),3,4)
consists of:
(2,2) : b
(2,3) : b
(2,4) : b
(2,5) : b
(3,5) : b
(4,2) : b
(4,3) : b
(4,4) : b
(4,5) : b
(3,2) : b
"""


print("- Define state1:")
# Create Initial blocks state
s1 = State('state1')
# Locations will be in standard graph axes and ordered pairs (x,y)
s1.locContents = bidict({(1,3):'b1',(2,3):'b2',(3,3):'b3',(4,3):'b4',(5,3):'b5',(1,5):'b6',(2,5):'b7',(3,5):'b8',(4,5):'b9',(5,5):'b10'},) # (1,1) holds b1, (1,2) holds b2
# TODO: Definitely come up with alternate solution to available blocks list - probably block status
s1.blocksAvail = s1.locContents.values()
# Could maybe at some point replace this by just checking if the key exists in loc?
s1.locOccupied = {(x,y):False for x in range(1,6) for y in range(1,6)}
s1.locOccupied.update({loc:True for loc in s1.locContents.keys()}) # make sure these reflect the occupied locs
s1.locRobot = (2,2)
s1.holding = False 

print_state(s1)
print('')

print("- Define goal1:")

#g1 = Goal('goal1')
#g1.locContents = bidict({(1,1):'b1',(1,2):'b2',(1,3):'b3'})
#g1.locOccupied = {loc:False for loc in s1.locContents.keys()} #locContents.keys() gives all locs
#g1.locOccupied.update({loc:True for loc in g1.locContents.keys()}) 
#g1.locRobot = (2,2)

#print_goal(g1)
#print('')


result = pyhop(s1,[('createRect',(3,3),3,4)], verbose=1)

import ipdb
ipdb.set_trace()
