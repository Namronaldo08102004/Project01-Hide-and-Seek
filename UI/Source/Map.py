from Source.util import *

class Map:
    def __init__ (self, matrix: list[list[int]]):
        #! Read the size of map
        self.numRows, self.numCols = len(matrix), len(matrix[0])
        
        #! Read Adjacency Matrix
        self.matrix = matrix
        self.seekerPosition: tuple[int, int] = None
        self.listHiderPositions: list[tuple[int, int]] = []
        for row in range (0, self.numRows):
            for col in range (0, self.numCols):
                if (self.matrix[row][col] == HIDER):
                    self.listHiderPositions.append((row, col))
                elif (self.matrix[row][col] == SEEKER):
                    self.seekerPosition = (row, col)
        
        # #! Read obstacles
        # self.obstacles = []
        # for i in range (self.numRows + 1, len(Lines)):
        #     if (len(list(Lines[i].split())) != 4):
        #         raise Exception(f"The line {i - self.numRows} of obstacles should only include 4 arguments")
            
        #     listPoints = Lines[i].split()
        #     for j in range (0,4):
        #         if (j % 2 == 0 and (int(listPoints[j]) <= 0 or int(listPoints[j]) > self.numRows)):
        #             raise IndexError(f"Check obstacle {i - self.numRows}")
        #         elif (j % 2 == 1 and (int(listPoints[j]) <= 0 or int(listPoints[j]) > self.numCols)):
        #             raise IndexError(f"Check obstacle {i - self.numRows}")
        #     if (int(listPoints[2]) < int(listPoints[0])):
        #         raise Exception(f"Check the bottom and the top of obstacle {i - self.numRows}")
        #     if (int(listPoints[3]) < int(listPoints[1])):
        #         raise Exception(f"Check the right and the left of obstacle {i - self.numRows}")
            
        #     for row in range (int(listPoints[0]), int(listPoints[2]) + 1):
        #         for col in range (int(listPoints[1]), int(listPoints[3]) + 1):
        #             #? If the cell is not empty, the obstacle is invalid
        #             if (self.matrix[row - 1][col - 1] != 0):
        #                 raise Exception (f"Obstacle {i - self.numRows} should be put at empty cells")
                    
        #             self.matrix[row - 1][col - 1] = WALL
                    
        #     self.obstacles.append((int(listPoints[0]), int(listPoints[1]), int(listPoints[2]), int(listPoints[3])))