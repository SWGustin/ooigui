from random import randint
class matr:
    def __init__(self, m:tuple, max_:int, min_:int):
        x,y = m
        self.matrix = [[randint(min_,max_) for x0 in range(x)]\
                           for y0 in range(y)]

    def __str__(self):
        return '\n'.join([str(x) for x in self.matrix])


class BinMatr(matr):
    def __init__(self, m:tuple):
        super().__init__(m, 1, 0)


class Finder:
    def __init__(self, matrix):
        self.matrix = matrix.matrix
        self.countr = 0
        self.visitedMatrix = [[False for _ in self.matrix[0]]\
                               for row in self.matrix]
    
    def findNeighbors(self, loc:tuple)->list:
        x,y = loc
        neighbors = []
        for i in (-1,0,1):
            for j in (-1,0,1):
                if i == 0 and j == 0:
                    continue
                if x+j < 0 or y+i<0 \
                   or x+j>len(self.matrix[0]) \
                   or y+i>len(self.matrix):
                    continue
                try:
                    neighbors.append((self.matrix[y+i][x+j], x+j, y+i))
                except(IndexError):
                    pass
        return neighbors

class BinBlockFinder(Finder):
    def __init__(self,matrix:list[list[object]]):
        super().__init__(matrix)


    def countBlocks(self):        
        for idy,row in enumerate(self.matrix:list[list[int]]):
            for idx,col in enumerate(row):
                if col and not self.visitedMatrix[idy][idx]:
                    self.countr+=1
                    self.findBlock((idx,idy))
                else:
                    self.visitedMatrix[idy][idx]=True
        return self.countr

    def findBlock(self,loc:tuple):
        x,y = loc
        self.visitedMatrix[y][x] = True
        for neighbor in self.findNeighbors((x,y)):
            val,x,y = neighbor
            if self.visitedMatrix[y][x]:
                continue
            self.visitedMatrix[y][x] = True
            if val:
                self.findBlock((x,y))
                        

def BoggleFinder(Finder):
    def __init__(self, matrix:list[list[str]], dict_:dict):
        self.dict_ = dict_
        super().__init__(self,matrix)

if __name__ == '__main__':
    test = BinMatr((5,4))
    print(test)

    testFinder = BinBlockFinder(test)
    print(testFinder.countBlocks())

    dictn = ['111','101']
    BoggleFinder(test, dictn)
    
    
