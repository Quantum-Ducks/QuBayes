from NeticaPy import Netica
import os

BASE_DIR = os.getcwd()

N = Netica()

INFINITY_ns = N.GetInfinityDbl_ns()
mesg = bytearray()
env = N.NewNeticaEnviron_ns("", None, "")
res = N.InitNetica2_bn (env, mesg)

print mesg

# initializing the network with environment
bayesian_network = N.NewNet_bn ("Alabio", env)

# create each node in the network
StateMaskOrder  = N.NewNode_bn("StateMaskOrder", 2, bayesian_network)
Testing = N.NewNode_bn("Testing", 2, bayesian_network)
TravelToWork = N.NewNode_bn("TravelToWork", 4, bayesian_network)
TravelToRec = N.NewNode_bn("TravelToRec", 4, bayesian_network)
Race = N.NewNode_bn("Race", 4, bayesian_network)
Poverty = N.NewNode_bn("Poverty", 4, bayesian_network)
Cases = N.NewNode_bn("Cases", 4, bayesian_network)
Age = N.NewNode_bn("Age", 2, bayesian_network)
Health = N.NewNode_bn("Health", 4, bayesian_network)
Deaths = N.NewNode_bn("Deaths", 2, bayesian_network)

# adding states to each node
N.SetNodeStateNames_bn(StateMaskOrder, "no, yes")
N.SetNodeStateNames_bn(Testing, "less5, great5")
N.SetNodeStateNames_bn(TravelToWork, "majorDec, modDec, minorDec, inc")
N.SetNodeStateNames_bn(TravelToRec, "majorDec, modDec, minorDec, inc")
N.SetNodeStateNames_bn(Race, "less15, 15to30, 30to45, great45")
N.SetNodeStateNames_bn(Poverty, "less11, 11to13, 13to15, great15")
N.SetNodeStateNames_bn(Cases, "dec, minorInc, modInc, majorInc")
N.SetNodeStateNames_bn(Age, "lessThanAvg, moreThanAvg")
N.SetNodeStateNames_bn(Health, "rare, somewhat, common, very")
N.SetNodeStateNames_bn(Deaths, "dec, inc")

# adding links between nodes
N.AddLink_bn(StateMaskOrder, Cases)
N.AddLink_bn(Testing, Cases)
N.AddLink_bn(TravelToWork, Cases)
N.AddLink_bn(TravelToRec, Cases)
N.AddLink_bn(Race, Cases)
N.AddLink_bn(Poverty, Cases)
N.AddLink_bn(Cases, Deaths)
N.AddLink_bn(Age, Deaths)
N.AddLink_bn(Health, Deaths)
N.AddLink_bn(Race, Deaths)
N.AddLink_bn(Poverty, Deaths)

# setting the probabilities for each top level node
# set conditional probabilities

# first layer (root nodes)
N.SetNodeProbs(StateMaskOrder, )
N.SetNodeProbs(Testing, )
N.SetNodeProbs(TravelToWork, )
N.SetNodeProbs(TravelToRec, )
N.SetNodeProbs(Race, )
N.SetNodeProbs(Poverty, )

# second layer (root)
N.SetNodeProbs(Age, )
N.SetNodeProbs(Health, )

# second layer (child)
N.SetNodeProbs(Cases, )

# third layer (child)
N.SetNodeProbs(Deaths, )

# print the error message in case of any errors within Netica
print N.ErrorMessage_ns(N.GetError_ns(N, 5, 0))

# compile the final network
N.CompileNet_bn(bayesian_network)            

# get the belief for each state for PopulationOutcome
belief = N.GetNodeBelief("Deaths", "inc", bayesian_network)
print """The probability of deaths increasing %g"""% belief

#N.EnterFinding("WarmBlooded", 'true', bayesian_network)
#belief = N.GetNodeBelief("Animal", "turtle", bayesian_network)
#print """The probability of being turtle when its WarmBlooded %g"""% belief

# delete the network and print the returned message
N.DeleteNet_bn(bayesian_network)
res = N.CloseNetica_bn(env, mesg)

print mesg

