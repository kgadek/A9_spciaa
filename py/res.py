#!/usr/bin/env python3

class Un:
    def __init__(self, number, part=None):
        self.number = number
        self.part = part
    def __repr__(self):
        if self.part:
            return "u{}_{}".format(self.number, self.part)
        return "u{}".format(self.number)
    def __add__(self, other):
        if self.number != other.number or not self.part or not other.part or self.part == other.part:
            raise Exception()
        return self.__class__(self.number)


class Matrix:
    def __init__(self, rows, cols, rowdescrs=None, coldescrs=None):
        self.rows = rows
        self.cols = cols 
        self.m = [ [0.0
                    for _j in range(cols)]
                  for _i in range(rows)]
        if not rowdescrs:
            rowdescrs = [Un(i) for i in range(rows)]
        self.rowdescrs = rowdescrs
        if not coldescrs:
            coldescrs = [Un(i) for i in range(rows)]
        self.coldescrs = coldescrs

    def __repr__(self):
        res = "{0:>13}".format("| ")
        for cold in self.coldescrs:
            res += "{:>10} | ".format(cold)
        res += "\n"
        for row,rowd in zip(self.m, self.rowdescrs):
            res += "|{:^10}| ".format(rowd)
            for x in row:
                res += "{0:10.6} | ".format(float(x))
            res += "\n"
        return res

    def __getitem__(self, row):
        return self.m[row]

    def __setitem__(self, row, val):
        self.m[row] = val
        return self

    def swaprow(self, rowA, rowB):
        self.m[rowA], self.m[rowB] = self.m[rowB], self.m[rowA]
        self.rowdescrs[rowA], self.rowdescrs[rowB] = self.rowdescrs[rowB], self.rowdescrs[rowA]
        return self

    def swapcol(self, colA, colB):
        for row in self.m:
            row[colA], row[colB] = row[colB], row[colA]
        self.coldescrs[colA], self.coldescrs[colB] = self.coldescrs[colB], self.coldescrs[colA]
        return self

    def __add__(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise Exception()
        res = self.__class__(self.rows, self.cols,
            [x+y for x,y in zip(self.rowdescrs, other.rowdescrs)],
            [x+y for x,y in zip(self.coldescrs, other.coldescrs)])
        for rowId, (rowA, rowB) in enumerate(zip(self.m, other.m)):
            res[rowId] = [x+y for x,y in zip(rowA, rowB)]
        return res

