import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from qubayes_tools import *
from network_setup import *


def get_probabilities(node):
    ############################################
    # USE THIS FUNCTION TO FIND THE PROBABILITIES FOR AN INDIVIDUAL NODE IN THE NETWORK
    
    ### INPUT ###
    # node:     Node     Node object in network

    ### OUTPUT ###
    # probs:    dict     probabilities
    ############################################

    data= node.data
    states = node.states
    name = node.name
    num_total = len(data)  #total number of data points with which to calculate probabilities

    probs = {}
    prob_sum = 0
    for state in states.keys(): #loop through different state strings
        prob = np.shape(np.where(data == states[state]))[1]/num_total
        prob_sum += prob
        probs.update({name + "_" + state : prob})
    assert round(prob_sum, 3) == 1. 
    
    return probs


def get_conditional_probability(child, *ps):
    ############################################
    ### THIS FUNCTION CALCULATES CONDITIONAL PROBABILITIES FOR CHILD NODE
    ### THAT HAS s_m STATES AND m PARENT NODES EACH WITH s_i STATES WHERE i = 0, ..., m-1
    
    ### INPUTS ###
    # child    Node
    # *ps      Node(s) or a single list of Nodes
    
    ### OUTPUT ###
    # a dictionary of conditional probabilities
    ############################################

    #we might want to add some assert statements checking that all inputs have the same shape
    #also use assert to check that for all p in ps, ps.name is in child.parents, and vice versa

    if type(ps[0]) == list:
        ps = ps[0]
    if type(ps[0]) != Node:
        print("ERROR: This input is not right!")
    
    keys = generate_cond_keys(child, ps)

    cond_probs = {key: 0 for key in keys} #initialize a dictionary for conditional probabilities
    for key in keys:
        numer, tot = 0, 0
        n = len(child.data)
        for i in range(n):
            all_ps = True
            for j in range(len(ps)):
                p = ps[j]
                if p.data[i] != int(p.states[key.split("|")[1].split(",")[j].split("_")[1]]):
                    all_ps = False
                    break
  
            if all_ps:
                tot += 1
                if child.data[i] == int(child.states[key.split("|")[0].split("_")[1]]):
                    numer += 1
                cond_probs.update({key : numer/tot})
  
    return cond_probs

# example: results from running simple model on simulator: 
# {'000': 2783, '001': 1240, '100': 603, '111': 815, '110': 294, '010': 1712, '101': 485, '011': 260}

def get_marginal_0probabilities(state_counts):
    #state_counts: dict, counts for each state from network result (should have 2^n entries)
    #marg_probs: array of length n, marginal probabilities that each qubit is 0,
        #from most significant to least significant qubit
    
    n = len(list(state_counts.keys())[0]) #number of qubits
    prob = np.zeros(n)
    total = sum(state_counts.values())

    for i in range(n):
        for key in state_counts:
            if int(key[i]) == 0:
                prob[i] += state_counts[key]
        prob[i] = prob[i]/total
    
    return prob



def func(**counts):
    return counts["c001"]