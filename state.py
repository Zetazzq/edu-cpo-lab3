'''
State is a class that
describe the state of NFA graph
'''
from typing import Dict
from typing import Any

from CONSTANT import *
from nfa import *

class State(object):
    def __init__(self) -> None:
        self.ID = getId()
        self.IsEnd = False
        self.edgeMap = {} #type: Dict[str, Any]


    def addPath(self,edge:str,nfaState) -> None:
        if self.edgeMap.__contains__(edge):
            self.edgeMap[edge].append(nfaState)
        else:
            self.edgeMap[edge] = []
            self.edgeMap[edge].append(nfaState)

