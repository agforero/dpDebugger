#!/usr/bin/env python3
import time
import random 
import turtle
import threading
import tkinter as tk
from math import pi

def getRandomColor():
    candidates = [f"{i+7}" for i in range(3)] + [chr(j+97) for j in range(6)]
    #candidates = [chr(j+97) for j in range(6)]
    ret = "" 
    for _ in range(6): 
        ret += random.choice(candidates)
    return f"#{ret}"

class Chopstick:
    def __init__(self, canvas, x1, y1, x2, y2):
        self.color = "#fff"
        self.canvas = canvas
        self.position1 = [x1, y1]
        self.position2 = [x2, y2]
        self.drawing = canvas.create_line(x1, y1, x2, y2, width=5, fill=self.color)

    def getColor(self):
        return self.color

    def setColor(self, color):
        self.canvas.itemconfig(self.drawing, fill=color)

class State:
    def __init__(self, startVals):
        self.vals = startVals
        self.feed = []

    def addToFeed(self, output):
        self.feed.append(output.strip())

    def __str__(self):
        ret = str(self.vals) + ":\n"
        for output in self.feed:
            ret += f"{output}\n"
        return ret

def isChopOutput(line):
    if line.isspace(): return False
    for term in line.split():
        try: int(term)
        except ValueError: return False
    return True # only gets here if all are numbers (-1 is valid)

def startAnimation_actual(b, frameLabelStr, colors, chops, states, wait):
    if wait == "": wait = 0.5

    b["state"] = "disabled"

    for j, s in enumerate(states):
        for i, v in enumerate(s.vals):
            chops[i].setColor(colors[v])
        time.sleep(float(wait))
        frameLabelStr.set(f" Frame {j}/{len(states)-1}")

    for c in chops:
        c.setColor(colors[-1])
        
    b["state"] = "active"

def startAnimation(b, frameLabelStr, colors, chops, states, wait):
    th = threading.Thread(target=(lambda: startAnimation_actual(b, frameLabelStr, colors, chops, states, wait)), daemon=True)
    th.start()

def main():
    # get nphil from reading data
    f = open("log.txt", 'r')
    fileLines = f.readlines()

    nphil = 0
    for line in fileLines:
        try: 
            if line.isspace(): continue
            terms = [int(term) for term in line.split()]
            nphil = len(terms)
            break
        except: continue
    
    if nphil < 2: return # if there are less than two philosophers, break

    # get all States involved
    allStates = [State([-1 for _ in range(nphil)])]
    for line in fileLines:
        # determine if this line is printing chops[], or something else
        if isChopOutput(line):
            allStates.append(State([int(term) for term in line.split()]))

        else:
            allStates[-1].addToFeed(line)

    # calculate points using a Turtle
    # I'm unironically using a Turtle in a 300 level class
    canvasSize = 500
    offset = 20
    r = 2.5
    turtleCoords1 = []
    turtleCoords2 = []
    turtleCoords3 = []

    # you can't see it tho B-)
    turtleScreen = tk.Tk()
    turtleScreen.withdraw()
    turtleCanvas = tk.Canvas(turtleScreen)

    startX = canvasSize//2
    startY = canvasSize//2

    t1 = turtle.RawTurtle(turtleCanvas)
    t1.goto(startX, startY)
    l1 = canvasSize / nphil
    t1.goto(startX - (l1//2), startY - ((l1 * nphil) / (2 * pi)))
    t1.speed(10)

    for _ in range(nphil):
        turtleCoords1.append(t1.pos())
        t1.forward(l1)
        t1.left(360/nphil)

    t2 = turtle.RawTurtle(turtleCanvas)
    t2.goto(startX, startY)
    l2 = l1 * r
    t2.goto(startX - (l2//2), startY - ((l2 * nphil) / (2 * pi)) + offset)
    t2.speed(10)

    for _ in range(nphil):
        turtleCoords2.append(t2.pos())
        t2.forward(l2)
        t2.left(360/nphil)

    t3 = turtle.RawTurtle(turtleCanvas)
    t3.goto(startX, startY)
    l3 = l1 * r * 1.08
    t3.goto(startX - (l3//2), startY - ((l3 * nphil) / (2 * pi)) + offset)
    t3.speed(10)

    for _ in range(nphil):
        turtleCoords3.append(t3.pos())
        t3.forward(l3)
        t3.left(360/nphil)

    turtleScreen.destroy()

    # get usable coords from Turtle coords
    coords1 = []
    for tc in turtleCoords1:
        coords1.append([int(c) for c in tc])

    coords2 = []
    for tc in turtleCoords2:
        coords2.append([int(c) for c in tc])

    coords3 = []
    for tc in turtleCoords3:
        coords3.append([int(c) for c in tc])

    # initialize tkinter stuff
    random.seed()
    top = tk.Tk()
    top.title("Dining Philosophers Debugger")
    top.resizable(False, False)

    topPart = tk.Frame(top)
    topPart.pack()

    canvasFrame = tk.Frame(topPart, padx=10, pady=10)
    canvasFrame.pack(side=tk.LEFT)

    chopCanvas = tk.Canvas(canvasFrame, width=canvasSize, height=canvasSize, bg="black")
    chopCanvas.pack()

    for i, c in enumerate(coords3):
        chopCanvas.create_text(c[0], c[1], text=f"p{i} left", fill="#fff")

    allChops = []
    for i in range(nphil):
        newChop = Chopstick(chopCanvas, coords1[i][0], coords1[i][1], coords2[i][0], coords2[i][1])
        allChops.append(newChop)

    colors = {}
    colors[-1] = "#777"
    for i in range(nphil):
        colors[i] = getRandomColor()

    # playing the animation
    labelFrame = tk.Frame(topPart, padx=10, pady=10)
    labelFrame.pack(side=tk.LEFT)

    keyFrame = tk.Frame(labelFrame)
    keyFrame.pack(side=tk.TOP)

    for i in range(nphil):
        thisCanvas = tk.Canvas(keyFrame, width=165, height=20)
        thisCanvas.pack(side=tk.TOP)

        thisCanvas.create_rectangle(0, 0, 20, 20, fill=colors[i])
        thisCanvas.create_text(75, 10, text=f"philosopher {i}")

    bottomPart = tk.Frame(top, pady=10)
    bottomPart.pack()

    timeLabel = tk.Label(bottomPart, text="Seconds per frame: ")
    timeLabel.pack(side=tk.LEFT)

    timeEntry = tk.Entry(bottomPart, width=3, font="TkFixedFont")
    timeEntry.pack(side=tk.LEFT)

    frameLabelStr = tk.StringVar()
    frameLabelStr.set(f" Frame 0/{len(allStates)-1}")
    frameLabel = tk.Label(bottomPart, textvariable=frameLabelStr)

    startButton = tk.Button(bottomPart, text="Start!", command=(lambda: startAnimation(startButton, frameLabelStr, colors, allChops, allStates, timeEntry.get())))
    
    startButton.pack(side=tk.LEFT)
    frameLabel.pack(side=tk.LEFT)

    top.mainloop()

if __name__ == "__main__":
    main()