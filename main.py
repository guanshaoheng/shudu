import numpy as np
import time


class Shudu:
    '''
    Used to solve the Soduku
    '''
    def __init__(self):
        self.pool = [[list(range(1, 10)) for i in range(9)] for j in range(1, 10)]
        self.nums = np.loadtxt('./problem4.txt', dtype=int)
        self.columnLack = [list(range(1, 10)) for _ in range(9)]
        self.rowLack = [list(range(1, 10)) for _ in range(9)]
        self.blockLack = [list(range(1, 10)) for _ in range(9)]
        for i in range(9):
            for j in range(9):
                if self.nums[i, j] != 0:
                    self.setNumberInit(coors=[[i, j]], values=[self.nums[i, j]])
        print(self.nums)

    def setNumberInit(self, coors: list, values: list):
        if len(coors) != len(values):
            raise ValueError('Length of the coors (%d) does not equal the values (%d)' % (len(coors), len(values)))
        for i in range(len(coors)):
            row, column = coors[i][0], coors[i][1]
            self.setValue(row=row, column=column, value=values[i])

    def forward(self):
        for i in range(9):
            for j in range(9):
                if i ==2 and j ==0:
                    print()
                if self.nums[i, j] != 0:
                    self.deleteGlobal(value=self.nums[i, j], row=i, column=j)  # in all the related elements

    def check(self):
        """
        if some value only happen once in a row or a column, then the numbe is that value
        :return:
        """
        # row check
        for i in range(9):      # row
            if len(self.rowLack[i]) == 0:
                continue
            for value in self.rowLack[i]:  # value
                count = 0
                for j in range(9): # column
                    if value in self.pool[i][j]:
                        count += 1
                        indexColumn = j
                        if count > 1:
                            break
                if count == 1:
                    self.setValue(row=i, column=indexColumn, value=value)
                    del indexColumn

        # column check
        for j in range(9):
            if len(self.columnLack[j]) == 0:
                continue
            tempColumn = [self.pool[k][j] for k in range(9)]
            for value in self.columnLack[j]: # value
                count = 0
                for i in range(9):  # column
                    if value in tempColumn[i]:
                        count += 1
                        indexRow = i
                        if count > 1:
                            break
                if count == 1:
                    self.setValue(row=indexRow, column=j, value=value)
                    del indexRow

        # block check
        for num in range(9):
            if len(self.blockLack[num]) == 0:
                continue
            rowList = range(num % 3 * 3, num % 3 * 3 + 3)
            columnList = range(num // 3 * 3, num // 3 * 3 + 3)
            tempBlock = [[self.pool[k][l] for l in columnList] for k in rowList]
            for value in self.blockLack[num]:
                count = 0
                for rowIndex in rowList:
                    for columnIndex in columnList:
                        if value in self.pool[rowIndex][columnIndex]:
                            count += 1
                            rowIndexTemp, columnIndexTemp = rowIndex, columnIndex
                            if count > 1:
                                break
                if count == 1:
                    self.setValue(row=rowIndexTemp, column=columnIndexTemp, value=value)
                    del rowIndexTemp, columnIndexTemp
        self.countSolved()
        return

    def setValue(self, row, column, value):
        self.pool[row][column] = [value]
        self.nums[row, column] = value
        try:
            self.columnLack[column].remove(value)
        except:
            pass
        try:
            self.rowLack[row].remove(value)
        except:
            pass
        try:
            blockNum = row//3+column//3*3
            self.blockLack[blockNum].remove(value)
        except:
            pass

    def deleteGlobal(self, value, row, column):
        for i in range(9):
            self.deleteSingle(row, i, value)
            self.deleteSingle(i, column, value)
        blockNum = row//3+column//3*3
        rowList = range(blockNum%3*3, blockNum%3*3+3)
        columnList = range(blockNum//3*3, blockNum//3*3+3)
        for i in rowList:
            for j in columnList:
                if row!=i and column!=j:
                    self.deleteSingle(i, j, value)
        return

    def deleteSingle(self, row, column, value):
        if len(self.pool[row][column]) == 1:
            if self.nums[row, column] == 0:
                self.nums[row, column] = self.pool[row][column][0]
            elif self.nums[row, column] != self.pool[row][column][0]:
                raise ValueError('nums[%d, %d]=%d, while pool[%d][%d]=%d' % (row, column, self.nums[row, column],
                                                                             row, column, self.pool[row][column][0]))
            return
        try:
            self.pool[row][column].remove(value)
        except:
            pass
        return

    def countSolved(self):
        count = 0
        for i in range(9):
            for j in range(9):
                if self.nums[i, j]!=0:
                    count += 1
        print('Solved elements number is: %d  left: %d' % (count, 81-count))

    def calSoduku(self, pos):
        if pos == 81:
            print('pos=%d' % (pos))
            print(self.nums)
            self.saveTxt()
            return
        row, column = pos//9, pos % 9
        if self.nums[row, column] == 0:
            for i in self.pool[row][column]:
                if self.checkIfValid(row, column, i):
                    self.nums[row, column] = i
                    self.calSoduku(pos+1)
            self.nums[row, column] = 0
        else:
            self.calSoduku(pos+1)

    def checkIfValid(self, row, column, i):
        if self.checkRow(row, i) and self.checkColumn(column, i) and self.checkBlock(row, column, i):
            return True
        else:
            return False

    def checkRow(self, row, i):
        if i in self.nums[row, :]:
            return False
        else:
            return True

    def checkColumn(self, column, i):
        if i in self.nums[:, column]:
            return False
        else:
            return True

    def checkBlock(self, row, columb, i):
        blockNum = row // 3 + columb // 3 * 3
        rowList = [blockNum % 3 * 3, blockNum % 3 * 3 + 3]
        columnList = [blockNum // 3 * 3, blockNum // 3 * 3 + 3]
        if i in self.nums[rowList[0]:rowList[1], columnList[0]:columnList[1]]:
            return False
        else:
            return True

    def former(self, row, column):
        if column == 0 and row == 0:
            raise ValueError('row = %d and column = %d' % (row, column))
        if column == 0:
            column = 8
            row = row-1
        else:
            column = column-1
        return row, column

    def saveTxt(self):
        np.savetxt(fname='results.txt', X=self.nums, fmt='%d')


if __name__=="__main__":
    time1 = time.time()
    shudu = Shudu()
    # pre-process to decrease the computation numbers needed
    for i in range(10):
        shudu.forward()
        shudu.check()
    shudu.calSoduku(pos=0)
    print('Consumed time: %es' % (time.time() - time1))