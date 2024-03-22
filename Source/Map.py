from PIL import Image, ImageDraw
from util import *

class Map:
    def __init__ (self, filename):
        Lines = []
        with open (filename, 'r', encoding = 'utf-8') as file:
            Lines = file.readlines()
            
        #? Input file should be at least 3 lines for the size of map, map matrix and obstacles
        if (len(Lines) < 3):
            raise Exception("Check your file again")
        
        #! Read the size of map
        if (len(list(Lines[0].split())) != 2):
            raise Exception("The first line should only include two arguments")
        self.numRows, self.numCols = Lines[0].split()
        self.numRows = int(self.numRows)
        self.numCols = int(self.numCols)
        if (self.numRows <= 0):
            raise ValueError("The number of rows in your matrix should be positive")
        if (self.numCols <= 0):
            raise ValueError("The number of columns in your matrix should be positive")
        
        #! Read Adjacency Matrix
        self.matrix = []
        self.seekerPosition: tuple[int, int] = None
        self.listHiderPositions: list[tuple[int, int]] = []
        if (len(Lines) - 1 < self.numRows):
            raise Exception("Your input matrix does not have enough rows")
        for i in range (0, self.numRows):
            temp = Lines[i + 1].split()
            if (len(temp) != self.numCols):
                raise Exception(f"Check the column {i + 1} in your matrix")
            
            listValues = []
            for j in range (0, len(temp)):
                if (int(temp[j]) < 0 or int(temp[j]) > 3):
                    raise ValueError(f"The value at position ({i + 1},{j + 1}) must be an integer from 0 to 3")
                
                if (int(temp[j]) == HIDER):
                    self.listHiderPositions.append((i, j))
                if (int(temp[j]) == SEEKER):
                    self.seekerPosition = (i, j)
                
                listValues.append(int(temp[j]))
            
            self.matrix.append(listValues)
        
        #! Read obstacles
        self.obstacles = []
        for i in range (self.numRows + 1, len(Lines)):
            if (len(list(Lines[i].split())) != 4):
                raise Exception(f"The line {i - self.numRows} of obstacles should only include 4 arguments")
            
            listPoints = Lines[i].split()
            for j in range (0,4):
                if (j % 2 == 0 and (int(listPoints[j]) <= 0 or int(listPoints[j]) > self.numRows)):
                    raise IndexError(f"Check obstacle {i - self.numRows}")
                elif (j % 2 == 1 and (int(listPoints[j]) <= 0 or int(listPoints[j]) > self.numCols)):
                    raise IndexError(f"Check obstacle {i - self.numRows}")
            if (int(listPoints[2]) < int(listPoints[0])):
                raise Exception(f"Check the bottom and the top of obstacle {i - self.numRows}")
            if (int(listPoints[3]) < int(listPoints[1])):
                raise Exception(f"Check the right and the left of obstacle {i - self.numRows}")
            
            for row in range (int(listPoints[0]), int(listPoints[2]) + 1):
                for col in range (int(listPoints[1]), int(listPoints[3]) + 1):
                    #? If the cell is not empty, the obstacle is invalid
                    if (self.matrix[row - 1][col - 1] != 0):
                        raise Exception (f"Obstacle {i - self.numRows} should be put at empty cells")
                    
                    self.matrix[row - 1][col - 1] = WALL
                    
            self.obstacles.append((int(listPoints[0]), int(listPoints[1]), int(listPoints[2]), int(listPoints[3])))
            
    def output_image (self, filename):
        cell_size = 50

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.numCols * cell_size, self.numRows * cell_size),
            "black"
        )
        draw = ImageDraw.Draw(img)

        for i in range (0, self.numRows):
            for j in range (0, self.numCols):
                #! Empty cell
                if (self.matrix[i][j] == 0):
                    fill = (255, 255, 255)
                    
                #! Walls
                if (self.matrix[i][j] == 1):
                    check = False
                    
                    #? Check whether self.matrix[i][j] is a position of any obstacle or not
                    for k in range (0, len(self.obstacles)):
                        if (i + 1 >= self.obstacles[k][0] and i + 1 <= self.obstacles[k][2] and
                            j + 1 >= self.obstacles[k][1] and j + 1 <= self.obstacles[k][3]):
                            check = True
                            fill = (255, 224, 189)
                            break
                    
                    if not check:
                        fill = (128, 128, 128)
                        
                #! Hiders
                if (self.matrix[i][j] == 2):
                    fill = (255, 0, 0)
                    
                #! Seeker
                if (self.matrix[i][j] == 3):
                    fill = (0, 171, 28)

                #! Draw cell
                draw.rectangle(
                    ([(j * cell_size, i * cell_size),
                      ((j + 1) * cell_size, (i + 1) * cell_size)]),
                    fill = fill
                )
                
        img.save(filename)