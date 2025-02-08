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
        print(f"{giving} -> {receiving}")
        receiving.push(giving.pop())

tubes = []

def printTubes():
    print()
    for tube in tubes:
        print(tube)
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

init()
scramble()