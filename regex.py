'''
Regex has match search sub split basic methods
user use regex can do certain things with strings
'''

from nfa import *
from reader import *
from strategy import *
from graphviz import Digraph # type: ignore
import logging

from typing import List

logging.basicConfig(level=logging.INFO)

class Regex(object):
    def __init__(self) -> None:
        self.reader = None
        self.nfa = None
        self.matchStrategyManager = MatchStrategyManager()
        # use for ^
        self.isHat = False
        # use for $
        self.isDoller = False
        # use for []
        self.isRact = False
        # use for {,m}
        self.isMaxMatch = False
        # record pre state node
        self.preNode = None
        # use for visualize
        self.nodesLst = [State]

    def compile(self,partten:str) -> None:
        self.reader = Reader(partten) # type: ignore
        assert isinstance(self.reader,Reader)
        self.nfa = None
        self.isRact = False
        self.isHat = False
        self.isDoller = False
        self.isMaxMatch = False
        assert isinstance(self.reader,Reader)
        self.reader.cur = 0
        self.nodesLst = []
        resetID()
        nfaGraph = self.regex2nfa()
        if not nfaGraph:
            logging.info('pattern: ' + partten + ' ' + 'nfaGraph build error')
        # The end node marked NFA is the end node
        nfaGraph.end.IsEnd = True
        self.nfa = nfaGraph
        logging.info('pattern: ' + partten + ' ' + 'nfaGraph build success')

    def parseRepeat_n_m(self,edge:str,nfaGraph:NFA) -> None:
        s = ''
        assert isinstance(self.reader ,Reader)
        while self.reader.peak() != '}':
            s += self.reader.peak()
            self.reader.next()
        lst = s.split(',')
        # case {n}
        if len(lst) == 1:
            num = int(lst[0])
            for i in range(num-1):
                mid = State()
                nfaGraph.end.addPath(edge,mid)
                nfaGraph.end = mid
        else:
            # case {n,}
            if lst[0] != '' and lst[1] == '':
                min = int(lst[0])
                pre = None
                for i in range(min-1):
                    mid = State()
                    pre = nfaGraph.end
                    nfaGraph.end.addPath(edge,mid)
                    nfaGraph.end = mid
                nfaGraph.end.addPath(EPSILON,pre)
            elif lst[0] == '' and lst[1] != '':
                self.isMaxMatch = True
                # case {,m}
                max = int(lst[1])
                end = State()
                for i in range(max-1):
                    mid = State()
                    nfaGraph.end.addPath(edge, mid)
                    nfaGraph.end.addPath(EPSILON,end)
                    nfaGraph.end = mid
                nfaGraph.end.addPath(EPSILON, end)
                nfaGraph.end = end
            else:
                # case {n,m}
                min = int(lst[0])
                max = int(lst[1])
                # draw min NFA
                for i in range(min-1):
                    mid = State()
                    nfaGraph.end.addPath(edge,mid)
                    nfaGraph.end = mid
                # draw max NFA
                i = min
                end = State()
                while i < max:
                    mid = State()
                    nfaGraph.end.addPath(edge, mid)
                    nfaGraph.end.addPath(EPSILON, end)
                    nfaGraph.end = mid
                    i += 1
                nfaGraph.end.addPath(EPSILON, end)
                nfaGraph.end = end

    def regex2nfa(self) -> NFA:
        nfaGraph = None
        # check ^ and $
        assert isinstance(self.reader ,Reader)
        if self.reader.peak() == '^':
            self.isHat = True
            self.reader.next()
        elif self.reader.tail() == '$':
            self.isDoller = True
            # if doller reverse the pattern  abcd -> dcba
            self.reader.string = self.reader.string[::-1]
            self.reader.next()
        elif self.reader.peak() == '[':
            self.isRact = True
            self.reader.next()
            # if [^abc] we will matches characters with abd removed
            if self.reader.peak() == '^':
                newStr = 'qwertyuiopasdfghjklzxcvbnm1234567890 '
                while self.reader.hasNext():
                    ch = self.reader.peak()
                    newStr = newStr.replace(ch,'')
                    self.reader.next()
                # use new character set
                self.reader = Reader(newStr)
        while self.reader.hasNext():
            ch = self.reader.next()
            edge = None
            if ch == '.':
                edge = '.'
            elif ch == ']':
                continue
            elif ch == '{':
                self.parseRepeat_n_m(self.reader.get(self.reader.cur-2),nfaGraph)
                continue
            elif ch == '}':
                continue
            elif ch == '\\':
                nextCh = self.reader.next()
                if nextCh == 'd':
                    edge = "\\d"
                elif nextCh == 's':
                    edge = '\\s'
                elif nextCh == 'w':
                    edge = '\\w'
                else:
                    edge = nextCh
            else:
                edge = ch

            if edge is not None:
                start = State()
                end = State()
                start.addPath(edge,end)
                newNfa = NFA(start,end)
                self.checkRepeat(newNfa)
                if nfaGraph == None:
                    nfaGraph = newNfa
                else:
                    if self.isRact:
                        nfaGraph.addParallelGraph(edge)
                    else:
                        nfaGraph.addSeriesGraph(newNfa)
        if self.isRact:
            end = State()
            for nextState in nfaGraph.start.edgeMap.values():
                nextState[0].addPath(EPSILON,end)
            nfaGraph.end = end
        return nfaGraph

    def checkRepeat(self,nfa:NFA):
        assert isinstance(self.reader ,Reader)
        ch = self.reader.peak()
        if ch == '*':
            nfa.repeatStar()
            self.reader.next()
        elif ch == '+':
            nfa.repeatPlus()
            self.reader.next()

    def getNewText(self,matchRange:tuple,repl:str,text:str):
        ix = matchRange[0]
        iy = matchRange[1]
        newText = ''
        for i in range(0, ix):
            newText += text[i]
        newText += repl
        for i in range(iy, len(text)):
            newText += text[i]
        return newText

    def match(self,text:str):
        assert isinstance(self.nfa, NFA)
        start = self.nfa.start
        # self.startIndex = 0
        if self.isDoller:
            text = text[::-1]
        # index
        startIndex = 0
        endIndex = -1
        # find the match index
        l = len(text)
        for i in range(l):
            subStr = text[:(l-i)]
            ret = self.isMatch(subStr,0,start)
            if ret:
                endIndex = l-i-1
                break
        # return match range
        if endIndex == -1:
            if self.isMaxMatch:
                logging.info('pattern: ' + self.reader.string + ' match text: ' + text)
                return (0,0)
            logging.info('pattern: ' + self.reader.string +' not match text: ' + text)
            return None
        else:
            logging.info('pattern: ' + self.reader.string + ' match text: ' + text)
            if self.isDoller:
                return (l-endIndex-1,l-1+1)
            return (startIndex,endIndex+1)

    def search(self,text:str):
        assert isinstance(self.nfa, NFA)
        start = self.nfa.start
        # self.startIndex = 0
        if self.isDoller:
            text = text[::-1]
        # index
        startIndex = 0
        endIndex = -1
        # find the match index
        l1 = len(text)
        for i in range(l1):
            startIndex = i
            subStr1 = text[i:]
            l2 = len(subStr1)
            for j in range(l2):
                subStr2 = subStr1[:(l2-j)]
                ret = self.isMatch(subStr2,0,start)
                if ret:
                    endIndex = l1-j-1
                    logging.info('pattern: ' + self.reader.string + ' match text: ' + text)
                    if self.isDoller:
                        return (l1 - endIndex - 1, l1 - 1+1)
                    return (startIndex, endIndex+1)
            if self.isHat or self.isDoller:
                break
        if endIndex == -1:
            if self.isMaxMatch:
                logging.info('pattern: ' + self.reader.string + ' match text: ' + text)
                return (0,0)
            logging.info('pattern: ' + self.reader.string + ' match text: ' + text)
            return None

    def sub(self,pattern:str,repl:str,text:str,count=0) -> str:
        if count > 0:
            for i in range(count):
                self.compile(pattern)
                matchRange = self.search(text)
                if not matchRange:
                    break
                text = self.getNewText(matchRange,repl,text)
            return text
        else:
            self.compile(pattern)
            matchRange = self.search(text)
            while matchRange:
                text = self.getNewText(matchRange,repl,text)
                self.compile(pattern)
                matchRange = self.search(text)
            return text

    def split(self,pattern,text:str) -> list:
        self.compile(pattern)
        matchRange = self.search(text)
        lst = []
        while matchRange:
            ix = matchRange[0]
            iy = matchRange[1]
            lst.append(text[0:ix])
            text = text[iy:]
            self.compile(pattern)
            matchRange = self.search(text)
        lst.append(text)
        return lst

    def isMatch(self,text,pos,curState:State) -> bool:
        if pos == len(text):
            stateLst = [] #type: List[State]
            if curState.edgeMap.__contains__(EPSILON):
                stateLst = curState.edgeMap.get(EPSILON) # type: ignore
            for nextState in stateLst:
                if self.isMatch(text,pos,nextState):
                    return True
            if curState.IsEnd:
                return True
            return False
        #assert isinstance(curState.edgeMap,dict)
        for edge in curState.edgeMap.keys():
            if EPSILON.__eq__(edge):
                for nextState in curState.edgeMap.get(edge): # type: ignore
                    if self.isMatch(text,pos,nextState):
                        return True
            else:
                matchStrategy = self.matchStrategyManager.getStrategy(edge)
                if not matchStrategy.isMatch(text[pos], edge):
                    continue
                elif self.isRact and not '.'.__eq__(edge):
                    assert isinstance(self.nfa, NFA)
                    self.nfa.start.IsEnd = True
                for nextState in curState.edgeMap.get(edge): # type: ignore
                    if self.isMatch(text,pos+1,nextState):
                        return True
        return False

    def drawGraph(self,dot:Digraph,edges:list,node:State,markSet:set) -> Optional[None]:
        if markSet.__contains__((node.ID)):
            return None
        markSet.add(node.ID)
        for key in node.edgeMap.keys():
            nextNode = node.edgeMap.get(key)
            dot.node(str(nextNode[0].ID),key) # type: ignore
            edge = '' + str(node.ID) + str(nextNode[0].ID) # type: ignore
            edges.append(edge)
        return None

    def findAllNode(self,node:State,nodeMap) -> None:

        if nodeMap.__contains__(node.ID):
            return
        nodeMap[node.ID] = node
        for v in node.edgeMap.values():
            self.findAllNode(v[0],nodeMap)

    def visualize(self,fileName:str) -> None:
        # use dot -Tpng fileName.dot -o fileName.png to generate picture
        res = list()
        res.append('digraph G {')
        res.append(' rankdir=BT;')

        nodeMap = {} #type: Dict[str,State]
        if self.nfa is not None:
            start = self.nfa.start
            self.findAllNode(start,nodeMap)
            nodeMap.items()
            for node in nodeMap.values():
                res.append(' node{}[label="{}"];'.format(node.ID, node.ID))
            for node in nodeMap.values():
                for key in node.edgeMap.keys():
                    for value in node.edgeMap[key]:
                        if key[0] == '\\':
                            key = '/'+ key[1]
                        res.append('node{} -> node{} [ label="{}" ];'.format(node.ID, value.ID,key))
            res.append('}')
            file = open('../awt/'+fileName+'.dot', 'w')
            file.write("\n".join(res))
            file.close()
            logging.info("\n".join(res))