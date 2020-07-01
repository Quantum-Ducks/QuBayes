from itertools import product
import numpy as np
from network_setup import *

def generate_cond_keys(child, ps):
    ##############################################
    #THIS FUNCTION WILL GENERATE A LIST OF STRINGS TO USE AS KEYS FOR CONDITIONAL PROBABILITIES
    ### INPUT ###
    # s_0    int    number of states of the child node
    # s_i    list   number of states for each parent node, from most to least significant
    
    ### OUTPUT ###
    # list of strings to use as keys for conditional probabilities (included commas in case there is ever an >11-state node!)
    ##############################################
    
    cname = child.name
    cstates = child.states
    
    ranges = [[child.name], child.states.keys()]
    for p in ps:
        ranges.append([str(p.name)])
        ranges.append(p.states.keys())
    enumed = product(*ranges)

    add = [",","_"]
    cond_keys = []
    for enum in enumed:
        suff = 0
        enum = list(enum)
        parent_str = ''
        for i in range(2,len(enum)-1):
            suff = (suff + 1)%2
            parent_str += str(enum[i]) + add[suff]
        parent_str += str(enum[len(enum)-1])
        cond_keys.append("%s_%s|%s"%(str(enum[0]), str(enum[1]), parent_str))
        
    return cond_keys
    
def generate_parent_str(ps):
    ##############################################
    #THIS FUNCTION WILL GENERATE A LIST OF STRINGS TO USE AS KEYS FOR CONDITIONAL PROBABILITIES
    ### INPUT ###
    # s_0    int    number of states of the child node
    # s_i    list   number of states for each parent node, from most to least significant
    
    ### OUTPUT ###
    # list of strings to use as keys for conditional probabilities (included commas in case there is ever an >11-state node!)
    ##############################################

    ranges = []
    for p in ps:
        ranges.append([str(p.name)])
        ranges.append(p.states.keys())
    enumed = product(*ranges)

    add = [",","_"]
    cond_keys = []
    for enum in enumed:
        suff = 0
        enum = list(enum)
        parent_str = ''
        for i in range(len(enum)-1):
            suff = (suff + 1)%2
            parent_str += str(enum[i]) + add[suff]
        parent_str += str(enum[len(enum)-1])
        cond_keys.append("%s"%(parent_str))
        
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
        
