'''
Created on Feb 26, 2019

@author: gosha
'''

from copy import copy
from functools import reduce

import Main
from Tree import recFind
import tkinter as tk


class Table(object):

    def __init__(self, rows, columns, defaultValue = 0, symetrical = False):
        if(type(rows) == int):
            rows = list(range(rows))
        if(type(columns) == int):
            columns = list(range(columns))

        if(symetrical):
            assert(len(rows) == len(columns))

        self.rows = rows
        self.columns = columns
        self.symetrical = symetrical
        self.defaultValue = defaultValue
        self.table = [[defaultValue] * len(columns)] * len(rows)
        self.table = list(map(lambda l: list(l), self.table))
        self.compare = [None, None]

    def setValue(self, row, column, value):
        if(type(row) != int):
            row = self.rows.index(row)
        if(type(column) != int):
            column = self.columns.index(column)

        self.table[row][column] = value

        if(self.symetrical):
            self.table[column][row] = value

    def clear(self, row, column):
        if(type(row) != int):
            row = self.table.index(row)
        if(type(column) != int):
            column = self.table.index(column)

        self.table[row][column] = self.itemClass()

        if(self.symetrical):
            self.table[column][row] = self.itemClass()

    def getValue(self, row, column):
        if(type(row) != int):
            row = self.rows.index(row)
        if(type(column) != int):
            column = self.columns.index(column)

        return(self.table[row][column])

    def display(self, master, row = 0, column = 0, width = 720, height = 800, headers = True):

        def setCompare(x, row):
            self.compare[x] = str(self.rows[row])

        master.title = "Difference Table"
        window = tk.Frame(master, width = width, height = height, relief = tk.RAISED, borderwidth = 3)
        window.pack()

        for row in range(len(self.table)):
            if(headers):
                label = tk.Button(window, text = str(self.rows[row]), command = lambda row = row: setCompare(0, row))
                label.grid(row = row + 1, column = 0)
            for column in range(len(self.table[row])):
                if(headers):
                    label = tk.Button(window, text = str(self.columns[column]), command = lambda column = column: setCompare(1, column))
                    label.grid(row = 0, column = column + 1)
                label = tk.Label(window, text = str(self.getValue(row, column)))
                label.grid(row = row + headers, column = column + headers)

    def compareLoop(self, proteins, colorEnabled):
        self.compareLoopRunning = True
        while(self.compareLoopRunning):
            if(self.compare[0] != None and self.compare[1] != None):
                print(*self.compare)
                withBestGaps = Main.insertBestGaps(proteins[self.compare[0]][0], proteins[self.compare[1]][0])
                Main.compare(*withBestGaps, colorEnabled)
                self.compare = [None, None]

    def exportTable(self, filename):
        out = ''

        for column in range(len(self.columns)):
            out += ',' + str(self.columns[column])

        for row in range(len(self.rows)):
            out += '\n' + str(self.rows[row])

            for column in range(len(self.columns)):
                value = self.table[row][column]
                out += ',' + str(value)

        file = open(filename, 'w')
        file.write(out)

    def importTable(self, fileName = "Differences.csv", toType = int):
        with open(fileName) as f:
            lines = f.readlines()

        splitCSV = [list(map(lambda x: x, line.split(','))) for line in lines]

        for rowNumber in range(1, len(splitCSV)):
            row = splitCSV[rowNumber]
            for columnNumber in range(1, len(row)):
                self.setValue(row[0], splitCSV[0][columnNumber], toType(row[columnNumber]))

    def copy(self):
        out = Table(self.rows, self.columns, self.itemClass, self.defaultValue, self.symetrical)
        out.table = list(map(lambda l: list(l), self.table))
        return(out)

    def listValues(self):
        return(reduce(lambda x, y: x + y, self.table))

    def getBest(self, score = lambda v, r, c: v, score2 = lambda r, c, v: 0, condition = lambda r, c, v: True, multiple = False):
        out = None
        m = None
        done = False
        while(not(done)):
            restart = False
            for rNumber in range(len(self.rows)):
                r = copy(self.rows[rNumber])
                for cNumber in range(rNumber if self.symetrical else len(self.columns)):
                    c = copy(self.columns[cNumber])
                    scoreA = score(copy(self.getValue(r, c)), r, c)
                    scoreB = score2(copy(self.getValue(r, c)), r, c)
                    if((m == None or scoreA > m[0] or (scoreA == m[0] and scoreB > m[1])) and (condition(self.getValue(r, c), r, c))):
                        out = [r, c]
                        m = [scoreA, scoreB]
                    if(out != None and multiple and scoreA == m[0] and scoreB == m[1] and not((r in out) and (c in out))):
                        if(r in out):
                            for org in out:
                                if(not(condition(self.getValue(org, c), org, c))):
                                    break
                            else:
                                # print("%s works with %s as it has a score with %s of %s" % (c, out, r, scoreA))
                                out.append(c)
                                # print("Out is now %s\n-----" % (out))
                                restart = True
                                break
                        if(c in out):
                            for org in out:
                                if(not(condition(self.getValue(r, org), r, org))):
                                    break
                            else:
                                # print("%s works with %s as it has a score with %s of %s" % (r, out, c, scoreA))
                                out.append(r)
                                # print("Out is now %s\n-----" % (out))
                                restart = True
                                break

                if(restart):
                    break
            else:
                break

        # print("Answer is %s with score %s\n**********" % (out, m[0]))
        return(out)

    def map(self, f = lambda v, r, c: v):
        out = self.copy()
        for r in self.rows:
            for c in self.columns:
                out.table[r][c] = f(self.table[r][c], r, c)
        return(out)

    def find(self, o):
        return(recFind(self.table, o))


def getDictionary(fileName = "Proteins.csv"):
    with open(fileName) as f:
        lines = f.readlines()
    out = {}
    for line in lines:
        if(line[-1] == '\n'):
            line = line[:-1]
        splitLine = line.split(',')
        out[splitLine[0]] = splitLine[1:]
    return(out)


def differenceTable(proteins, verbose = False):

    table = Table(list(proteins.keys()), list(proteins.keys()), 0, True)
    count = 0
    for a in range(len(proteins)):
        for b in range(a):
            if(verbose):
                print("Generating difference table: %s%%: %s" % (round(count / (len(proteins) * (len(proteins) - 1) / 200)), list(proteins.keys())[a] + " - " + list(proteins.keys())[b]))
            withBestGaps = Main.insertBestGaps(proteins[list(proteins.keys())[a]][0], proteins[list(proteins.keys())[b]][0])
            score = Main.score(withBestGaps[0], withBestGaps[1])
            table.setValue(a, b, 0 - score)
            count += 1
    return(table)


def importDifferenceTable(fileName = "Differences.csv"):
    with open(fileName) as f:
        lines = f.readlines()
    columns = lines[0].split(',')[1:]
    rows = [row.split(',')[0] for row in lines[1:]]
    table = Table(rows, columns, symetrical = True)
    table.importTable(fileName)
    return(table)
