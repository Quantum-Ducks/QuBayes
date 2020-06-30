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