from enum import Enum
import random
import tkinter as tk

class Liquid(Enum):
    BLUE = "B"
    RED = "R"
    GREEN = "G"

class Tube:
    max = 4
    
    def __init__(self, liquids: list[Liquid]):
        self.liquids = liquids
        self.frame = tk.Frame(main, padx=3)
        self.frame.pack(side=tk.LEFT)
        self.button = tk.Button(self.frame, width=2)
        self.button.pack(side=tk.BOTTOM)
        self.labels:list[tk.Label] = []
        for i in range(Tube.max):
            label = tk.Label(self.frame, width=2, relief=tk.SOLID)
            label.pack(side=tk.BOTTOM)
            self.labels.append(label)
        for i, liquid in enumerate(self.liquids):
            self.labels[i].config(bg=liquid.name)

    def space(self):
        return Tube.max - len(self.liquids)

    def pop(self):
        if not self.liquids:
            return
        self.labels[len(self.liquids)-1].config(bg="white")
        return self.liquids.pop()
    
    def push(self, liquid:Liquid):
        if not self.space():
            return
        self.labels[len(self.liquids)].config(bg=liquid.name)
        self.liquids.append(liquid)

    def top(self):
        if not self.liquids: return None
        return self.liquids[-1]
    
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
        receiving.push(giving.pop())

tubes:list[Tube] = []
selected_tube:Tube = None

root = tk.Tk()
root.title("water sort")

main = tk.Frame()
main.pack(padx=3, pady=3)

def print_tubes():
    print()
    for i, tube in enumerate(tubes):
        print(f"{i+1}: {tube}")
    print()

def select(tube:Tube):
    global selected_tube
    print("selected " + str(tube))
    tube.frame.config(relief=tk.RAISED)
    selected_tube = tube

def deselect():
    global selected_tube
    print("deselected " + str(selected_tube))
    selected_tube.frame.config(relief=tk.FLAT)
    selected_tube = None

def click(tube:Tube):
    print(f"clicked {tube}")
    if not selected_tube:
        if tube.top(): # tube isn't empty
            select(tube)
    else:
        if (not tube.top()) or (selected_tube.top() == tube.top()): # can pour selected into tube
            pour(selected_tube, tube)
            deselect(selected_tube)
        else:
            select(tube)

def init():
    for liquid in Liquid:
        tube = Tube([liquid,]*Tube.max)
        tubes.append(tube)
    for _ in range(1):
        tubes.append(Tube([]))
    for tube in tubes:
        tube.button.config(command=lambda:select(tube)) # this is doing weird weird things
    print_tubes()

def scramble():
    for _ in range(30):
        minipour(random.choice(tubes), random.choice(tubes))
    print_tubes()

def solved():
    for tube in tubes:
        if not tube.solved():
            return False
    return True

init()
scramble()
main.mainloop()

while False:
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
        print_tubes()
        break

    print_tubes()