def fix(branch):
    if(type(branch) == str):
        return([branch])
    else:
        return([fix(b) for b in branch])

import sys
sys.path.append("/Users/gosha/Google Drive/Programming/EclipseProjects/ASTEAMS2019")
from Main import *
def example():
    branch = fix(eval(input("branch: ")))
    print(branch)
    t = turtle.Pen()
    t.hideturtle()
    drawBranch(t, branch, -300, 0, 24, 64, 1, deepestLevel(branch) - 1, colors = colors)
    
