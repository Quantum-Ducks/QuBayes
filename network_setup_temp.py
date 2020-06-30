import numpy as np
import pandas as pd

from qbayes_tools import *
from probabilities import *



def build_graph(ntwk_func, filename = None, **kwargs):
    if filename == None:
        nodes = ntwk_func(**kwargs)
    else:
        nodes = ntwk_func(filename = filename, **kwargs)
    
    graph = {}
    for node in nodes:
        if node.parents == []:
            #this is a root node, we just need to calculate probabilities
            ct = 0
            probs = []
            got_probs = get_probabilities(node)
            newkey = ""
            for state_i in node.states.keys():
                if ct == 0:
                    newkey += node.name + "_" + state_i
                else:
                    newkey += "," + node.name + "_" + state_i
                probs.append(got_probs["state_key"])
                ct += 1
            graph.update({newkey : ([], probs)})
        else:
            #this is a child node, we need conditional probabilities!
            cond_probs = []
            
            p_nodes = []   #initialize a list in which to place parent nodes
            for anode in nodes: #loop thru all nodes in network
                if anode.name in node.parents:
                    p_nodes.append(anode)
            
            cond_prob_dict = get_conditional_probability(node, p_nodes[:])
            p_ct = 0
            for p_str in generate_parent_str(node.parents):
                s_ct = 0
                for state_i in node.states.keys():
                    s_ct += 1
                    cond_str = node.name + "_" + state_i + "|" + p_str
                    cond_probs.append(cond_prob_dict[cond_str])
                    
                    if p_ct == 0:
                        if s_ct == 0:
                            newkey += node.name + "_" + state_i
                        else:
                            nekwy += "," + node.name + "_" + state_i
                p_ct += 1
                
            graph.update({newkey : (node.parents, cond_probs)})




#################################################
# COVID-19 EXAMPLES:


def get_lesser_model_nodes(filename='data/lesser_model_data.csv'):
    lesserdata = pd.read_csv(filename)
    
    statedataStayHome = {'MarHome' : lesserdata['MarHome'], 'AprHome' : lesserdata['AprHome'], 'MayHome' : lesserdata['MayHome'], 'JunHome' : lesserdata['JunHome']}
    StayHome = Node("StayHome", np.ndarray.flatten(np.array(pd.DataFrame(data=statedataStayHome))), states = {"No" : 0, "Yes" : 1})

    statedataTests = {'MarTest' : lesserdata['MarTest'], 'AprTest' : lesserdata['AprTest'], 'MayTest' : lesserdata['MayTest'], 'JunTest' : lesserdata['JunTest']}
    Tests = Node("Tests", np.ndarray.flatten(np.array(pd.DataFrame(data=statedataTests))), states = {"GT5" : 0, "LE5" : 1})

    statedataCases = {'MarCases' : lesserdata['MarCases'], 'AprCases' : lesserdata['AprCases'], 'MayCases' : lesserdata['MayCases'], 'JunCases' : lesserdata['JunCases']}
    Cases = Node("Cases", np.ndarray.flatten(np.array(pd.DataFrame(data=statedataCases))), states = {"Inc" : 0, "noInc" : 1}, parents = ["Tests", "StayHome"])
                 
    return Cases, Tests, StayHome


def get_mallard_model_nodes(filename='data/mallardmodeldata.csv'):
    mallarddata = pd.read_csv(filename)
    Cases = Node("Cases", np.ndarray.flatten(np.array(pd.DataFrame(data={'MarCases':mallarddata['MarCases'], 'AprCases':mallarddata['AprCases'], 'MayCases':mallarddata['MayCases'], 'JunCases':mallarddata['JunCases']}))),
                 states = {"Inc" : 0, "Min" : 1, "Mod" : 2, "Maj" : 3}, parents = ["Test", "Mask", "Work", "Rec","Race","Poverty"])
    Test = Node("Test", np.ndarray.flatten(np.array(pd.DataFrame(data={'MarTest':mallarddata['MarTest'],'AprTest':mallarddata['AprTest'],'MayTest':mallarddata['MayTest'], 'JuneTest':mallarddata['JunTest']}))),
                states = {"GT5" : 0, "LE5" : 1})
    Mask = Node("Mask", np.ndarray.flatten(np.array(pd.DataFrame(data={'MarMask':mallarddata['MarMask'],'AprMask':mallarddata['AprMask'],'MayMask':mallarddata['MayMask'],'JunMask':mallarddata['JunMask']}))),
                states = {"No" : 0, "Yes" : 1})
    Work = Node("Work", np.ndarray.flatten(np.array(pd.DataFrame(data={'MarWork':mallarddata['MarWork'],'AprWork':mallarddata['AprWork'],'MayWork':mallarddata['MayWork'],'JunWork':mallarddata['JunWork']}))),
                states = {"Inc" : 0, "Min" : 1, "Mod" : 2, "Maj" : 3})
    Rec = Node("Rec", np.ndarray.flatten(np.array(pd.DataFrame(data={'MarRec':mallarddata['MarRec'],'AprRec':mallarddata['AprRec'],'MayRec':mallarddata['MayRec'],'JunRec':mallarddata['JunRec']}))),
               states = {"Inc" : 0, "Min" : 1, "Mod" : 2, "Maj" : 3})
    Death = Node("Death", np.ndarray.flatten(np.array(pd.DataFrame(data={'MarDeath':mallarddata['MarDeath'],'AprDeath':mallarddata['AprDeath'],'MayDeath':mallarddata['MayDeath'],'JunDeath':mallarddata['JunDeath']}))),
                 states = {"Inc" : 0, "notInc" : 1}, parents = ["Cases", "Age"])
    Age = Node("Age", np.ndarray.flatten(np.array(pd.DataFrame(data={'MarAge':mallarddata['MarAge'],'AprAge':mallarddata['AprAge'],'MayAge':mallarddata['MayAge'],'JunAge':mallarddata['JunAge']}))),
               states = {"Old" : 0, "Young" : 1})
    return Cases, Test, Mask, Work, Rec, Death, Age


def get_alabio_model_nodes(filename='data/alabiomodeldata.csv'):
    alabiodata = pd.read_csv(filename)
    Cases = Node("Cases", np.ndarray.flatten(np.array(pd.DataFrame(data={'MarCases':alabiodata['MarCases'], 'AprCases':alabiodata['AprCases'], 'MayCases':alabiodata['MayCases'], 'JunCases':alabiodata['JunCases']}))),
                states={"Inc":0,"Min":1,"Mod":2,"Maj":3}, parents=["Test", "Mask", "Work", "Rec", "Race", "Poverty"])
    Test = Node("Test", np.ndarray.flatten(np.array(pd.DataFrame(data={'MarTest':alabiodata['MarTest'],'AprTest':alabiodata['AprTest'],'MayTest':alabiodata['MayTest'], 'JuneTest':alabiodata['JunTest']}))),
                states={"GT5" : 0, "LE5" : 1})
    Mask = Node("Mask", np.ndarray.flatten(np.array(pd.DataFrame(data={'MarMask':alabiodata['MarMask'],'AprMask':alabiodata['AprMask'],'MayMask':alabiodata['MayMask'],'JunMask':alabiodata['JunMask']}))),
                states = {"No" : 0, "Yes" : 1})
    Work = Node("Work", np.ndarray.flatten(np.array(pd.DataFrame(data={'MarWork':alabiodata['MarWork'],'AprWork':alabiodata['AprWork'],'MayWork':alabiodata['MayWork'],'JunWork':alabiodata['JunWork']}))),
                states = {"Inc" : 0, "Min" : 1, "Mod" : 2, "Maj" : 3})
    Rec = Node("Rec", np.ndarray.flatten(np.array(pd.DataFrame(data={'MarRec':alabiodata['MarRec'],'AprRec':alabiodata['AprRec'],'MayRec':alabiodata['MayRec'],'JunRec':alabiodata['JunRec']}))),
               states = {"Inc" : 0, "Min" : 1, "Mod" : 2, "Maj" : 3})
    Death = Node("Death", np.ndarray.flatten(np.array(pd.DataFrame(data={'MarDeath':alabiodata['MarDeath'],'AprDeath':alabiodata['AprDeath'],'MayDeath':alabiodata['MayDeath'],'JunDeath':alabiodata['JunDeath']}))),
                 states = {"Inc" : 0, "notInc" : 1}, parents = ["Cases", "Age", "Race", "Poverty", "Health"])
    Age = Node("Age", np.ndarray.flatten(np.array(pd.DataFrame(data={'MarAge':alabiodata['MarAge'],'AprAge':alabiodata['AprAge'],'MayAge':alabiodata['MayAge'],'JunAge':alabiodata['JunAge']}))),
               states = {"Old" : 0, "Young" : 1})
    Race = Node("Race", np.ndarray.flatten(np.array(pd.DataFrame(data={'MarRace':alabiodata['MarRace'],'AprRace':alabiodata['AprRace'],'MayRace':alabiodata['MayRace'],'JunRace':alabiodata['JunRace']}))),
                states = {"LE15":0, "15to30":1, "30to45":2, "GT45":3})
    Poverty = Node("Poverty", np.ndarray.flatten(np.array(pd.DataFrame(data={'MarPoverty':alabiodata['MarPoverty'],'AprPoverty':alabiodata['AprPoverty'],'MayPoverty':alabiodata['MayPoverty'],'JunPoverty':alabiodata['JunPoverty']}))),
                   states={"LE11":0, "11to13":1, "13to15":2, "GT15":3})
    Health = Node("Health", np.ndarray.flatten(np.array(pd.DataFrame(data={'MarHealth':alabiodata['MarHealth'],'AprHealth':alabiodata['AprHealth'],'MayHealth':alabiodata['MayHealth'],'JunHealth':alabiodata['JunHealth']}))),
                  states={"Rare":0, "SomewhatCom":1, "Common":2, "VeryCom":3})
    return Cases, Test, Mask, Work, Rec, Death, Age, Race, Poverty, Health
