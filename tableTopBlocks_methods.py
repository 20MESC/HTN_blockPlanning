"""
tableTopBlocks methods for Pyhop 1.1.
Author: Rosario Scalise, April 30, 2016
"""

import pyhop
from pyhop import Goal
from bidict import bidict
from tableTopBlocks_utils import get_line
import math

"""
Here are some helper functions that are used in the methods' preconditions.
"""
# CHECKS TO SEE IF BLOCK IS WHERE IT IS SUPPOSED TO BE
def is_done(b1,state,goal):
    if b1 in goal.locContents.values() and goal.locContents.inv[b1] != state.locContents.inv[b1]:
        return False
    else:
        return True

# GIVES BLOCKS STATUSES
def status(b1,state,goal):
    if is_done(b1,state,goal):
        return 'done'
    elif not state.locOccupied[goal.locContents.inv[b1]]:
        return 'move-to-table'
    else:
        return 'waiting'

# OLD STATUS WHICH ALLOWS FOR BLOCK STACKING LOGIC
#def status(b1,state,goal):
#    if is_done(b1,state,goal):
#        return 'done'
#    elif not state.clear[b1]:
#        return 'inaccessible'
#    elif not (b1 in goal.pos) or goal.pos[b1] == 'table':
#        return 'move-to-table'
#    elif is_done(goal.pos[b1],state,goal) and state.clear[goal.pos[b1]]:
#        return 'move-to-block'
#    else:
#        return 'waiting'

def all_blocks(state):
    return state.locContents.values()


"""
In each Pyhop planning method, the first argument is the current state (this is analogous to Python methods, in which the first argument is the class instance). The rest of the arguments must match the arguments of the task that the method is for. For example, ('pickup', b1) has a method get_m(state,b1), as shown below.
"""

### methods for "move_blocks"

# Currently being handled by checking occupied space -> Finding the blocks in each occupied space -> Checking status of block -> Check if its part of goal -> If it needs to be moved, move it
# TODO: There might be a more concise way to address this.
def moveBlocks_m(state,goal):
    """
    This method implements the following block-stacking algorithm:
    If there's a block that can be moved to its final position, then
    do so and call move_blocks recursively. Otherwise, if there's a
    block that needs to be moved and can be moved to the table, then 
    do so and call move_blocks recursively. Otherwise, no blocks need
    to be moved.
    """
    # for each currently occupied location (keys will only list these since we delete and add keys so that only currently occupied locations are a valid key)
    for loc in state.locContents.keys():
        b1 = state.locContents[loc]
        s = status(b1,state,goal)
        if s == 'move-to-table':
            return [('moveOne',loc,goal.locContents.inv[b1]),('moveBlocks',goal)]
        else:
            continue
    
    ## here is where calls to address blocks would go

    ## no more blocks need moving
    return []




    # OLD METHODS WHICH ALLOWS FOR BLOCK STACKING
    #for loc in all_blocks(state):
    #    s = status(b1,state,goal)
    #    if s == 'move-to-table':
    #        return [('moveOne',b1,'table'),('moveBlocks',goal)]
    #    elif s == 'move-to-block':
    #        return [('moveOne',b1,goal.pos[b1]), ('moveBlocks',goal)]
    #    else:
    #        continue
    ##
    ## if we get here, no blocks can be moved to their final locations
    #b1 = pyhop.find_if(lambda x: status(x,state,goal) == 'waiting', all_blocks(state))
    #if b1 != None:
    #    return [('moveOne',b1,'table'), ('moveBlocks',goal)]
    ##
    ## if we get here, there are no blocks that need moving
    #return []

"""
declare_methods must be called once for each taskname. Below, 'declare_methods('get',get_m)' tells Pyhop that 'get' has one method, get_m. Notice that 'get' is a quoted string, and get_m is the actual function.
"""
pyhop.declare_methods('moveBlocks',moveBlocks_m)


### methods for "move_one"

def moveOne_m(state,locI,locF):
    """
    Generate subtasks to get b1 and put it at dest.
    """
    #TODO: POTENTIALLY CHANGE WHERE THIS EFFECT HAPPENS
    # when a block is moved to its final resting place, it should be removed from blocksAvail list
    state.blocksAvail.remove(state.locContents[locI])
    return [('moveRobot', locI),('pickUp', locI), ('moveRobot', locF), ('putDown', locF)]

pyhop.declare_methods('moveOne',moveOne_m)


##### BELOW ARE METHODS FOR FORMING SHAPE COMPONENTS AND SHAPES

def createLine_m(state,pI,pF):
    """
    Generate subtasks to create a line starting at loc given by pI and ending at loc given by pF.
    """ 
    #TODO: CHECK BOUNDS

    # uses Bresenham's Line Algorithm to compute discrete points for line
    linePointsList = get_line(pI,pF)
    #TODO: Alternate Method
    # Currently filters available blocks by first n (n is number of points on linePointsList) 
    blocksList = state.blocksAvail[0:len(linePointsList)] 

    gL = Goal('goalLine')
    gL.locContents = bidict(zip(linePointsList,blocksList))
    gL.locOccupied = {loc:False for loc in state.locContents.keys()} # locContents.keys() gives all locs 
    gL.locOccupied.update({loc:True for loc in gL.locContents.keys()}) 
    return [('moveBlocks',gL)]


pyhop.declare_methods('createLine',createLine_m)


def createRect_m(state,center,sideLen1,sideLen2):
    """
    Generate subtasks to create a rectangle centered around 'center' with side lengths 'sideLen' .
    """ 
    # Compute Vertices
    cx = center[0]
    cy = center[1]
    v1 = (int(cx-math.floor(sideLen1/2.0)),int(cy-math.floor(sideLen2/2.0))) 
    v2 = (int(cx-math.floor(sideLen1/2.0)),int(cy+math.ceil(sideLen2/2.0))) 
    v3 = (int(cx+math.ceil(sideLen1/2.0)),int(cy+math.ceil(sideLen2/2.0))) 
    v4 = (int(cx+math.ceil(sideLen1/2.0)),int(cy-math.floor(sideLen2/2.0))) 

    
    # TODO: CHECK BOUNDS
    
    return [('createLine',v1,v2),('createLine',v2,v3),('createLine',v3,v4),('createLine',v4,v1)]
     
    


pyhop.declare_methods('createRect',createRect_m)







### methods for "get"

def get_m(state,b1):
    """
    Generate either a pickup or an unstack subtask for b1.
    """
    if state.clear[b1]:
        if state.pos[b1] == 'table':
                return [('pickup',b1)]
        else:
                return [('unstack',b1,state.pos[b1])]
    else:
        return False

pyhop.declare_methods('get',get_m)


### methods for "put"

def put_m(state,b1,b2):
    """
    Generate either a putdown or a stack subtask for b1.
    b2 is b1's destination: either the table or another block.
    """
    if state.holding == b1:
        if b2 == 'table':
                return [('putdown',b1)]
        else:
                return [('stack',b1,b2)]
    else:
        return False

pyhop.declare_methods('put',put_m)


