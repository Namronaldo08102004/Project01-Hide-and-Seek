from AI.util import *

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