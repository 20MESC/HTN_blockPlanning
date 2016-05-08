"""
tableTopBlocks methods for Pyhop 1.1.
Author: Rosario Scalise, April 30, 2016
"""

import pyhop


"""
Here are some helper functions that are used in the methods' preconditions.
"""
# CHECKS TO SEE IF BLOCK IS WHERE IT IS SUPPOSED TO BE
#def is_done(b1, state, goal):
#    if b1 in goal.locContents.values() and locContents


#def is_done(b1,state,goal):
#    if b1 == 'table': return True
#    if b1 in goal.pos and goal.pos[b1] != state.pos[b1]:
#        return False
#    if state.pos[b1] == 'table': return True
#    return is_done(state.pos[b1],state,goal)

# GIVES BLOCKS STATUSES
def status(b1,state,goal):
    if is_done(b1,state,goal):
        return 'done'
    elif not state.clear[b1]:
        return 'inaccessible'
    elif not (b1 in goal.pos) or goal.pos[b1] == 'table':
        return 'move-to-table'
    elif is_done(goal.pos[b1],state,goal) and state.clear[goal.pos[b1]]:
        return 'move-to-block'
    else:
        return 'waiting'

def all_blocks(state):
    return state.locContents.values()


"""
In each Pyhop planning method, the first argument is the current state (this is analogous to Python methods, in which the first argument is the class instance). The rest of the arguments must match the arguments of the task that the method is for. For example, ('pickup', b1) has a method get_m(state,b1), as shown below.
"""

### methods for "move_blocks"

def moveBlocks_m(state,goal):
    """
    This method implements the following block-stacking algorithm:
    If there's a block that can be moved to its final position, then
    do so and call move_blocks recursively. Otherwise, if there's a
    block that needs to be moved and can be moved to the table, then 
    do so and call move_blocks recursively. Otherwise, no blocks need
    to be moved.
    """






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
    return [('moveRobot', locI),('pickUp', locI), ('moveRobot', locF), ('putDown', locF)]

pyhop.declare_methods('moveOne',moveOne_m)


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


