'''
Created on Feb 21, 2019

@author: Gosha
'''

import threading
import time

from Table import *
from Tree import *

colors = {
    "black": "\033[30m",
    "red": "\033[31m",
    "green": "\033[32m",
    "orange": "\033[33m",
    "blue": "\033[34m",
    "purple": "\033[35m",
    "cyan": "\033[36m",
    "lightgrey": "\033[37m",
    "darkgrey": "\033[90m",
    "lightred": "\033[91m",
    "lightgreen": "\033[92m",
    "yellow": "\033[93m",
    "lightblue": "\033[94m",
    "pink": "\033[95m",
    "lightcyan": "\033[96m"}


def color(c, overide = None):
    global colorEnabled
    if(overide if overide != None else colorEnabled):
        return(colors[c])
    else:
        return('')


def weight(f):
    if(f == "constant"):
        return(lambda x: 1)
    if(f == "inverse exponential"):
        return(lambda x: 1 / 2 ** (x / 4.25))


def insertGap(a, b, position, n):
    if(n > 0):
        a = a[:position] + '_' * n + a[position:]
    if(n < 0):
        b = b[:position] + '_' * (0 - n) + b[position:]
    return(a, b)


def insertGaps(a, b, gaps):
    assert(len(gaps) <= min(len(a), len(b)))

    outA = ''
    outB = ''

    for i in range(max(len(a), len(b))):
        if(len(gaps) > i):
            outA += '_' * gaps[i] if(gaps[i] > 0) else ''
            outB += '_' * (0 - gaps[i]) if(gaps[i] < 0) else ''
        outA += a[i] if(len(a) > i) else ''
        outB += b[i] if(len(b) > i) else ''

    return(outA, outB)


def score(a, b, start = 0, stop = None, w = "constant"):
    if(type(w) == str):
        w = weight(w)

    out = 0
    b += '_' * (len(a) - len(b)) if(len(a) > len(b)) else ''
    a += '_' * (len(b) - len(a)) if(len(b) > len(a)) else ''

    if(stop == None):
        stop = len(a)
    else:
        stop = min(stop, len(a))

    for i in range(start, stop):
        if(a[i] != b[i] or (a[i] == '_' and b[i] == '_')):
            out -= w(i - start)
    return(out)


def insertBestGaps(a, b, M = 16, startM = 32, length = None, w = "inverse exponential"):
    if(type(w) == str):
        w = weight(w)

    gaps = []
    for start in range(min(len(a), len(b))):
        best = 0
        withGaps = insertGaps(a, b, gaps)
        end = None if length == None else start + length
        bestScore = score(withGaps[0], withGaps[1], start, end, w)

        checkTo = startM if start == 0 else M
        for n in range(-checkTo, checkTo + 1):
            withGaps = insertGaps(a, b, gaps + [n])
            s = score(withGaps[0], withGaps[1], start, end, w)
            if(s > bestScore):
                best = n
                bestScore = s
        gaps += [best]

    return(insertGaps(a, b, gaps))


def compare(a, b, colorOveride = None):
    print(str(color("yellow", colorOveride)))
    print(color("yellow", colorOveride) + ''.join(a))
    for i in range(min(len(a), len(b))):
        if(a[i] == b[i]):
            print(color("green", colorOveride) + '|', end = '')
        else:
            print(color("red", colorOveride) + '|', end = '')
    print('\n' + color("yellow", colorOveride) + ''.join(b))
    print(color("green", colorOveride))


if __name__ == '__main__':
    colorEnabled = (input("Color?: ").lower()[0] == 'y')
    start = time.time()

    master = tk.Tk()
    master.title("ASTEAMS 2019")

    print("Getting proteins")
    proteins = getDictionary("TestProteins.csv")
    colors = getDictionary("Colors.csv")
    namesToColors = {name: colors[proteins[name][1]][0] for name in proteins}

    if(input("Would you like to use the differences in Differences.csv?: ").lower()[0] == 'y'):
        print("Importing difference table")
        table = importDifferenceTable()
    else:
        print("Generating differences")
        table = differenceTable(proteins, verbose = True)
        print(time.time() - start)
        if(input("Would you like to overwrite the difference table, Differences.csv?: ").lower()[0] == 'y'):
            print('Exporting table')
            table.exportTable("Differences.csv")

    if(input("Display table?: ").lower()[0] == 'y'):
        print("Displaying table")
        table.display(tk.Toplevel(master), 1, 0)

        print("Creating compare loop thread")
        compareLoopThread = threading.Thread(None, table.compareLoop, "Compare loop thread", args = (proteins, colorEnabled,), daemon = True)
        print("Starting compare loop thread")
        compareLoopThread.start()

    if(input("Display tree?: ").lower()[0] == 'y'):
        print("Creating tree")
        tree = Tree(table)
        print("Generating tree")
        tree.generate(True, 0)
        print("Drawing tree")
        tree.draw(tk.Toplevel(master), namesToColors, 0, 0, size = 2)

    print("Starting master tk mainloop")
    # print(time.time() - start)
    master.mainloop()
