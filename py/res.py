#!/usr/bin/env python3

class Un:
    def __init__(self, number=None, part=None):
        self.number = number
        self.part = part
    def __repr__(self):
        number = self.number
        if self.number is None:
            number = "??"
        if self.part:
            return "u{}_{}".format(number, self.part)
        return "u{}".format(number)
    def __add__(self, other):
        if self.number and self.number and (self.number != other.number or not self.part or not other.part or self.part == other.part):
            raise Exception()
        return self.__class__(self.number)


class Matrix:
    def __init__(self, rows, cols, rowdescrs=None, coldescrs=None, flatvals=None):
        self.rows = rows
        self.cols = cols 
        self.m = [ [0.0
                    for _j in range(cols)]
                  for _i in range(rows)]
        if not rowdescrs:
            rowdescrs = [Un() for _i in range(rows)]
        self.rowdescrs = rowdescrs
        if not coldescrs:
            coldescrs = [Un() for _i in range(rows)]
        self.coldescrs = coldescrs
        if flatvals:
            for i, v in enumerate(flatvals):
                self.m[i//cols][i%cols] = v

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

    def cutpart(self, rows, cols):
        res = self.__class__(len(rows), len(cols), [self.rowdescrs[row] for row in rows], [self.coldescrs[col] for col in cols])
        for rowId, rowA in enumerate(rows):
            res[rowId] = [self[rowA][c] for c in cols]
        return res

    @classmethod
    def prodA1(cls, a, b):
        res = cls.prodA2(a, b)
        res.swapcol(0, 1)
        res.swaprow(0, 1)
        return res

    @classmethod
    def prodA2(cls, a, b):
        coldescrs = [a.coldescrs[0], a.coldescrs[1] + b.coldescrs[0], b.coldescrs[1], ""]
        rowdescrs = [a.rowdescrs[0], a.rowdescrs[1] + b.rowdescrs[0], b.rowdescrs[1], ""]
        res = cls(3, 4, coldescrs, rowdescrs)
        res[0] = a[0] + [a[0][2]]
        res[1] = [a[1][0], a[1][1]+b[0][0], b[0][1], a[1][2]+b[0][2]]
        res[2] = [0.0, b[1][0], b[1][1], b[1][2]]
        return res


if __name__ == "__main__":
    a1 = Matrix(2, 3, [Un(0),    Un(1, 1)], [Un(0),    Un(1, 1), ""], [1, 0, 0, 1, -1, 0])
    a2 = Matrix(2, 3, [Un(1, 2), Un(2, 1)], [Un(1, 2), Un(2, 1), ""],       [-1, 1, 0, 1, -1, 0])
    print(a1)
    print(a2)

    b1 = Matrix.prodA1(a1,a2)
    print(b1)
    b1 = b1.cutpart([1,2], [1,2,3])
    print(b1)