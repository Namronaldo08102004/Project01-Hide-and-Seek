from AI.Map import *
from random import choice
from AI.A_Star import *
    
class Level:
    """
    This class is used to store common methods and attributes used in all levels in the game
    In our program, we mention many times about wall intersections, so below is the definition of wall intersections:
         ------ ------
        |      |      |
        |      |      |
         ------ ------
        |      | <----
        |      | 
         ------
    """
    def __init__ (self, map: Map):
        self.map: Map = map
        self.score: int = 0
        self.numSeekerSteps: int = 0 #? Increase this attribute by 1 if seeker took its turn and the game is not over
        self.numHiderSteps: int = 0 #? Increase this attribute by 1 if hider took its turn and the game is not over
        self.takeTurn: int = SEEKER
        
    def broadcastAnnouncement (self, hiderPosition: tuple[int, int]) -> tuple[int, int]:
        """
        This function is used to broadcast the announcement from a certain position of hider
        Announcement will be broadcasted at a random position in the radius 3 around the hider position, including walls or obstacles
        """
        listPositions = []
        
        for level in range (1, 3):
            for row in range (hiderPosition[0] - level, hiderPosition[0] + level + 1):
                if (row >= 0 and row < self.map.numRows):
                    for col in range (hiderPosition[1] - level, hiderPosition[1] + level + 1):
                        if (col >= 0 and col < self.map.numCols and (row, col) != hiderPosition):
                            listPositions.append((row, col))
        
        randomPosition = choice(listPositions)
        return randomPosition
    
    def getObservableCells (self, seekerPosition: tuple[int, int]):
        """
        Get the observable cells of the seeker.
        The flow of this function is similar to the getObservableCellsOfHider function in the Hider class
        """
        
        radius_3_matrix: list[list[bool]] = []
        seeker_position_in_matrix: tuple[int, int] = None
        for row in range (seekerPosition[0] - 3, seekerPosition[0] + 4):
            if (row >= 0 and row < self.map.numRows):
                tempList: list[int] = []
            
                for col in range (seekerPosition[1] - 3, seekerPosition[1] + 4):
                    if (col >= 0 and col < self.map.numCols):
                        if (self.map.matrix[row][col] in [WALL, OBSTACLE]):
                            tempList.append(False)
                        else:
                            tempList.append(True)
                            
                        if ((row, col) == seekerPosition):
                            seeker_position_in_matrix = (len(radius_3_matrix), len(tempList) - 1)
                    
                radius_3_matrix.append(tempList)
                
        X = seeker_position_in_matrix[0]
        Y = seeker_position_in_matrix[1]
        numRows = len(radius_3_matrix)
        numCols = len(radius_3_matrix[0])
                
        #? Case 1
        if (X - 1 >= 0 and Y - 1 >= 0 and radius_3_matrix[X - 1][Y - 1] == False):
            if (X - 3 >= 0 and Y - 3 >= 0):    
                radius_3_matrix[X - 3][Y - 3] = False
            if (X - 3 >= 0 and Y - 2 >= 0):    
                radius_3_matrix[X - 3][Y - 2] = False
            if (X - 2 >= 0 and Y - 3 >= 0):    
                radius_3_matrix[X - 2][Y - 3] = False
            if (X - 2 >= 0 and Y - 2 >= 0):    
                radius_3_matrix[X - 2][Y - 2] = False
                
            if (X - 1 >= 0 and radius_3_matrix[X - 1][Y] == False):
                if (X - 3 >= 0 and Y - 1 >= 0):
                    radius_3_matrix[X - 3][Y - 1] = False
                if (X - 3 >= 0):
                    radius_3_matrix[X - 3][Y] = False
                if (X - 3 >= 0 and Y + 1 < numCols):
                    radius_3_matrix[X - 3][Y + 1] = False
                if (X - 2 >= 0):
                    radius_3_matrix[X - 2][Y] = False
                if (X - 2 >= 0 and Y - 1 >= 0):
                    radius_3_matrix[X - 2][Y - 1] = False
                if (X - 3 >= 0 and Y - 2 >= 0):
                    radius_3_matrix[X - 3][Y - 2] = False
                if (X - 3 >= 0 and Y - 1 >= 0):
                    radius_3_matrix[X - 3][Y - 1] = False
            
            if (Y - 1 >= 0 and radius_3_matrix[X][Y - 1] == False):
                if (Y - 3 >= 0):
                    radius_3_matrix[X][Y - 3] = False
                if (Y - 2 >= 0):
                    radius_3_matrix[X][Y - 2] = False
                if (X - 1 >= 0 and Y - 3 >= 0):
                    radius_3_matrix[X - 1][Y - 3] = False
                if (X + 1 < numRows and Y - 3 >= 0):
                    radius_3_matrix[X + 1][Y - 3] = False
                if (X - 1 >= 0 and Y - 2 >= 0):
                    radius_3_matrix[X - 1][Y - 2] = False
                if (X - 1 >= 0 and Y - 3 >= 0):
                    radius_3_matrix[X - 1][Y - 3] = False
                if (X - 2 >= 0 and Y - 3 >= 0):
                    radius_3_matrix[X - 2][Y - 3] = False
        
        #? Case 2
        if (X - 1 >= 0 and radius_3_matrix[X - 1][Y] == False):
            if (X - 3 >= 0 and Y - 1 >= 0):
                radius_3_matrix[X - 3][Y - 1] = False
            if (X - 3 >= 0):
                radius_3_matrix[X - 3][Y] = False
            if (X - 3 >= 0 and Y + 1 < numCols):
                radius_3_matrix[X - 3][Y + 1] = False
            if (X - 2 >= 0):
                radius_3_matrix[X - 2][Y] = False
                
            if (X - 1 >= 0 and Y - 1 >= 0 and radius_3_matrix[X - 1][Y - 1] == False):
                if (X - 3 >= 0 and Y - 3 >= 0):    
                    radius_3_matrix[X - 3][Y - 3] = False
                if (X - 3 >= 0 and Y - 2 >= 0):    
                    radius_3_matrix[X - 3][Y - 2] = False
                if (X - 2 >= 0 and Y - 3 >= 0):    
                    radius_3_matrix[X - 2][Y - 3] = False
                if (X - 2 >= 0 and Y - 2 >= 0):    
                    radius_3_matrix[X - 2][Y - 2] = False
                if (X - 2 >= 0 and Y - 1 >= 0):
                    radius_3_matrix[X - 2][Y - 1] = False
                if (X - 3 >= 0 and Y - 2 >= 0):
                    radius_3_matrix[X - 3][Y - 2] = False
                if (X - 3 >= 0 and Y - 1 >= 0):
                    radius_3_matrix[X - 3][Y - 1] = False
                    
            if (X - 1 >= 0 and Y + 1 < numCols and radius_3_matrix[X - 1][Y + 1] == False):
                if (X - 3 >= 0 and Y + 2 < numCols):
                    radius_3_matrix[X - 3][Y + 2] = False
                if (X - 3 >= 0 and Y + 3 < numCols):
                    radius_3_matrix[X - 3][Y + 3] = False
                if (X - 2 >= 0 and Y + 2 < numCols):
                    radius_3_matrix[X - 2][Y + 2] = False
                if (X - 2 >= 0 and Y + 3 < numCols):
                    radius_3_matrix[X - 2][Y + 3] = False
                if (X - 2 >= 0 and Y + 1 < numCols):
                    radius_3_matrix[X - 2][Y + 1] = False
                if (X - 3 >= 0 and Y + 1 < numCols):
                    radius_3_matrix[X - 3][Y + 1] = False
                if (X - 3 >= 0 and Y + 2 < numCols):
                    radius_3_matrix[X - 3][Y + 2] = False
            
        #? Case 3
        if (X - 1 >= 0 and Y + 1 < numCols and radius_3_matrix[X - 1][Y + 1] == False):
            if (X - 3 >= 0 and Y + 2 < numCols):
                radius_3_matrix[X - 3][Y + 2] = False
            if (X - 3 >= 0 and Y + 3 < numCols):
                radius_3_matrix[X - 3][Y + 3] = False
            if (X - 2 >= 0 and Y + 2 < numCols):
                radius_3_matrix[X - 2][Y + 2] = False
            if (X - 2 >= 0 and Y + 3 < numCols):
                radius_3_matrix[X - 2][Y + 3] = False
                
            if (X - 1 >= 0 and radius_3_matrix[X - 1][Y] == False):
                if (X - 3 >= 0 and Y - 1 >= 0):
                    radius_3_matrix[X - 3][Y - 1] = False
                if (X - 3 >= 0):
                    radius_3_matrix[X - 3][Y] = False
                if (X - 3 >= 0 and Y + 1 < numCols):
                    radius_3_matrix[X - 3][Y + 1] = False
                if (X - 2 >= 0):
                    radius_3_matrix[X - 2][Y] = False
                if (X - 2 >= 0 and Y + 1 < numCols):
                    radius_3_matrix[X - 2][Y + 1] = False
                if (X - 3 >= 0 and Y + 1 < numCols):
                    radius_3_matrix[X - 3][Y + 1] = False
                if (X - 3 >= 0 and Y + 2 < numCols):
                    radius_3_matrix[X - 3][Y + 2] = False
                    
            if (Y + 1 < numCols and radius_3_matrix[X][Y + 1] == False):
                if (Y + 2 < numCols):
                    radius_3_matrix[X][Y + 2] = False
                if (Y + 3 < numCols):
                    radius_3_matrix[X][Y + 3] = False
                if (X - 1 >= 0 and Y + 3 < numCols):
                    radius_3_matrix[X - 1][Y + 3] = False
                if (X + 1 < numRows and Y + 3 < numCols):
                    radius_3_matrix[X + 1][Y + 3] = False
                if (X - 1 >= 0 and Y + 2 < numCols):
                    radius_3_matrix[X - 1][Y + 2] = False
                if (X - 2 >= 0 and Y + 3 < numCols):
                    radius_3_matrix[X - 2][Y + 3] = False
                if (X - 1 >= 0 and Y + 3 < numCols):
                    radius_3_matrix[X - 1][Y + 3] = False
        
        #? Case 4      
        if (Y + 1 < numCols and radius_3_matrix[X][Y + 1] == False):
            if (Y + 2 < numCols):
                radius_3_matrix[X][Y + 2] = False
            if (Y + 3 < numCols):
                radius_3_matrix[X][Y + 3] = False
            if (X - 1 >= 0 and Y + 3 < numCols):
                radius_3_matrix[X - 1][Y + 3] = False
            if (X + 1 < numRows and Y + 3 < numCols):
                radius_3_matrix[X + 1][Y + 3] = False
                
            if (X - 1 >= 0 and Y + 1 < numCols and radius_3_matrix[X - 1][Y + 1] == False):
                if (X - 3 >= 0 and Y + 2 < numCols):
                    radius_3_matrix[X - 3][Y + 2] = False
                if (X - 3 >= 0 and Y + 3 < numCols):
                    radius_3_matrix[X - 3][Y + 3] = False
                if (X - 2 >= 0 and Y + 2 < numCols):
                    radius_3_matrix[X - 2][Y + 2] = False
                if (X - 2 >= 0 and Y + 3 < numCols):
                    radius_3_matrix[X - 2][Y + 3] = False
                if (X - 1 >= 0 and Y + 2 < numCols):
                    radius_3_matrix[X - 1][Y + 2] = False
                if (X - 2 >= 0 and Y + 3 < numCols):
                    radius_3_matrix[X - 2][Y + 3] = False
                if (X - 1 >= 0 and Y + 3 < numCols):
                    radius_3_matrix[X - 1][Y + 3] = False
                    
            if (X + 1 < numRows and Y + 1 < numCols and radius_3_matrix[X + 1][Y + 1] == False):
                if (X + 2 < numRows and Y + 2 < numCols):
                    radius_3_matrix[X + 2][Y + 2] = False
                if (X + 2 < numRows and Y + 3 < numCols):
                    radius_3_matrix[X + 2][Y + 3] = False
                if (X + 3 < numRows and Y + 2 < numCols):
                    radius_3_matrix[X + 3][Y + 2] = False
                if (X + 3 < numRows and Y + 3 < numCols):
                    radius_3_matrix[X + 3][Y + 3] = False
                if (X + 1 < numRows and Y + 2 < numCols):
                    radius_3_matrix[X + 1][Y + 2] = False
                if (X + 1 < numRows and Y + 3 < numCols):
                    radius_3_matrix[X + 1][Y + 3] = False
                if (X + 2 < numRows and Y + 3 < numCols):
                    radius_3_matrix[X + 2][Y + 3] = False
        
        #? Case 5 
        if (X + 1 < numRows and Y + 1 < numCols and radius_3_matrix[X + 1][Y + 1] == False):
            if (X + 2 < numRows and Y + 2 < numCols):
                radius_3_matrix[X + 2][Y + 2] = False
            if (X + 2 < numRows and Y + 3 < numCols):
                radius_3_matrix[X + 2][Y + 3] = False
            if (X + 3 < numRows and Y + 2 < numCols):
                radius_3_matrix[X + 3][Y + 2] = False
            if (X + 3 < numRows and Y + 3 < numCols):
                radius_3_matrix[X + 3][Y + 3] = False
            
            if (Y + 1 < numCols and radius_3_matrix[X][Y + 1] == False):
                if (Y + 2 < numCols):
                    radius_3_matrix[X][Y + 2] = False
                if (Y + 3 < numCols):
                    radius_3_matrix[X][Y + 3] = False
                if (X - 1 >= 0 and Y + 3 < numCols):
                    radius_3_matrix[X - 1][Y + 3] = False
                if (X + 1 < numRows and Y + 3 < numCols):
                    radius_3_matrix[X + 1][Y + 3] = False
                if (X + 1 < numRows and Y + 2 < numCols):
                    radius_3_matrix[X + 1][Y + 2] = False
                if (X + 1 < numRows and Y + 3 < numCols):
                    radius_3_matrix[X + 1][Y + 3] = False
                if (X + 2 < numRows and Y + 3 < numCols):
                    radius_3_matrix[X + 2][Y + 3] = False
                
            if (X + 1 < numRows and radius_3_matrix[X + 1][Y] == False):
                if (X + 2 < numRows):
                    radius_3_matrix[X + 2][Y] = False
                if (X + 3 < numRows):
                    radius_3_matrix[X + 3][Y] = False
                if (X + 3 < numRows and Y - 1 >= 0):
                    radius_3_matrix[X + 3][Y - 1] = False
                if (X + 3 < numRows and Y + 1 < numCols):
                    radius_3_matrix[X + 3][Y + 1] = False
                if (X + 2 < numRows and Y + 1 < numCols):
                    radius_3_matrix[X + 2][Y + 1] = False
                if (X + 3 < numRows and Y + 1 < numCols):
                    radius_3_matrix[X + 3][Y + 1] = False
                if (X + 3 < numRows and Y + 2 < numCols):
                    radius_3_matrix[X + 3][Y + 2] = False    
        
        #? Case 6
        if (X + 1 < numRows and radius_3_matrix[X + 1][Y] == False):
            if (X + 2 < numRows):
                radius_3_matrix[X + 2][Y] = False
            if (X + 3 < numRows):
                radius_3_matrix[X + 3][Y] = False
            if (X + 3 < numRows and Y - 1 >= 0):
                radius_3_matrix[X + 3][Y - 1] = False
            if (X + 3 < numRows and Y + 1 < numCols):
                radius_3_matrix[X + 3][Y + 1] = False
                
            if (X + 1 < numRows and Y + 1 < numCols and radius_3_matrix[X + 1][Y + 1] == False):
                if (X + 2 < numRows and Y + 2 < numCols):
                    radius_3_matrix[X + 2][Y + 2] = False
                if (X + 2 < numRows and Y + 3 < numCols):
                    radius_3_matrix[X + 2][Y + 3] = False
                if (X + 3 < numRows and Y + 2 < numCols):
                    radius_3_matrix[X + 3][Y + 2] = False
                if (X + 3 < numRows and Y + 3 < numCols):
                    radius_3_matrix[X + 3][Y + 3] = False
                if (X + 2 < numRows and Y + 1 < numCols):
                    radius_3_matrix[X + 2][Y + 1] = False
                if (X + 3 < numRows and Y + 1 < numCols):
                    radius_3_matrix[X + 3][Y + 1] = False
                if (X + 3 < numRows and Y + 2 < numCols):
                    radius_3_matrix[X + 3][Y + 2] = False
            
            if (X + 1 < numRows and Y - 1 >= 0 and radius_3_matrix[X + 1][Y - 1] == False):
                if (X + 2 < numRows and Y - 3 >= 0):
                    radius_3_matrix[X + 2][Y - 3] = False
                if (X + 2 < numRows and Y - 2 >= 0):
                    radius_3_matrix[X + 2][Y - 2] = False
                if (X + 3 < numRows and Y - 3 >= 0):
                    radius_3_matrix[X + 3][Y - 3] = False
                if (X + 3 < numRows and Y - 2 >= 0):
                    radius_3_matrix[X + 3][Y - 2] = False
                if (X + 2 < numRows and Y - 1 >= 0):
                    radius_3_matrix[X + 2][Y - 1] = False
                if (X + 3 < numRows and Y - 1 >= 0):
                    radius_3_matrix[X + 3][Y - 1] = False
                if (X + 3 < numRows and Y - 2 >= 0):
                    radius_3_matrix[X + 3][Y - 2] = False
                
        #? Case 7
        if (X + 1 < numRows and Y - 1 >= 0 and radius_3_matrix[X + 1][Y - 1] == False):
            if (X + 2 < numRows and Y - 3 >= 0):
                radius_3_matrix[X + 2][Y - 3] = False
            if (X + 2 < numRows and Y - 2 >= 0):
                radius_3_matrix[X + 2][Y - 2] = False
            if (X + 3 < numRows and Y - 3 >= 0):
                radius_3_matrix[X + 3][Y - 3] = False
            if (X + 3 < numRows and Y - 2 >= 0):
                radius_3_matrix[X + 3][Y - 2] = False
                
            if (X + 1 < numRows and radius_3_matrix[X + 1][Y] == False):
                if (X + 2 < numRows):
                    radius_3_matrix[X + 2][Y] = False
                if (X + 3 < numRows):
                    radius_3_matrix[X + 3][Y] = False
                if (X + 3 < numRows and Y - 1 >= 0):
                    radius_3_matrix[X + 3][Y - 1] = False
                if (X + 3 < numRows and Y + 1 < numCols):
                    radius_3_matrix[X + 3][Y + 1] = False
                if (X + 2 < numRows and Y - 1 >= 0):
                    radius_3_matrix[X + 2][Y - 1] = False
                if (X + 3 < numRows and Y - 1 >= 0):
                    radius_3_matrix[X + 3][Y - 1] = False
                if (X + 3 < numRows and Y - 2 >= 0):
                    radius_3_matrix[X + 3][Y - 2] = False
                    
            if (Y - 1 >= 0 and radius_3_matrix[X][Y - 1] == False):
                if (Y - 3 >= 0):
                    radius_3_matrix[X][Y - 3] = False
                if (Y - 2 >= 0):
                    radius_3_matrix[X][Y - 2] = False
                if (X - 1 >= 0 and Y - 3 >= 0):
                    radius_3_matrix[X - 1][Y - 3] = False
                if (X + 1 < numRows and Y - 3 >= 0):
                    radius_3_matrix[X + 1][Y - 3] = False
                if (X + 1 < numRows and Y - 2 >= 0):
                    radius_3_matrix[X + 1][Y - 2] = False
                if (X + 1 < numRows and Y - 3 >= 0):
                    radius_3_matrix[X + 1][Y - 3] = False
                if (X + 2 < numRows and Y - 3 >= 0):
                    radius_3_matrix[X + 2][Y - 3] = False
                
        #? Case 8
        if (Y - 1 >= 0 and radius_3_matrix[X][Y - 1] == False):
            if (Y - 3 >= 0):
                radius_3_matrix[X][Y - 3] = False
            if (Y - 2 >= 0):
                radius_3_matrix[X][Y - 2] = False
            if (X - 1 >= 0 and Y - 3 >= 0):
                radius_3_matrix[X - 1][Y - 3] = False
            if (X + 1 < numRows and Y - 3 >= 0):
                radius_3_matrix[X + 1][Y - 3] = False
                
            if (X + 1 < numRows and Y - 1 >= 0 and radius_3_matrix[X + 1][Y - 1] == False):
                if (X + 2 < numRows and Y - 3 >= 0):
                    radius_3_matrix[X + 2][Y - 3] = False
                if (X + 2 < numRows and Y - 2 >= 0):
                    radius_3_matrix[X + 2][Y - 2] = False
                if (X + 3 < numRows and Y - 3 >= 0):
                    radius_3_matrix[X + 3][Y - 3] = False
                if (X + 3 < numRows and Y - 2 >= 0):
                    radius_3_matrix[X + 3][Y - 2] = False
                if (X + 1 < numRows and Y - 2 >= 0):
                    radius_3_matrix[X + 1][Y - 2] = False
                if (X + 1 < numRows and Y - 3 >= 0):
                    radius_3_matrix[X + 1][Y - 3] = False
                if (X + 2 < numRows and Y - 3 >= 0):
                    radius_3_matrix[X + 2][Y - 3] = False
                    
            if (X - 1 >= 0 and Y - 1 >= 0 and radius_3_matrix[X - 1][Y - 1] == False):
                if (X - 3 >= 0 and Y - 3 >= 0):    
                    radius_3_matrix[X - 3][Y - 3] = False
                if (X - 3 >= 0 and Y - 2 >= 0):    
                    radius_3_matrix[X - 3][Y - 2] = False
                if (X - 2 >= 0 and Y - 3 >= 0):    
                    radius_3_matrix[X - 2][Y - 3] = False
                if (X - 2 >= 0 and Y - 2 >= 0):    
                    radius_3_matrix[X - 2][Y - 2] = False
                if (X - 1 >= 0 and Y - 2 >= 0):
                    radius_3_matrix[X - 1][Y - 2] = False
                if (X - 1 >= 0 and Y - 3 >= 0):
                    radius_3_matrix[X - 1][Y - 3] = False
                if (X - 2 >= 0 and Y - 3 >= 0):
                    radius_3_matrix[X - 2][Y - 3] = False
            
        #! Check in the radius 2 around the current seeker position
        if (X - 2 >= 0 and Y - 2 >= 0 and radius_3_matrix[X - 2][Y - 2] == False):
            if (X - 3 >= 0 and Y - 3 >= 0):
                radius_3_matrix[X - 3][Y - 3] = False
        if (X - 2 >= 0 and Y - 1 >= 0 and radius_3_matrix[X - 2][Y - 1] == False):
            if (X - 3 >= 0 and Y - 2 >= 0):
                radius_3_matrix[X - 3][Y - 2] = False
            if (X - 3 >= 0 and Y - 1 >= 0):
                radius_3_matrix[X - 3][Y - 1] = False
        if (X - 2 >= 0 and radius_3_matrix[X - 2][Y] == False):
            if (X - 3 >= 0):
                radius_3_matrix[X - 3][Y] = False
        if (X - 2 >= 0 and Y + 1 < numCols and radius_3_matrix[X - 2][Y + 1] == False):
            if (X - 3 >= 0 and Y + 1 < numCols):
                radius_3_matrix[X - 3][Y + 1] = False
            if (X - 3 >= 0 and Y + 2 < numCols):
                radius_3_matrix[X - 3][Y + 2] = False
        if (X - 2 >= 0 and Y + 2 < numCols and radius_3_matrix[X - 2][Y + 2] == False):
            if (X - 3 >= 0 and Y + 3 < numCols):
                radius_3_matrix[X - 3][Y + 3] = False
        if (X - 1 >= 0 and Y + 2 < numCols and radius_3_matrix[X - 1][Y + 2] == False):
            if (X - 2 >= 0 and Y + 3 < numCols):
                radius_3_matrix[X - 2][Y + 3] = False
            if (X - 1 >= 0 and Y + 3 < numCols):
                radius_3_matrix[X - 1][Y + 3] = False
        if (Y + 2 < numCols and radius_3_matrix[X][Y + 2] == False):
            if (Y + 3 < numCols):
                radius_3_matrix[X][Y + 3] = False
        if (X + 1 < numRows and Y + 2 < numCols and radius_3_matrix[X + 1][Y + 2] == False):
            if (X + 1 < numRows and Y + 3 < numCols):
                radius_3_matrix[X + 1][Y + 3] = False
            if (X + 2 < numRows and Y + 3 < numCols):
                radius_3_matrix[X + 2][Y + 3] = False
        if (X + 2 < numRows and Y + 2 < numCols and radius_3_matrix[X + 2][Y + 2] == False):
            if (X + 3 < numRows and Y + 3 < numCols):
                radius_3_matrix[X + 3][Y + 3] = False
        if (X + 2 < numRows and Y + 1 < numCols and radius_3_matrix[X + 2][Y + 1] == False):
            if (X + 3 < numRows and Y + 1 < numCols):
                radius_3_matrix[X + 3][Y + 1] = False
            if (X + 3 < numRows and Y + 2 < numCols):
                radius_3_matrix[X + 3][Y + 2] = False
        if (X + 2 < numRows and radius_3_matrix[X + 2][Y] == False):
            if (X + 3 < numRows):
                radius_3_matrix[X + 3][Y] = False
        if (X + 2 < numRows and Y - 1 >= 0 and radius_3_matrix[X + 2][Y - 1] == False):
            if (X + 3 < numRows and Y - 1 >= 0):
                radius_3_matrix[X + 3][Y - 1] = False
            if (X + 3 < numRows and Y - 2 >= 0):
                radius_3_matrix[X + 3][Y - 2] = False
        if (X + 2 < numRows and Y - 2 >= 0 and radius_3_matrix[X + 2][Y - 2] == False):
            if (X + 3 < numRows and Y - 3 >= 0):
                radius_3_matrix[X + 3][Y - 3] = False
        if (X + 1 < numRows and Y - 2 >= 0 and radius_3_matrix[X + 1][Y - 2] == False):
            if (X + 1 < numRows and Y - 3 >= 0):
                radius_3_matrix[X + 1][Y - 3] = False
            if (X + 2 < numRows and Y - 3 >= 0):
                radius_3_matrix[X + 2][Y - 3] = False
        if (Y - 2 >= 0 and radius_3_matrix[X][Y - 2] == False):
            if (Y - 3 >= 0):
                radius_3_matrix[X][Y - 3] = False
        if (X - 1 >= 0 and Y - 2 >= 0 and radius_3_matrix[X - 1][Y - 2] == False):
            if (X - 1 >= 0 and Y - 3 >= 0):
                radius_3_matrix[X - 1][Y - 3] = False
            if (X - 2 >= 0 and Y - 3 >= 0):
                radius_3_matrix[X - 2][Y - 3] = False
        
        listObservablePositions = []
        index_row = 0
        for row in range (seekerPosition[0] - 3, seekerPosition[0] + 4):
            if (row >= 0 and row < self.map.numRows):
                index_col = 0
                
                for col in range (seekerPosition[1] - 3, seekerPosition[1] + 4):
                    if (col >= 0 and col < self.map.numCols):
                        if (radius_3_matrix[index_row][index_col] and (row, col) != seekerPosition):
                            listObservablePositions.append((row, col))
                        index_col = index_col + 1
                        
                index_row = index_row + 1
                    
        return listObservablePositions
    
    def getShortestPath (self, startPosition: tuple[int, int], goalPosition: tuple[int, int], visitedMatrix = None) -> list[tuple[int, int]]:
        """
        This function returns the shortest path from the start position to the goal position
        """
        
        goal = A_Star(startPosition, goalPosition, self.map.matrix, visitedMatrix)
        shortestPath = []
        
        if (goal is not None):
            while (goal is not None):
                shortestPath.append(goal.state)
                goal = goal.parent
        
            shortestPath = shortestPath[:-1]
            shortestPath = shortestPath[::-1]
            
            return shortestPath
        
        return None
    
    def countNumWallsBetweenTwoPositions (self, position1: tuple[int, int], position2: tuple[int, int]):
        """
        This function returns the number of walls in the shortest path (without any walls in the map) 
        from the first position to the second position.
        
        The algorithm used in this function is based on the Bresenham's line algorithm.
        From the first position, we consider all Brsenham's lines and Manhattan lines to the second position
        Then we calculate the number of walls in each line and return the minimum number of walls.
        
        This calculating will be considered as an element in the heuristic function for choosing the nearest wall intersections
        """
        X1 = position1[1]
        X2 = position2[1]
        Y1 = position1[0]
        Y2 = position2[0]
        
        numWallIntersectionsBetweenThem = 0
        
        #! Calculate on Bresenham's lines
        if (X2 <= X1 and Y1 >= Y2):
            if (Y1 - Y2 > X1 - X2):
                temp1 = 0
                temp2 = 0
                
                for j in range (0, X1 - X2 + 1):
                    if (self.map.matrix[Y1 - j][X1 - j] in [WALL, OBSTACLE]):
                        temp1 += 1
                for j in range (1, (Y1 - Y2) - (X1 - X2) + 1):
                    if (self.map.matrix[Y1 - (X1 - X2) - j][X2] in [WALL, OBSTACLE]):
                        temp1 += 1 
                
                for j in range (0, (Y1 - Y2) - (X1 - X2) + 1):
                    if (self.map.matrix[Y1 - j][X1] in [WALL, OBSTACLE]):
                        temp2 += 1 
                for j in range (1, X1 - X2 + 1):
                    if (self.map.matrix[Y2 + (X1 - X2) - j][X1 - j] in [WALL, OBSTACLE]):
                        temp2 += 1
                        
                numWallIntersectionsBetweenThem = min(temp1, temp2)
                
            else:
                temp1 = 0
                temp2 = 0
                for j in range (0, (X1 - X2) - (Y1 - Y2) + 1):
                    if (self.map.matrix[Y1][X1 - j] in [WALL, OBSTACLE]):
                        temp1 += 1
                for j in range (1, Y1 - Y2 + 1):
                    if (self.map.matrix[Y1 - j][X2 + Y1 - Y2 - j] in [WALL, OBSTACLE]):
                        temp1 += 1
                
                for j in range (0, Y1 - Y2 + 1):
                    if (self.map.matrix[Y1 - j][X1 - j] in [WALL, OBSTACLE]):
                        temp2 += 1     
                for j in range (1, (X1 - X2) - (Y1 - Y2) + 1):
                    if (self.map.matrix[Y2][X1 - (Y1 - Y2) - j] in [WALL, OBSTACLE]):
                        temp2 += 1
                        
                numWallIntersectionsBetweenThem = min(temp1, temp2)
            
        elif (X2 >= X1 and Y1 >= Y2):
            if (Y1 - Y2 > X2 - X1):
                temp1 = 0
                temp2 = 0
                
                for j in range (0, (Y1 - Y2) - (X2 - X1) + 1):
                    if (self.map.matrix[Y1 - j][X1] in [WALL, OBSTACLE]):
                        temp1 += 1
                for j in range (1, X2 - X1 + 1):
                    if (self.map.matrix[Y2 + (X2 - X1) - j][X1 + j] in [WALL, OBSTACLE]):
                        temp1 += 1
                
                for j in range (0, X2 - X1 + 1):
                    if (self.map.matrix[Y1 - j][X1 + j] in [WALL, OBSTACLE]):
                        temp2 += 1     
                for j in range (1, (Y1 - Y2) - (X2 - X1) + 1):
                    if (self.map.matrix[Y1 - (X2 - X1) - j][X2] in [WALL, OBSTACLE]):
                        temp2 += 1
                        
                numWallIntersectionsBetweenThem = min(temp1, temp2)        
                
            else:
                temp1 = 0
                temp2 = 0
                
                for j in range (0, Y1 - Y2 + 1):
                    if (self.map.matrix[Y1 - j][X1 + j] in [WALL, OBSTACLE]):
                        temp1 += 1
                for j in range (1, X2 - X1 - (Y1 - Y2) + 1):
                    if (self.map.matrix[Y2][X1 + Y1 - Y2 + j] in [WALL, OBSTACLE]):
                        temp1 += 1
                    
                for j in range (0, X2 - X1 - (Y1 - Y2) + 1):
                    if (self.map.matrix[Y1][X1 + j] in [WALL, OBSTACLE]):
                        temp2 += 1   
                for j in range (1, Y1 - Y2 + 1):
                    if (self.map.matrix[Y1 - j][X2 - (Y1 - Y2) + j] in [WALL, OBSTACLE]):
                        temp2 += 1
                        
                numWallIntersectionsBetweenThem = min(temp1, temp2)        
                    
        elif (X2 >= X1 and Y2 >= Y1):
            if (Y2 - Y1 > X2 - X1):
                temp1 = 0
                temp2 = 0
                
                for j in range (0, X2 - X1 + 1):
                    if (self.map.matrix[Y1 + j][X1 + j] in [WALL, OBSTACLE]):
                        temp1 += 1
                for j in range (1, Y2 - Y1 - (X2 - X1) + 1):
                    if (self.map.matrix[Y1 + (X2 - X1) + j][X2] in [WALL, OBSTACLE]):
                        temp1 += 1
                
                for j in range (0, Y2 - Y1 - (X2 - X1) + 1):
                    if (self.map.matrix[Y1 + j][X1] in [WALL, OBSTACLE]):
                        temp2 += 1      
                for j in range (1, X2 - X1 + 1):
                    if (self.map.matrix[Y2 - (X2 - X1) + j][X1 + j] in [WALL, OBSTACLE]):
                        temp2 += 1
                        
                numWallIntersectionsBetweenThem = min(temp1, temp2)
                
            else:
                temp1 = 0
                temp2 = 0
                
                for j in range (0, (X2 - X1) - (Y2 - Y1) + 1):
                    if (self.map.matrix[Y1][X1 + j] in [WALL, OBSTACLE]):
                        temp1 += 1
                for j in range (1, Y2 - Y1 + 1):
                    if (self.map.matrix[Y1 + j][X2 - (Y2 - Y1) + j] in [WALL, OBSTACLE]):
                        temp1 += 1
                
                for j in range (0, Y2 - Y1 + 1):
                    if (self.map.matrix[Y1 + j][X1 + j] in [WALL, OBSTACLE]):
                        temp2 += 1       
                for j in range (1, (X2 - X1) - (Y2 - Y1) + 1):
                    if (self.map.matrix[Y2][X1 + (Y2 - Y1) + j] in [WALL, OBSTACLE]):
                        temp2 += 1
                
                numWallIntersectionsBetweenThem = min(temp1, temp2)
                    
        elif (X1 >= X2 and Y2 >= Y1):
            if (Y2 - Y1 > X1 - X2):
                temp1 = 0
                temp2 = 0
                
                for j in range (0, Y2 - Y1 - (X1 - X2) + 1):
                    if (self.map.matrix[Y1 + j][X1] in [WALL, OBSTACLE]):
                        temp1 += 1
                for j in range (1, X1 - X2 + 1):
                    if (self.map.matrix[Y2 - (X1 - X2) + j][X1 - j] in [WALL, OBSTACLE]):
                        temp1 += 1
                
                for j in range (0, X1 - X2 + 1):
                    if (self.map.matrix[Y1 + j][X1 - j] in [WALL, OBSTACLE]):
                        temp2 += 1        
                for j in range (1, Y2 - Y1 - (X1 - X2) + 1):
                    if (self.map.matrix[Y1 + (X1 - X2) + j][X2] in [WALL, OBSTACLE]):
                        temp2 += 1
                
                numWallIntersectionsBetweenThem = min(temp1, temp2)       
                
            else:
                temp1 = 0
                temp2 = 0
                
                for j in range (0, Y2 - Y1 + 1):
                    if (self.map.matrix[Y1 + j][X1 - j] in [WALL, OBSTACLE]):
                        temp1 += 1
                for j in range (1, X1 - X2 - (Y2 - Y1) + 1):
                    if (self.map.matrix[Y2][X1 - (Y2 - Y1) - j] in [WALL, OBSTACLE]):
                        temp1 += 1
                
                for j in range (0, X1 - X2 - (Y2 - Y1) + 1):
                    if (self.map.matrix[Y1][X1 - j] in [WALL, OBSTACLE]):
                        temp2 += 1       
                for j in range (1, Y2 - Y1 + 1):
                    if (self.map.matrix[Y1 + j][X2 + (Y2 - Y1) - j] in [WALL, OBSTACLE]):
                        temp2 += 1
                
                numWallIntersectionsBetweenThem = min(temp1, temp2)         
        
        #! Calculate on Manhattan lines
        temp1 = 0
        temp2 = 0           
        if (X2 <= X1 and Y1 >= Y2):
            for i in range (0, X1 - X2 + 1):
                if (self.map.matrix[Y1][X1 - i] in [WALL, OBSTACLE]):
                    temp1 += 1
            for i in range (1, Y1 - Y2 + 1):
                if (self.map.matrix[Y1 - i][X2] in [WALL, OBSTACLE]):
                    temp1 += 1
                    
            for i in range (0, Y1 - Y2 + 1):
                if (self.map.matrix[Y1 - i][X1] in [WALL, OBSTACLE]):
                    temp2 += 1
            for i in range (1, X1 - X2 + 1):
                if (self.map.matrix[Y2][X1 - i] in [WALL, OBSTACLE]):
                    temp2 += 1
            
        elif (X2 >= X1 and Y1 >= Y2):
            for i in range (0, X2 - X1 + 1):
                if (self.map.matrix[Y1][X1 + i] in [WALL, OBSTACLE]):
                    temp1 += 1
            for i in range (1, Y1 - Y2 + 1):
                if (self.map.matrix[Y1 - i][X2] in [WALL, OBSTACLE]):
                    temp1 += 1
                    
            for i in range (0, Y1 - Y2 + 1):
                if (self.map.matrix[Y1 - i][X1] in [WALL, OBSTACLE]):
                    temp2 += 1
            for i in range (1, X2 - X1 + 1):
                if (self.map.matrix[Y2][X1 + i] in [WALL, OBSTACLE]):
                    temp2 += 1
                    
        elif (X2 >= X1 and Y2 >= Y1):
            for i in range (0, X2 - X1 + 1):
                if (self.map.matrix[Y1][X1 + i] in [WALL, OBSTACLE]):
                    temp1 += 1
            for i in range (1, Y2 - Y1 + 1):
                if (self.map.matrix[Y1 + i][X2] in [WALL, OBSTACLE]):
                    temp1 += 1
                    
            for i in range (0, Y2 - Y1 + 1):
                if (self.map.matrix[Y1 + i][X1] in [WALL, OBSTACLE]):
                    temp2 += 1
            for i in range (1, X2 - X1 + 1):
                if (self.map.matrix[Y2][X1 + i] in [WALL, OBSTACLE]):
                    temp2 += 1
                    
        elif (X1 >= X2 and Y2 >= Y1):
            for i in range (0, X1 - X2 + 1):
                if (self.map.matrix[Y1][X1 - i] in [WALL, OBSTACLE]):
                    temp1 += 1
            for i in range (1, Y2 - Y1 + 1):
                if (self.map.matrix[Y1 + i][X2] in [WALL, OBSTACLE]):
                    temp1 += 1
                    
            for i in range (0, Y2 - Y1 + 1):
                if (self.map.matrix[Y1 + i][X1] in [WALL, OBSTACLE]):
                    temp2 += 1
            for i in range (1, X1 - X2 + 1):
                if (self.map.matrix[Y2][X1 - i] in [WALL, OBSTACLE]):
                    temp2 += 1
        
        #! Calculate the minimum number of walls
        numWallIntersectionsBetweenThem = min(numWallIntersectionsBetweenThem, min(temp1, temp2))
        return numWallIntersectionsBetweenThem
    
    def checkCorner (self, position: tuple[int, int]) -> bool:
        """
        Corner is a special wall intersection
            + It can be surrounded by 3 walls or obstacles
            + It can be one of 4 corners of the map
            + If it is in the edge of the map, it can be surrounded by 2 walls or obstacles
            
        Below is a demonstration of corners in a specific map:
         ------ ------ ------ ------ ------ ------ ------
        |   C  |      |   W  |   C  |      |      |   C  |
        |      |      |      |      |      |      |      |
         ------ ------ ------ ------ ------ ------ ------
        |      |      |   W  |   W  |      |      |      |
        |      |      |      |      |      |      |      |
         ------ ------ ------ ------ ------ ------ ------
        |   W  |   W  |      |      |      |      |      |
        |      |      |      |      |      |      |      |
         ------ ------ ------ ------ ------ ------ ------
        |   C  |   W  |      |      |      |      |      |
        |      |      |      |      |      |      |      |
         ------ ------ ------ ------ ------ ------ ------
        |      |      |   W  |   W  |   W  |      |      |
        |      |      |      |      |      |      |      |
         ------ ------ ------ ------ ------ ------ ------
        |      |      |   W  |   C  |   W  |      |      |
        |      |      |      |      |      |      |      |
         ------ ------ ------ ------ ------ ------ ------
        |   C  |      |   W  |      |      |      |   C  |
        |      |      |      |      |      |      |      |
         ------ ------ ------ ------ ------ ------ ------
         
        W: Wall or obstacle
        C: Corner
        
        This function returns True if the position is a corner, otherwise it returns False
        
        Identifying whether a wall intersection is a corner or not is vital in the heuristic function for choosing the nearest wall intersections
        """
        row = position[0]
        col = position[1]
        numRows = self.map.numRows
        numCols = self.map.numCols
        if (
            (row - 1 >= 0 and self.map.matrix[row - 1][col] in [WALL, OBSTACLE] and row + 1 < numRows and self.map.matrix[row + 1][col] in [WALL, OBSTACLE] and col - 1 >= 0 and self.map.matrix[row][col - 1] in [WALL, OBSTACLE])
            or 
            (row - 1 >= 0 and self.map.matrix[row - 1][col] in [WALL, OBSTACLE] and row + 1 < numRows and self.map.matrix[row + 1][col] in [WALL, OBSTACLE] and col + 1 < numCols and self.map.matrix[row][col + 1] in [WALL, OBSTACLE])
            or
            (col - 1 >= 0 and self.map.matrix[row][col - 1] in [WALL, OBSTACLE] and col + 1 < numCols and self.map.matrix[row][col + 1] in [WALL, OBSTACLE] and row - 1 >= 0 and self.map.matrix[row - 1][col] in [WALL, OBSTACLE])
            or
            (col - 1 >= 0 and self.map.matrix[row][col - 1] in [WALL, OBSTACLE] and col + 1 < numCols and self.map.matrix[row][col + 1] in [WALL, OBSTACLE] and row + 1 < numRows and self.map.matrix[row + 1][col] in [WALL, OBSTACLE])
            or
            (row == 0 and col - 1 >= 0 and self.map.matrix[row][col - 1] in [WALL, OBSTACLE] and row + 1 < numRows and self.map.matrix[row + 1][col] in [WALL, OBSTACLE])
            or
            (row == 0 and col + 1 < numCols and self.map.matrix[row][col + 1] in [WALL, OBSTACLE] and row + 1 < numRows and self.map.matrix[row + 1][col] in [WALL, OBSTACLE])
            or
            (row == numRows - 1 and col - 1 >= 0 and self.map.matrix[row][col - 1] in [WALL, OBSTACLE] and row - 1 >= 0 and self.map.matrix[row - 1][col] in [WALL, OBSTACLE])
            or
            (row == numRows - 1 and col + 1 < numCols and self.map.matrix[row][col + 1] in [WALL, OBSTACLE] and row - 1 >= 0 and self.map.matrix[row - 1][col] in [WALL, OBSTACLE])
            or
            (col == 0 and col + 1 < numCols and self.map.matrix[row][col + 1] in [WALL, OBSTACLE] and row + 1 < numRows and self.map.matrix[row + 1][col] in [WALL, OBSTACLE])
            or
            (col == 0 and col + 1 < numCols and self.map.matrix[row][col + 1] in [WALL, OBSTACLE] and row - 1 >= 0 and self.map.matrix[row - 1][col] in [WALL, OBSTACLE])
            or 
            (col == numCols - 1 and col - 1 >= 0 and self.map.matrix[row][col - 1] in [WALL, OBSTACLE] and row + 1 < numRows and self.map.matrix[row + 1][col] in [WALL, OBSTACLE])
            or
            (col == numCols - 1 and col - 1 >= 0 and self.map.matrix[row][col - 1] in [WALL, OBSTACLE] and row - 1 >= 0 and self.map.matrix[row - 1][col] in [WALL, OBSTACLE])
            or
            ((row, col) == (0, 0) and self.map.matrix[0][1] in [WALL, OBSTACLE])
            or
            ((row, col) == (0, 0) and self.map.matrix[1][0] in [WALL, OBSTACLE])
            or
            ((row, col) == (0, numCols - 1) and self.map.matrix[0][numCols - 2] in [WALL, OBSTACLE])
            or
            ((row, col) == (0, numCols - 1) and self.map.matrix[1][numCols - 1] in [WALL, OBSTACLE])
            or
            ((row, col) == (numRows - 1, 0) and self.map.matrix[numRows - 2][0] in [WALL, OBSTACLE])
            or
            ((row, col) == (numRows - 1, 0) and self.map.matrix[numRows - 1][1] in [WALL, OBSTACLE])
            or
            ((row, col) == (numRows - 1, numCols - 1) and self.map.matrix[numRows - 2][numCols - 1] in [WALL, OBSTACLE])
            or
            ((row, col) == (numRows - 1, numCols - 1) and self.map.matrix[numRows - 1][numCols - 2] in [WALL, OBSTACLE])
        ):
            return True
        
        return False