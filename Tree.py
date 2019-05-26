'''
Created on Mar 1, 2019

@author: gosha
'''

from math import cos, pi
import turtle

import tkinter as tk

canvasPosition = [0, 0]
zoom = 1


class Tree(object):

    def __init__(self, table):
        self.branches = list(table.rows)
        self.table = table

    def link(self, orgs):
        branch = []
        for org in orgs:
            tempBranch = self.branches[recFind(self.branches, org)[0]]
            if(type(tempBranch) == str):
                tempBranch = [tempBranch]
            else:
                tempBranch = list(tempBranch)
            del self.branches[recFind(self.branches, org)[0]]
            branch.append(tempBranch)

        self.branches.append(branch)

    def generate(self, combine = True, colors = None):

        def score(v, r, c):
            return(-v)

        def condition(v, r, c):
            return(recFind(self.branches, r)[0] != recFind(self.branches, c)[0])

        nextOrgs = self.table.getBest(score, condition = condition, multiple = True)
        while(nextOrgs != None):
            self.link(nextOrgs)
            nextOrgs = self.table.getBest(score, condition = condition, multiple = True)

    def draw(self, master, colors, row = 0, column = 0, width = 1440, height = 800, size = 3):

        global defaultScreenSize, window, canvasPosition, speed, canvas

        window = tk.Frame(width = width, height = height, relief = tk.RAISED, borderwidth = 3)
#        window.grid(row = row, column = column)
        window.pack()
#        window.geometry("1440x800")
#        window.resizable(True, True)
        speed = 16

        canvas = turtle.Canvas(window, width = 4096, height = 2048)
        canvasPosition = [0, height / 2 - 1024]
        move(0, 0)

        t = turtle.RawTurtle(canvas)
        t.speed(0)

        master.bind("<KeyPress-Up>", down)
        master.bind("<KeyPress-Down>", up)
        master.bind("<KeyPress-Right>", right)
        master.bind("<KeyPress-Left>", left)
        master.bind("<KeyPress-p>", printCenter)
        master.bind("<KeyPress-r>", resetPosition)

        print(self.branches)

        t.hideturtle()
        if(size == 1):
            drawBranch(t, self.branches[0], -2048, 0, 16, 32, 1, deepestLevel(self.branches) - 2, colors = colors)
        elif(size == 2):
            drawBranch(t, self.branches[0], -2048, 0, 24, 64, 1, deepestLevel(self.branches) - 2, colors = colors)
        else:
            drawBranch(t, self.branches[0], -2048, 0, 32, 64, 2, deepestLevel(self.branches) - 2, colors = colors)


def drawBranch(t, b, x, y, height, length, step, distanceFromDL, size = 2, fontSize = 16, colors = None):
    t.width(size)

    space = height * recCount(b)

    s = y - space / 2
    for branchNumber in range(len(b)):
        branchY = s + height * recCount(b[branchNumber]) / 2
        s += height * recCount(b[branchNumber])
        branchX = x + length
        t.up()
        t.goto(x, y)
        t.down()
        if(colors == None):
            t.color("Black")
        else:
            t.color(branchColor(b[branchNumber], colors))

        if((type(b[branchNumber]) in [list, tuple, map, range]) and not(len(b[branchNumber]) == 0)):
            sCurve(t, x, branchX, y, branchY, step)
            drawBranch(t, b[branchNumber], branchX, branchY, height, length, step, distanceFromDL - 1, size, fontSize, colors)
        elif(type(b[branchNumber]) in [list, tuple, map, range]):
            t.fd(distanceFromDL * length)
            t.up()
            t.setx(t.position()[0] + fontSize / 2)
            t.sety(t.position()[1] - fontSize / 2)
            t.write(str(b[branchNumber][0]), font = ("Arial", fontSize, "normal"))
        else:
            t.fd(distanceFromDL * length)
            t.up()
            t.setx(t.position()[0] + fontSize / 2)
            t.sety(t.position()[1] - fontSize / 2)
            t.write(str(b[branchNumber]), font = ("Arial", fontSize, "normal"))


def sCurve(t, x0, x1, y0, y1, step):
    for x in range(round(x0), round(x1), step):
        xShift = cos(((x - x0) * pi) / (x1 - x0))
        y = (xShift - 1) * (y0 - y1) / 2 + y0
        t.goto(x, y)


def recFind(iterable, o):
    iterable = list(iterable)
    for itemNumber in range(len(iterable)):
        item = iterable[itemNumber]
        if(item == o):
            return([itemNumber])
        if(type(item) in [list, tuple, map, range]):
            result = recFind(item, o)
            if(result != None):
                return([itemNumber] + result)


def recCount(item):
    if(type(item) in [list, tuple, map, range]):
        return(sum([recCount(x) for x in item]))
    else:
        return(1)


def branchColor(b, colors):
    if(type(b) in [list, tuple, map, range]):
        out = branchColor(b[0], colors)
        for subB in b[1:]:
            bc = branchColor(subB, colors)
            if(bc != out):
                return("Black")
        return(out)

    if(b in colors.keys()):
        return(colors[b])
    return("Black")


def deepestLevel(item):
    if(type(item) in [list, tuple, map, range]):
        return(max([deepestLevel(x) for x in item]) + 1)
    else:
        return(0)


def move(x, y):
    global canvasPosition, canvas, t, speed

    canvasPosition[0] -= x * speed
    canvasPosition[1] -= y * speed

    canvas.place(x = canvasPosition[0], y = canvasPosition[1])


def up(_):
    move(0, 1)


def down(_):
    move(0, -1)


def right(_):
    move(1, 0)


def left(_):
    move(-1, 0)


def resetPosition(_):
    global canvasPosition
    canvasPosition = [0, 800 / 2 - 1024]
    move(0, 0)
    print("Reset")


def printCenter(_):
    global canvasPosition
    print(canvasPosition)
