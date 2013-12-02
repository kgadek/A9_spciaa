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

    def gaussStep(self, baseRowId):
        if self.m[baseRowId][baseRowId] == 0:
            raise Exception()
        self.m[baseRowId] = [x / self.m[baseRowId][baseRowId] for x in self.m[baseRowId]]
        for rowId, _row in enumerate(self.m[baseRowId+1:], baseRowId+1):
            if self.m[rowId][baseRowId] != 0:
                self.m[rowId] = [x - self.m[rowId][baseRowId] * y for x, y in zip(self.m[rowId], self.m[baseRowId])]

    @classmethod
    def prodA1(cls, a, b):
        coldescrs = [a.coldescrs[0], a.coldescrs[1] + b.coldescrs[0], b.coldescrs[1], ""]
        rowdescrs = [a.rowdescrs[0], a.rowdescrs[1] + b.rowdescrs[0], b.rowdescrs[1], ""]
        res = cls(3, 4, coldescrs, rowdescrs)
        res[0] = a[0][:2] + [0.0, a[0][2]]
        res[1] = [a[1][0], a[1][1]+b[0][0], b[0][1], a[1][2]+b[0][2]]
        res[2] = [0.0, b[1][0], b[1][1], b[1][2]]
        res.swapcol(0, 1)
        res.swaprow(0, 1)
        res.gaussStep(0)
        return res

    @classmethod
    def prodA2(cls, a, b):
        coldescrs = [a.coldescrs[0], a.coldescrs[1] + b.coldescrs[0], b.coldescrs[1], ""]
        rowdescrs = [a.rowdescrs[0], a.rowdescrs[1] + b.rowdescrs[0], b.rowdescrs[1], ""]
        res = cls(3, 4, coldescrs, rowdescrs)
        res[0] = a[0][:2] + [0.0, a[0][2]]
        res[1] = [a[1][0], a[1][1]+b[0][0], b[0][1], a[1][2]+b[0][2]]
        res[2] = [0.0, b[1][0], b[1][1], b[1][2]]
        res.gaussStep(0)
        # res.gaussStep(1)
        return res

    def gauss(self):
        for rowId, _row in enumerate(self.m):
            self.gaussStep(rowId)

    def solv(self, globalsolution):
        self.gauss()
        for rowId, _i in reversed(list(enumerate(self.m))):
            # for x,y in zip(self[rowId][rowId+1:-1], self.coldescrs[rowId+1:-1]):
            #     print("x * u_{} = {} * {}".format(y.number, x, globalsolution[y.number]))
            globalsolution[self.rowdescrs[rowId].number] = self[rowId][-1] - sum(x*globalsolution[y.number]
                           for x,y in zip(self[rowId][rowId+1:-1], self.coldescrs[rowId+1:-1]))
            # print(" --> u_{} = {} = {} - ...".format(self.rowdescrs[rowId].number, globalsolution[self.rowdescrs[rowId].number], self[rowId][-1]))



if __name__ == "__main__":
    a1 = Matrix(2, 3, [Un(0),    Un(1, 1)], [Un(0),    Un(1, 1), ""], [  1,  0,  0,  1, -1, 1./32 ])
    print("a1\n" + str(a1))
    a2 = Matrix(2, 3, [Un(1, 2), Un(2, 1)], [Un(1, 2), Un(2, 1), ""], [ -1,  1,  1./32,  1, -1, 1./32 ])
    print("a2\n" + str(a2))
    
    a3 = Matrix(2, 3, [Un(2, 2), Un(3, 1)], [Un(2, 2), Un(3, 1), ""], [ -1,  1,  1./32,  1, -1, 1./32 ])
    print("a3\n" + str(a3))
    a4 = Matrix(2, 3, [Un(3, 2), Un(4)], [Un(3, 2), Un(4), ""],       [ -1,  1,  1./32,  0,  1, 1 ])
    print("a4\n" + str(a4))

    b1 = Matrix.prodA1(a1,a2)
    print("b1\n" + str(b1))
    b2 = Matrix.prodA1(a3,a4)
    print("b2\n" + str(b2))

    globalsolution = [None, None, None, None, None]
    c1 = Matrix.prodA2(b1.cutpart([1,2], [1,2,3]), b2.cutpart([1,2], [1,2,3]))
    print("c1\n" + str(c1))
    c1.solv(globalsolution)
    

    b1[2] = [0, 0, 1, globalsolution[2]]
    b1.coldescrs[2] = Un(2)
    b1.rowdescrs[2] = Un(2)
    b1.solv(globalsolution)

    b2[1] = [0, 1, 0, globalsolution[2]]
    b2.coldescrs[1] = Un(2)
    b2.rowdescrs[1] = Un(2)
    b2.solv(globalsolution)
    
    print(globalsolution)
    # 0, 0.97, 0.22, 0.375, 0.555, 0.763, 1
    with open('plot.dat', 'w') as fh:
        for i, v in enumerate(globalsolution):
            fh.write("{}    {}\n".format(1./4*i, v))