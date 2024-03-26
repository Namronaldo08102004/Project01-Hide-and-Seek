from Map import *
from random import choice
from A_Star import *
    
class Hider:
    def __init__ (self, state: tuple[int, int], startPosition: tuple[int, int] = None, map = None, visitedMatrix = None):
        self.state = state
        self.startPosition = startPosition
        self.map = map
        self.visitedMatrix = visitedMatrix
        
        self.hiderObservableCells = self.getObservableCellsOfHider()
        
    def __lt__ (self, other):
        goal1 = None
        goal2 = None
        if (self.visitedMatrix is None):
            goal1 = A_Star(self.startPosition, self.state, self.map, self.visitedMatrix)
            goal2 = A_Star(self.startPosition, other.state, self.map, self.visitedMatrix)
        else:
            goal1 = A_Star(self.startPosition, self.state, self.map)
            goal2 = A_Star(self.startPosition, other.state, self.map)
        
        shortestPath1 = []
        shortestPath2 = []
        
        while (goal1 is not None):
            shortestPath1.append(goal1.state)
            goal1 = goal1.parent
        while (goal2 is not None):
            shortestPath2.append(goal2.state)
            goal2 = goal2.parent
        
        return len(shortestPath1) < len(shortestPath2)
    
    def __eq__ (self, other):
        return self.state == other.state
    
    def __hash__ (self):
        return hash(self.state)
    
    def getObservableCellsOfHider (self):
        mapNumRows = len(self.map)
        mapNumCols = len(self.map[0])
        
        radius_2_matrix: list[list[bool]] = []
        hider_position_in_matrix: tuple[int, int] = None
        for row in range (self.state[0] - 2, self.state[0] + 3):
            if (row >= 0 and row < mapNumRows):
                tempList: list[int] = []
            
                for col in range (self.state[1] - 2, self.state[1] + 3):
                    if (col >= 0 and col < mapNumCols):
                        if (self.map[row][col] == WALL):
                            tempList.append(False)
                        else:
                            tempList.append(True)
                            
                        if ((row, col) == self.state):
                            hider_position_in_matrix = (len(radius_2_matrix), len(tempList) - 1)
                    
                radius_2_matrix.append(tempList)
                
        X = hider_position_in_matrix[0]
        Y = hider_position_in_matrix[1]
        numRows = len(radius_2_matrix)
        numCols = len(radius_2_matrix[0])
                
        #! Check in the radius 1 around the current seeker position
        #? Case 1
        if (X - 1 >= 0 and Y - 1 >= 0 and radius_2_matrix[X - 1][Y - 1] == False):
            if (X - 2 >= 0 and Y - 2 >= 0):    
                radius_2_matrix[X - 2][Y - 2] = False
                
            if (X - 1 >= 0 and radius_2_matrix[X - 1][Y] == False):
                if (X - 2 >= 0):
                    radius_2_matrix[X - 2][Y] = False
                if (X - 2 >= 0 and Y - 1 >= 0):
                    radius_2_matrix[X - 2][Y - 1] = False
            
            if (Y - 1 >= 0 and radius_2_matrix[X][Y - 1] == False):
                if (Y - 2 >= 0):
                    radius_2_matrix[X][Y - 2] = False
                if (X - 1 >= 0 and Y - 2 >= 0):
                    radius_2_matrix[X - 1][Y - 2] = False
        
        #? Case 2
        if (X - 1 >= 0 and radius_2_matrix[X - 1][Y] == False):
            if (X - 2 >= 0):
                radius_2_matrix[X - 2][Y] = False
                
            if (X - 1 >= 0 and Y - 1 >= 0 and radius_2_matrix[X - 1][Y - 1] == False):
                if (X - 2 >= 0 and Y - 2 >= 0):    
                    radius_2_matrix[X - 2][Y - 2] = False
                if (X - 2 >= 0 and Y - 1 >= 0):
                    radius_2_matrix[X - 2][Y - 1] = False
                    
            if (X - 1 >= 0 and Y + 1 < numCols and radius_2_matrix[X - 1][Y + 1] == False):
                if (X - 2 >= 0 and Y + 2 < numCols):
                    radius_2_matrix[X - 2][Y + 2] = False
                if (X - 2 >= 0 and Y + 1 < numCols):
                    radius_2_matrix[X - 2][Y + 1] = False
            
        #? Case 3
        if (X - 1 >= 0 and Y + 1 < numCols and radius_2_matrix[X - 1][Y + 1] == False):
            if (X - 2 >= 0 and Y + 2 < numCols):
                radius_2_matrix[X - 2][Y + 2] = False
                
            if (X - 1 >= 0 and radius_2_matrix[X - 1][Y] == False):
                if (X - 2 >= 0):
                    radius_2_matrix[X - 2][Y] = False
                if (X - 2 >= 0 and Y + 1 < numCols):
                    radius_2_matrix[X - 2][Y + 1] = False
                    
            if (Y + 1 < numCols and radius_2_matrix[X][Y + 1] == False):
                if (Y + 2 < numCols):
                    radius_2_matrix[X][Y + 2] = False
                if (X - 1 >= 0 and Y + 2 < numCols):
                    radius_2_matrix[X - 1][Y + 2] = False
        
        #? Case 4      
        if (Y + 1 < numCols and radius_2_matrix[X][Y + 1] == False):
            if (Y + 2 < numCols):
                radius_2_matrix[X][Y + 2] = False
                
            if (X - 1 >= 0 and Y + 1 < numCols and radius_2_matrix[X - 1][Y + 1] == False):
                if (X - 2 >= 0 and Y + 2 < numCols):
                    radius_2_matrix[X - 2][Y + 2] = False
                if (X - 1 >= 0 and Y + 2 < numCols):
                    radius_2_matrix[X - 1][Y + 2] = False
                    
            if (X + 1 < numRows and Y + 1 < numCols and radius_2_matrix[X + 1][Y + 1] == False):
                if (X + 2 < numRows and Y + 2 < numCols):
                    radius_2_matrix[X + 2][Y + 2] = False
                if (X + 1 < numRows and Y + 2 < numCols):
                    radius_2_matrix[X + 1][Y + 2] = False
        
        #? Case 5 
        if (X + 1 < numRows and Y + 1 < numCols and radius_2_matrix[X + 1][Y + 1] == False):
            if (X + 2 < numRows and Y + 2 < numCols):
                radius_2_matrix[X + 2][Y + 2] = False
            
            if (Y + 1 < numCols and radius_2_matrix[X][Y + 1] == False):
                if (Y + 2 < numCols):
                    radius_2_matrix[X][Y + 2] = False
                if (X + 1 < numRows and Y + 2 < numCols):
                    radius_2_matrix[X + 1][Y + 2] = False
                
            if (X + 1 < numRows and radius_2_matrix[X + 1][Y] == False):
                if (X + 2 < numRows):
                    radius_2_matrix[X + 2][Y] = False
                if (X + 2 < numRows and Y + 1 < numCols):
                    radius_2_matrix[X + 2][Y + 1] = False

        #? Case 6
        if (X + 1 < numRows and radius_2_matrix[X + 1][Y] == False):
            if (X + 2 < numRows):
                radius_2_matrix[X + 2][Y] = False
                
            if (X + 1 < numRows and Y + 1 < numCols and radius_2_matrix[X + 1][Y + 1] == False):
                if (X + 2 < numRows and Y + 2 < numCols):
                    radius_2_matrix[X + 2][Y + 2] = False
                if (X + 2 < numRows and Y + 1 < numCols):
                    radius_2_matrix[X + 2][Y + 1] = False
            
            if (X + 1 < numRows and Y - 1 >= 0 and radius_2_matrix[X + 1][Y - 1] == False):
                if (X + 2 < numRows and Y - 2 >= 0):
                    radius_2_matrix[X + 2][Y - 2] = False
                if (X + 2 < numRows and Y - 1 >= 0):
                    radius_2_matrix[X + 2][Y - 1] = False
                
        #? Case 7
        if (X + 1 < numRows and Y - 1 >= 0 and radius_2_matrix[X + 1][Y - 1] == False):
            if (X + 2 < numRows and Y - 2 >= 0):
                radius_2_matrix[X + 2][Y - 2] = False
                
            if (X + 1 < numRows and radius_2_matrix[X + 1][Y] == False):
                if (X + 2 < numRows):
                    radius_2_matrix[X + 2][Y] = False
                if (X + 2 < numRows and Y - 1 >= 0):
                    radius_2_matrix[X + 2][Y - 1] = False
                    
            if (Y - 1 >= 0 and radius_2_matrix[X][Y - 1] == False):
                if (Y - 2 >= 0):
                    radius_2_matrix[X][Y - 2] = False
                if (X + 1 < numRows and Y - 2 >= 0):
                    radius_2_matrix[X + 1][Y - 2] = False
                
        #? Case 8
        if (Y - 1 >= 0 and radius_2_matrix[X][Y - 1] == False):
            if (Y - 2 >= 0):
                radius_2_matrix[X][Y - 2] = False
                
            if (X + 1 < numRows and Y - 1 >= 0 and radius_2_matrix[X + 1][Y - 1] == False):
                if (X + 2 < numRows and Y - 2 >= 0):
                    radius_2_matrix[X + 2][Y - 2] = False
                if (X + 1 < numRows and Y - 2 >= 0):
                    radius_2_matrix[X + 1][Y - 2] = False

                    
            if (X - 1 >= 0 and Y - 1 >= 0 and radius_2_matrix[X - 1][Y - 1] == False):
                if (X - 2 >= 0 and Y - 2 >= 0):    
                    radius_2_matrix[X - 2][Y - 2] = False
                if (X - 1 >= 0 and Y - 2 >= 0):
                    radius_2_matrix[X - 1][Y - 2] = False
        
        listObservablePositions = []
        index_row = 0
        for row in range (self.state[0] - 2, self.state[0] + 3):
            if (row >= 0 and row < mapNumRows):
                index_col = 0
                
                for col in range (self.state[1] - 2, self.state[1] + 3):
                    if (col >= 0 and col < mapNumCols):
                        if (radius_2_matrix[index_row][index_col] and (row, col) != self.state):
                            listObservablePositions.append((row, col))
                        index_col = index_col + 1
                        
                index_row = index_row + 1
                    
        return listObservablePositions
    
class Level:
    def __init__ (self, map: Map):
        self.map: Map = map
        self.score: int = 0
        self.numSeekerSteps: int = 0 #? Increase this attribute by 1 if seeker took its turn and the game is not over
        self.numHiderSteps: int = 0 #? Increase this attribute by 1 if hider took its turn and the game is not over
        self.takeTurn: int = SEEKER
        
    def broadcastAnnouncement (self, hiderPosition: tuple[int, int]) -> tuple[int, int]:
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
        radius_3_matrix: list[list[bool]] = []
        seeker_position_in_matrix: tuple[int, int] = None
        for row in range (seekerPosition[0] - 3, seekerPosition[0] + 4):
            if (row >= 0 and row < self.map.numRows):
                tempList: list[int] = []
            
                for col in range (seekerPosition[1] - 3, seekerPosition[1] + 4):
                    if (col >= 0 and col < self.map.numCols):
                        if (self.map.matrix[row][col] == WALL):
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
                
        #! Check in the radius 1 around the current seeker position
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