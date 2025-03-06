from enum import Enum
import random
import tkinter as tk

NUM_TUBES = 20

class Liquid(Enum):
    RED = "#FF0000"
    GREEN = "#00FF00"
    BLUE = "#0000FF"
    YELLOW = "#FFFF00"
    ORANGE = "#FF8000"
    LIME = "#80FF00"
    PURPLE = "#FF00FF"
    PINK = "#FF0080"
    MAGENTA = "#8000FF"
    CYAN = "#00FFFF"
    MINT = "#00FF80"
    CORNFLOWER = "#0080FF"

class Tube:
    max = 4
    
    def __init__(self, liquids: list[Liquid]):
        self.liquids = liquids
        self.frame = tk.Frame(tube_frame, padx=3)
        self.frame.pack(side=tk.LEFT)
        self.button = tk.Button(self.frame, width=2)
        self.button.pack(side=tk.BOTTOM)
        self.labels:list[tk.Label] = []
        for i in range(Tube.max):
            label = tk.Label(self.frame, width=2, relief=tk.SOLID)
            label.pack(side=tk.BOTTOM)
            self.labels.append(label)
        for i, liquid in enumerate(self.liquids):
            self.labels[i].config(bg=liquid.value)

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
        self.labels[len(self.liquids)].config(bg=liquid.value)
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
            s += liquid.name + " "
        s += "_ " * (Tube.max - len(self.liquids))
        return s

class PrevMove:
    def start_move(giving, receiving):
        PrevMove.giving = giving
        PrevMove.receiving = receiving
        PrevMove.length = 0
        PrevMove.text = f"{giving} -> {receiving}"
    
    def clear():
        PrevMove.giving = None
        PrevMove.receiving = None
        PrevMove.length = 0
        PrevMove.text = None

if NUM_TUBES > len(list(Liquid)):
    NUM_TUBES = len(list(Liquid))

tubes:list[Tube] = []
selected_tube:Tube = None
board_start:list[list[Liquid]] = []

def pour(giving: Tube, receiving: Tube):
    if giving is receiving:
        return
    PrevMove.clear()
    print(f"{giving} -> {receiving}")
    PrevMove.start_move(giving, receiving)
    while giving.top() and (giving.top() == receiving.top() or not receiving.top()):
        if receiving.space():
            PrevMove.length += 1
            receiving.push(giving.pop())
        else:
            break

def minipour(giving: Tube, receiving: Tube):
    if giving.top() and receiving.space():
        receiving.push(giving.pop())
        if giving.top() is not receiving.top():
            giving.push(receiving.pop())
        else:
            # print(f"{giving} -> {receiving}")
            pass

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
    print(f"tube: {id(tube)}")
    print(f"button: {id(tube.button)}")

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
    message.config(text="generating board")
    liquids = list(Liquid)
    # if NUM_TUBES <= 4:
    if True:
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
    
    for _ in range(9999):
        minipour(random.choice(tubes), random.choice(tubes))
    
    message.config(text="")
    global board_start
    board_start.clear()
    for tube in tubes:
        tube_start = []
        for liquid in tube.liquids:
            tube_start.append(liquid)
        board_start.append(tube_start)
    print_tubes()
    print("\n".join(map(str, board_start)))

def reset():
    print("resetting board")
    clear()
    for tube_start in board_start:
        tubes.append(Tube(tube_start))
    for tube in tubes:
        tube.button.config(command = (lambda x: (lambda: click(x)))(tube))

def undo():
    if not PrevMove.giving or not PrevMove.receiving or not PrevMove.length:
        return
    print("undoing " + PrevMove.text)
    for _ in range(PrevMove.length):
        minipour(PrevMove.receiving, PrevMove.giving)
    PrevMove.clear()

root = tk.Tk()
root.title("water sort")
root.minsize(400,200)
root.tk.call('tk', 'scaling', 2.5)

tube_frame = tk.Frame()
tube_frame.pack(padx=3, pady=3)

buttons = tk.Frame()
buttons.pack(padx=3, pady=3)
reset_button = tk.Button(buttons, text="reset", command=reset)
reset_button.pack(side = tk.LEFT)
start_button = tk.Button(buttons, text="new game", command=init)
start_button.pack(side = tk.LEFT)
undo_button = tk.Button(buttons, text="undo", command=undo)
undo_button.pack(side = tk.LEFT)

message = tk.Label(text="welcome!")
message.pack(side = tk.BOTTOM)

root.mainloop()