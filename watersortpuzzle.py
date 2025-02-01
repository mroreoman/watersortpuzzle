from enum import Enum
import random

class Liquid(Enum):
    BLUE = "B"
    RED = "R"
    GREEN = "G"
    
class Tube:
    max = 4
    
    def __init__(self, liquids: list[Liquid]):
        self.liquids = liquids

    def top(self):
        if not self.liquids: return None
        return self.liquids[-1]

    def __str__(self):
        s = ""
        for liquid in self.liquids:
            s += liquid.value + " "
        s += "_ " * (Tube.max - len(self.liquids))
        return s

def pour(giving: Tube, recieving: Tube):
        while giving.top() and (giving.top() == recieving.top() or not recieving.top()):
            if len(recieving.liquids) < Tube.max:
                recieving.liquids.append(giving.liquids.pop(-1))
            else:
                break

def minipour(giving: Tube, recieving: Tube):
    #pour 1 liquid
    pass

#tube1 = Tube([Liquid.BLUE, Liquid.RED])
#tube2 = Tube([Liquid.RED, Liquid.RED, Liquid.RED])

#print(tube1)
#print(tube2)
#print("pouring 1 into 2")
#pour(tube2, tube1)
#print(tube1)
#print(tube2)

tubes = []
for liquid in Liquid:
    tubes.append(Tube([liquid,]*Tube.max))
tubes.append(Tube([]))
tubes.append(Tube([]))
tubes.append(Tube([]))
for tube in tubes:
    print(tube)
#for _ in range(999):
#    pour(random.choice(tubes), random.choice(tubes))
minipour(tubes[1], tubes[4])
for tube in tubes:
    print(tube)