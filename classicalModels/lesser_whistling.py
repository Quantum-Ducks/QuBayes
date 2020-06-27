from NeticaPy import Netica
N = Netica()
mesg = bytearray()
env = N.NewNeticaEnviron_ns("",None,"")
#env = N.NewNeticaEnviron_ns("",None,"");
res = N.InitNetica2_bn(env, mesg)

print mesg
	
net = N.NewNet_bn("Classical_LesserWhistlingDuck", env)

# define the nodes of the system
StayHome = N.NewNode_bn("StayHome", 2, net);
Testing = N.NewNode_bn("Testing", 2, net);
Cases = N.NewNode_bn("Cases", 2, net);

# define the states (here, only 2 states used)
N.SetNodeStateNames_bn(StayHome,"not_in_place, in_place");
N.SetNodeStateNames_bn(Testing, "bad, good");
N.SetNodeStateNames_bn(Cases, "increasing, decreasing");

# add links between nodes (from, to)
N.AddLink_bn(StayHome, Cases);
N.AddLink_bn(Testing, Cases);

# type in conditional probabilities
# parent nodes:	
N.SetNodeProbs(StayHome, 0.645, 0.355);
N.SetNodeProbs(Testing, 0.62, 0.38);

# child nodes (layer 1):
N.SetNodeProbs(Cases, "not_in_place", "bad", 0.8181818181818182, 0.18181818181818182);
N.SetNodeProbs(Cases, "not_in_place", "good", 0.8412698412698413, 0.15873015873015872);
N.SetNodeProbs(Cases, "in_place", "bad", 0.7068965517241379, 0.29310344827586204);
N.SetNodeProbs(Cases, "in_place", "good", 0.23076923076923078, 0.7692307692307693);

# now run this shiz
N.CompileNet_bn(net)

N.EnterFinding("StayHome", "not_in_place", net);
N.EnterFinding("Testing", "bad", net);
belief = N.GetNodeBelief("Cases", "increasing", net)
print """The probability of cases increasing with no stay at home and bad testing is %g"""% belief

# Remove all findings
N.RetractNetFindings_bn(net)

N.EnterFinding("StayHome", "in_place", net);
N.EnterFinding("Testing", "bad", net);
belief = N.GetNodeBelief("Cases", "decreasing", net)
print """The probability of cases decreasing with a stay at home order and bad testing is %g"""% belief

N.DeleteNet_bn(net)
res = N.CloseNetica_bn(env, mesg)

print mesg
