'''
This file holds global variables and can generate globally unique IDs
'''

EPSILON = "Epsilon"
CHAR = "char";

ID = 0

def getId() -> int:
    global ID
    id = ID
    ID += 1
    return id

def resetID() -> None:
    global ID
    ID = 0