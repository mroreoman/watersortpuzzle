from enum import Enum
import random
import tkinter as tk

NUM_TUBES = 4
if NUM_TUBES > 9:
    NUM_TUBES = 9

class Liquid(Enum):
    RED = "R"
    ORANGE = "O"
    YELLOW = "Y"
    GREEN = "G"
    CYAN = "C"
    BLUE = "B"
    PURPLE = "P"

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
    print(f"{giving} -> {receiving}")
    if giving is receiving:
        return
    while giving.top() and (giving.top() == receiving.top() or not receiving.top()):
        if receiving.space():
            receiving.push(giving.pop())
        else:
            break

def minipour(giving: Tube, receiving: Tube):
    if giving.top() and receiving.space():
        receiving.push(giving.pop())
        print(f"{giving} -> {receiving}")

tubes:list[Tube] = []
selected_tube:Tube = None

def print_tubes():
    print()
    for i, tube in enumerate(tubes):
        print(f"{i+1}: {tube}")
    print()

def solved():
    for tube in tubes:
        if not tube.solved():
            return False
    return True

def select(tube:Tube):
    global selected_tube
    # print("selected " + str(tube))
    tube.button.config(relief=tk.SUNKEN)
    selected_tube = tube

def deselect():
    global selected_tube
    # print("deselected " + str(selected_tube))
    selected_tube.button.config(relief=tk.RAISED)
    selected_tube = None

def finish_board():
    print("board solved")
    message.config(text="you won!")

def click(tube:Tube):
    # print(f"clicked {tube}")
    if not selected_tube:
        if tube.top(): # tube isn't empty
            select(tube)
    else:
        if (not tube.top()) or (selected_tube.top() == tube.top()): # can pour selected into tube
            pour(selected_tube, tube)
            deselect()
            if solved():
                finish_board()
        else:
            deselect()
            select(tube)

def clear():
    for tube in tubes:
        tube.frame.destroy()
    tubes.clear()
    message.config(text="")

def init():
    clear()
    liquids = list(Liquid)
    if NUM_TUBES <= 4:
        for _ in range(NUM_TUBES-1):
            tubes.append(Tube([liquids.pop(random.randint(0, len(liquids)-1)),]*Tube.max))
        tubes.append(Tube([]))
    else:
        for _ in range(NUM_TUBES-2):
            tubes.append(Tube([liquids.pop(random.randint(0, len(liquids)-1)),]*Tube.max))
        for _ in range(2):
            tubes.append(Tube([]))
    
    for tube in tubes:
        tube.button.config(command = (lambda x: (lambda: click(x)))(tube))
    
    for _ in range(20):
        minipour(random.choice(tubes), random.choice(tubes))
    
    print_tubes()

root = tk.Tk()
root.title("water sort")
root.minsize(400,200)
root.tk.call('tk', 'scaling', 2.5)

main = tk.Frame()
main.pack(padx=3, pady=3)

start = tk.Button(main, text="new game", command=init)
start.pack(side = tk.BOTTOM)

message = tk.Label(main, text="welcome!")
message.pack(side = tk.BOTTOM)

root.mainloop()