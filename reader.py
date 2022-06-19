'''
The Reader class serves as an input buffer from which we can fetch characters
'''

class Reader(object):
    def __init__(self,partten: str) -> None:
        self.string = partten
        self.cur = 0

    def tail(self) -> str:
        return self.string[-1]

    def peak(self) -> str:
        if self.cur == len(self.string):
            return '\0'
        return self.string[self.cur]

    def get(self,index) -> str:
        return self.string[index]

    def next(self) -> str:
        if self.cur == len(self.string):
            return '\0'
        index = self.cur
        self.cur += 1
        return self.string[index]

    def hasNext(self) -> bool:
        return self.cur < len(self.string)