import numpy as np
import pandas as pd

from qbayes_tools import *

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


def get_mallard_model_states(filename='data/mallardmodeldata.csv'):
    mallarddata = pd.read_csv(filename)
    Cases = Node("Cases", np.ndarray.flatten(np.array(pd.DataFrame(data={'MarCases':mallarddata['MarCases'], 'AprCases':mallarddata['AprCases'], 'MayCases':mallarddata['MayCases'], 'JunCases':mallarddata['JunCases']}))),
                 states = {"Inc" : 0, "Min" : 1, "Mod" : 2, "Maj" : 3}, parents = ["Test", "Mask", "Work", "Rec"])
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
