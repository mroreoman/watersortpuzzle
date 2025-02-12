from enum import Enum
import random
# import tkinter as tk

class Liquid(Enum):
    BLUE = "B"
    RED = "R"
    GREEN = "G"
    
class Tube:
    max = 4
    
    def __init__(self, liquids: list[Liquid]):
        self.liquids = liquids

    def pop(self):
        return self.liquids.pop()
    
    def push(self, liquid:Liquid):
        self.liquids.append(liquid)

    def top(self):
        if not self.liquids: return None
        return self.liquids[-1]

    def space(self):
        return Tube.max - len(self.liquids)
    
    def solved(self):
        if not self.liquids:
            return True
        
        if len(self.liquids) != Tube.max:
            return False

        color = self.liquids[0]
        for liquid in self.liquids:
            if liquid != color:
                return False
        return True

    def __str__(self):
        s = ""
        for liquid in self.liquids:
            s += liquid.value + " "
        s += "_ " * (Tube.max - len(self.liquids))
        return s

def pour(giving: Tube, receiving: Tube):
    while giving.top() and (giving.top() == receiving.top() or not receiving.top()):
        if receiving.space():
            receiving.push(giving.pop())
        else:
            break

def minipour(giving: Tube, receiving: Tube):
    if giving.top() and receiving.space():
        # print(f"{giving} -> {receiving}")
        receiving.push(giving.pop())

tubes = []

def printTubes():
    print()
    for i, tube in enumerate(tubes):
        print(f"{i+1}: {tube}")
    print()

def init():
    for liquid in Liquid:
        tubes.append(Tube([liquid,]*Tube.max))
    for _ in range(1):
        tubes.append(Tube([]))
    printTubes()

def scramble():
    for _ in range(30):
        minipour(random.choice(tubes), random.choice(tubes))
    printTubes()

def solved():
    for tube in tubes:
        if not tube.solved():
            return False
    return True

init()
scramble()

while True:
    giving = input("giving: ").lower().strip()
    try:
        giving = tubes[int(giving)-1]
    except:
        break

    receiving = input("receiving: ").lower().strip()
    try:
        receiving = tubes[int(receiving)-1]
    except:
        break

    print(f"{giving} -> {receiving}")
    pour(giving, receiving)
    
    if solved():
        break

    printTubes()

printTubes()