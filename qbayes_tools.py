from itertools import product

def generate_cond_keys(s_0, s_i):
    ##############################################
    #THIS FUNCTION WILL GENERATE A LIST OF STRINGS TO USE AS KEYS FOR CONDITIONAL PROBABILITIES
    ### INPUT ###
    # s_0    int    number of states of the child node
    # s_i    list   number of states for each parent node, from most to least significant
    
    ### OUTPUT ###
    # list of strings to use as keys for conditional probabilities (included commas in case there is ever an >11-state node!)
    ##############################################
    
    ranges = [range(0, elem) for elem in list([s_0])+list(s_i)]
    enumed = product(*ranges)
    
    cond_keys = []
    for enum in enumed:
        enum = list(enum)
        parent_str = ",".join(str(x) for x in enum[1:])
        cond_keys.append("%s|%s"%(str(enum[0]), parent_str))
        
    return cond_keys


class Node:
    # A single variable in the Bayesian network
    def __init__(self, name, data, states=None, parents=[]):
        ### INPUTS ###
        # name:    str    name of variable
        # data:    array  state data for the node
        # states:  dict   keys are state names, values are the int each takes on in the data
        # parents: list   strings of names of parent nodes to this node
        ##############
        
        if states == None:
            states = {}
            for i in range(max(data) + 1):
                states.update({str(i) : i})
        
        self.name = name
        self.data = data
        self.states = states
        self.parents = parents