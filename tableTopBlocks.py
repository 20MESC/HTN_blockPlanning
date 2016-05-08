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
"""

print("- Define state1:")
# Create Initial blocks state
s1 = State('state1')
# Locations will be in standard graph axes and ordered pairs (x,y)
s1.locContents = bidict({(1,1):'b1',(2,1):'b2'}) # (1,1) holds b1, (1,2) holds b2
# Could maybe at some point replace this by just checking if the key exists in loc?
s1.locOccupied = {(x,y):False for x in range(1,4) for y in range(1,4)}
s1.locOccupied.update({(1,1):True, (2,1):True}) # make sure these reflect the occupied locs
s1.locRobot = (2,2)
s1.holding = False 

print_state(s1)
print('')

print("- Define goal1:")

g1 = Goal('goal1')
g1.locContents = bidict({(1,3):'b1',(2,3):'b2'})
g1.locOccupied = {(x,y):False for x in range(1,4) for y in range(1,4)}
g1.locOccupied.update({(1,3):True, (2,3):True}) # make sure these reflect the occupied locs

print_goal(g1)
print('')


pyhop(s1,[('moveBlocks',g1)], verbose=1)

import ipdb
ipdb.set_trace()
