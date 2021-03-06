"""
tableTopBlocks domain definition for Pyhop 1.1.
Author:Rosario Scalise, April 30, 2016 
"""

import pyhop

"""Each Pyhop planning operator is a Python function. The 1st argument is
the current state, and the others are the planning operator's usual arguments.
This is analogous to how methods are defined for Python classes (where
the first argument is always the name of the class instance). For example,
the function pickup(state,b) implements the planning operator for the task
('pickup', b).

The blocks-world operators state variables:
- locContents[loc] = what is contained at loc given by (x,y) 
- locOccupied[loc] = Boolean describing whether there is something occupying loc (x,y)
- locRobot = loc in (x,y) at which the robot is currently located
- holding = name of the block being held, or False if the hand is empty.
"""

def pickUp(state, loc):
    # if robot at loc AND robot not holding anything AND loc has something to pickup
    if  not state.holding  and state.locOccupied[loc]:
        #state.loc[b] = 'hand'
        state.locOccupied[loc] = False 
        state.holding = state.locContents[loc] 
        # be sure to delete old contents once they are picked up!
        del state.locContents[loc]
        print(state.holding)
        return state
    else: return False

def putDown(state, loc):
    if state.holding:
        state.locContents[loc] = state.holding
        state.holding = ""
        return state
    else: return False

def moveRobot(state, locTo):
    state.locRobot = locTo
    return state


#def unstack(state,b,c):
#    if state.pos[b] == c and c != 'table' and state.clear[b] == True and state.holding == False:
#        state.pos[b] = 'hand'
#        state.clear[b] = False
#        state.holding = b
#        state.clear[c] = True
#        return state
#    else: return False
#    
#def stack(state,b,c):
#    if state.pos[b] == 'hand' and state.clear[c] == True:
#        state.pos[b] = c
#        state.clear[b] = True
#        state.holding = False
#        state.clear[c] = False
#        return state
#    else: return False
#
"""
Below, 'declare_operators(pickup, unstack, putdown, stack)' tells Pyhop
what the operators are. Note that the operator names are *not* quoted.
"""

pyhop.declare_operators(moveRobot,pickUp,putDown)
