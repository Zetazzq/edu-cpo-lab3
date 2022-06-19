'''
we design some basic MatchStrategy
to deal with ordinary situations
'''
from typing import Optional, Dict

from CONSTANT import *


class MatchStrategy(object):
    def isMatch(self,c:str, edge:str) -> bool:
        return False

# match simple character
class CharMatchStrategy(MatchStrategy):
    def isMatch(self,c:str, edge:str) -> bool:
        return c.__eq__(edge)

# match dot
class DotMatchStrategy(MatchStrategy):
    def isMatch(self,c:str, edge:str) -> bool:
        return (not c.__eq__('\n')) and (not c.__eq__('\r'))

# match digital
class DigitalMatchStrategy(MatchStrategy):
    def isMatch(self,c:str, edge:str) -> bool:
        return str.isdigit(c)

# match \\w
class WMatchStrategy(MatchStrategy):
    def isMatch(self,c:str, edge:str) -> bool:
        return str.isalpha(c) or str.isalnum(c) or c.__eq__('_')

# match space
class SpaceMatchStrategy(MatchStrategy):
    def isMatch(self,c:str, edge:str) -> bool:
        return (c == '\f' or c == '\n' or c == '\r' or c == '\t' or c == ' ')

# match hat ^
class HatMatchStrategy(MatchStrategy):
    def isMatch(self,c:str, edge:str) -> bool:
        return c == edge[1]

class MatchStrategyManager(object):
    def __init__(self) -> None:
        self.matchStrategyMap = {} # type: Dict[str, MatchStrategy]
        # Put it in the strategy table
        self.matchStrategyMap[CHAR] = CharMatchStrategy()
        self.matchStrategyMap['.'] = DotMatchStrategy()
        self.matchStrategyMap['\\d'] = DigitalMatchStrategy()
        self.matchStrategyMap['\\s'] = SpaceMatchStrategy()
        self.matchStrategyMap['\\w'] = WMatchStrategy()
        self.matchStrategyMap['^'] = HatMatchStrategy()

    def getStrategy(self,edge:str):
        if self.matchStrategyMap.__contains__(edge):
            return self.matchStrategyMap.get(edge)
        if len(edge) == 1:
            return self.matchStrategyMap.get(CHAR)
