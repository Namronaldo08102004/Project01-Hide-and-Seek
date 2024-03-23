from Level_util import *

class Level1 (Level):
    """
        Our strategy for level 1 is sequentialy finding each wall intersection in the map.
        When reached a certain wall intersection:
            + If there is not hider around this wall position, we will move to the next nearest wall intersection.
            + If there is hider, conduct to touch that hider.
        Through the process of moving among other wall intersections, we keep a matrix for checking visited cells which are
        identified to not include hider, and we hope that we can find the hider through the process
        If there is not any hiders found, we will check unvisited cells and move sequentially to each cell in the order from nearest
        to furtherest.
        
        A wall intersection is demonstrated by the following image:
         ------ ------
        |      |      |
        |      |      |
         ------ ------
        |      | <----
        |      | 
         ------
    """ 
    def __init__ (self, map: Map):
        Level.__init__ (self, map)
        
        #! Define a temporary matrix for saving cells that were identified to not include hider
        self.visitedMatrix: list[list[bool]] = []
        for row in range (0, self.map.numRows):
            tempList = []
            for col in range (0, self.map.numCols):
                if (self.map.matrix[row][col] == 0 or self.map.matrix[row][col] == 2):
                    tempList.append(False)
                else:
                    tempList.append(True)
            
            self.visitedMatrix.append(tempList)
            
        #! Define a list of all wall intersections in the map
        self.listWallIntersections: list[tuple[int, int]] = []
        for row in range (0, self.map.numRows):
            for col in range (0, self.map.numCols):
                if (self.map.matrix[row][col] == WALL and (row + 1 < self.map.numRows and self.map.matrix[row + 1][col] == WALL)
                    and (col + 1 < self.map.numCols and self.map.matrix[row][col + 1] == WALL)):
                    if (self.map.matrix[row + 1][col + 1] != WALL):
                        self.listWallIntersections.append((row + 1, col + 1))
                
                if (self.map.matrix[row][col] == WALL and (row + 1 < self.map.numRows and self.map.matrix[row + 1][col] == WALL)
                    and (col - 1 >= 0 and self.map.matrix[row][col - 1] == WALL)):
                    if (self.map.matrix[row + 1][col - 1] != WALL):
                        self.listWallIntersections.append((row + 1, col - 1))
                
                if (self.map.matrix[row][col] == WALL and (row - 1 >= 0 and self.map.matrix[row - 1][col] == WALL)
                    and (col - 1 >= 0 and self.map.matrix[row][col - 1] == WALL)):
                    if (self.map.matrix[row - 1][col - 1] != WALL):
                        self.listWallIntersections.append((row - 1, col - 1))
                
                if (self.map.matrix[row][col] == WALL and (row - 1 >= 0 and self.map.matrix[row - 1][col] == WALL)
                    and (col + 1 < self.map.numCols and self.map.matrix[row][col + 1] == WALL)):
                    if (self.map.matrix[row - 1][col + 1] != WALL):
                        self.listWallIntersections.append((row - 1, col + 1))
                    
                if ((row, col) == (0, self.map.numCols - 1) or (row, col) == (0, 0)
                    or (row, col) == (self.map.numRows - 1, self.map.numCols - 1)
                    or (row, col) == (self.map.numRows - 1, 0)):
                    if (self.map.matrix[row][col] != WALL):
                        self.listWallIntersections.append((row, col))
                
                if ((col == self.map.numCols - 1 or col == 0) and self.map.matrix[row][col] == WALL):
                    if (row - 1 >= 0 and self.map.matrix[row - 1][col] != WALL):
                        self.listWallIntersections.append((row - 1, col))

                    if (row + 1 < self.map.numRows and self.map.matrix[row + 1][col] != WALL):
                        self.listWallIntersections.append((row + 1, col))
                
                if ((row == self.map.numRows - 1 or row == 0) and self.map.matrix[row][col] == WALL):
                    if (col - 1 >= 0 and self.map.matrix[row][col - 1] != WALL):
                        self.listWallIntersections.append((row, col - 1))

                    if (col + 1 < self.map.numCols and self.map.matrix[row][col + 1] != WALL):
                        self.listWallIntersections.append((row, col + 1))
        
        #! Define seeker and hider for the game
        self.seekerPosition: tuple[int, int] = map.seekerPosition
        self.listObservableCells: list[tuple[int, int]] = self.getObservableCells(self.seekerPosition)
        self.IdentifiedHider: tuple[int, int] = self.identifyObservableHider()
        self.IdentifiedAnnouncement: tuple[int, int] = None
        self.listUnvisitedPositionsAroundAnnouncement: list[tuple[int, int]] = None
        
        self.hiderPosition: tuple[int, int] = map.listHiderPositions[0]
            
        #? Announcement will be broadcast by hider after each 8 steps and will exist in 2 steps
        self.announcement: tuple[int, int] = None
        self.announcementTime: int = None
        
        #! Get the goal position for the next move
        self.goalPosition: tuple[int, int] = None
        self.path: list[tuple[int, int]] = None
        self.pathMove: int = 0
        if (self.IdentifiedHider is not None):
            self.goalPosition = self.IdentifiedHider
            self.path = self.getShortestPath(self.goalPosition)
            self.pathMove = 0
        elif (self.IdentifiedHider is None and self.IdentifiedAnnouncement is not None):
            self.goalPosition = self.IdentifiedAnnouncement
            self.path = self.getShortestPath(self.goalPosition)
            self.pathMove = 0
        else:
            self.goalPosition: tuple[int, int] = self.getNearestWallIntersection()
            self.path: list[tuple[int, int]] = self.getShortestPath(self.goalPosition)
            self.pathMove: int = 0
            
    def hiderTakeTurn (self):
        if (self.numHiderSteps % 8 != 7):
            return
        
        #! The hider will broadcast an announcement after each 8 steps and set the time for this announcement
        self.announcement = self.broadcastAnnouncement(self.hiderPosition)
        self.announcementTime = 0
    
    def getNearestWallIntersection (self) -> tuple[int, int]:
        def countNumWallsBetweenTwoPositions (position1: tuple[int, int], position2: tuple[int, int]):
            X1 = position1[1]
            X2 = position2[1]
            Y1 = position1[0]
            Y2 = position2[0]
            
            #! Calculate the number of walls in the shortest path (without any walls in the map) from the current seeker position to this wall intersection
            numWallIntersectionsBetweenThem = 0
            if (X2 <= X1 and Y1 >= Y2):
                if (Y1 - Y2 > X1 - X2):
                    temp1 = 0
                    temp2 = 0
                    
                    for j in range (0, X1 - X2 + 1):
                        if (self.map.matrix[Y1 - j][X1 - j] == WALL):
                            temp1 += 1
                    for j in range (1, (Y1 - Y2) - (X1 - X2) + 1):
                        if (self.map.matrix[Y1 - (X1 - X2) - j][X2] == WALL):
                            temp1 += 1 
                    
                    for j in range (0, (Y1 - Y2) - (X1 - X2) + 1):
                        if (self.map.matrix[Y1 - j][X1] == WALL):
                            temp2 += 1 
                    for j in range (1, X1 - X2 + 1):
                        if (self.map.matrix[Y2 + (X1 - X2) - j][X1 - j] == WALL):
                            temp2 += 1
                            
                    numWallIntersectionsBetweenThem = min(temp1, temp2)
                    
                else:
                    temp1 = 0
                    temp2 = 0
                    for j in range (0, (X1 - X2) - (Y1 - Y2) + 1):
                        if (self.map.matrix[Y1][X1 - j] == WALL):
                            temp1 += 1
                    for j in range (1, Y1 - Y2 + 1):
                        if (self.map.matrix[Y1 - j][X2 + Y1 - Y2 - j] == WALL):
                            temp1 += 1
                    
                    for j in range (0, Y1 - Y2 + 1):
                        if (self.map.matrix[Y1 - j][X1 - j] == WALL):
                            temp2 += 1     
                    for j in range (1, (X1 - X2) - (Y1 - Y2) + 1):
                        if (self.map.matrix[Y2][X1 - (Y1 - Y2) - j] == WALL):
                            temp2 += 1
                            
                    numWallIntersectionsBetweenThem = min(temp1, temp2)
                
            elif (X2 >= X1 and Y1 >= Y2):
                if (Y1 - Y2 > X2 - X1):
                    temp1 = 0
                    temp2 = 0
                    
                    for j in range (0, (Y1 - Y2) - (X2 - X1) + 1):
                        if (self.map.matrix[Y1 - j][X1] == WALL):
                            temp1 += 1
                    for j in range (1, X2 - X1 + 1):
                        if (self.map.matrix[Y2 + (X2 - X1) - j][X1 + j] == WALL):
                            temp1 += 1
                    
                    for j in range (0, X2 - X1 + 1):
                        if (self.map.matrix[Y1 - j][X1 + j] == WALL):
                            temp2 += 1     
                    for j in range (1, (Y1 - Y2) - (X2 - X1) + 1):
                        if (self.map.matrix[Y1 - (X2 - X1) - j][X2] == WALL):
                            temp2 += 1
                            
                    numWallIntersectionsBetweenThem = min(temp1, temp2)        
                    
                else:
                    temp1 = 0
                    temp2 = 0
                    
                    for j in range (0, Y1 - Y2 + 1):
                        if (self.map.matrix[Y1 - j][X1 + j] == WALL):
                            temp1 += 1
                    for j in range (1, X2 - X1 - (Y1 - Y2) + 1):
                        if (self.map.matrix[Y2][X1 + Y1 - Y2 + j] == WALL):
                            temp1 += 1
                        
                    for j in range (0, X2 - X1 - (Y1 - Y2) + 1):
                        if (self.map.matrix[Y1][X1 + j] == WALL):
                            temp2 += 1   
                    for j in range (1, Y1 - Y2 + 1):
                        if (self.map.matrix[Y1 - j][X2 - (Y1 - Y2) + j] == WALL):
                            temp2 += 1
                            
                    numWallIntersectionsBetweenThem = min(temp1, temp2)        
                        
            elif (X2 >= X1 and Y2 >= Y1):
                if (Y2 - Y1 > X2 - X1):
                    temp1 = 0
                    temp2 = 0
                    
                    for j in range (0, X2 - X1 + 1):
                        if (self.map.matrix[Y1 + j][X1 + j] == WALL):
                            temp1 += 1
                    for j in range (1, Y2 - Y1 - (X2 - X1) + 1):
                        if (self.map.matrix[Y1 + (X2 - X1) + j][X2] == WALL):
                            temp1 += 1
                    
                    for j in range (0, Y2 - Y1 - (X2 - X1) + 1):
                        if (self.map.matrix[Y1 + j][X1] == WALL):
                            temp2 += 1      
                    for j in range (1, X2 - X1 + 1):
                        if (self.map.matrix[Y2 - (X2 - X1) + j][X1 + j] == WALL):
                            temp2 += 1
                            
                    numWallIntersectionsBetweenThem = min(temp1, temp2)
                    
                else:
                    temp1 = 0
                    temp2 = 0
                    
                    for j in range (0, (X2 - X1) - (Y2 - Y1) + 1):
                        if (self.map.matrix[Y1][X1 + j] == WALL):
                            temp1 += 1
                    for j in range (1, Y2 - Y1 + 1):
                        if (self.map.matrix[Y1 + j][X2 - (Y2 - Y1) + j] == WALL):
                            temp1 += 1
                    
                    for j in range (0, Y2 - Y1 + 1):
                        if (self.map.matrix[Y1 + j][X1 + j] == WALL):
                            temp2 += 1       
                    for j in range (1, (X2 - X1) - (Y2 - Y1) + 1):
                        if (self.map.matrix[Y2][X1 + (Y2 - Y1) + j] == WALL):
                            temp2 += 1
                    
                    numWallIntersectionsBetweenThem = min(temp1, temp2)
                        
            elif (X1 >= X2 and Y2 >= Y1):
                if (Y2 - Y1 > X1 - X2):
                    temp1 = 0
                    temp2 = 0
                    
                    for j in range (0, Y2 - Y1 - (X1 - X2) + 1):
                        if (self.map.matrix[Y1 + j][X1] == WALL):
                            temp1 += 1
                    for j in range (1, X1 - X2 + 1):
                        if (self.map.matrix[Y2 - (X1 - X2) + j][X1 - j] == WALL):
                            temp1 += 1
                    
                    for j in range (0, X1 - X2 + 1):
                        if (self.map.matrix[Y1 + j][X1 - j] == WALL):
                            temp2 += 1        
                    for j in range (1, Y2 - Y1 - (X1 - X2) + 1):
                        if (self.map.matrix[Y1 + (X1 - X2) + j][X2] == WALL):
                            temp2 += 1
                    
                    numWallIntersectionsBetweenThem = min(temp1, temp2)       
                    
                else:
                    temp1 = 0
                    temp2 = 0
                    
                    for j in range (0, Y2 - Y1 + 1):
                        if (self.map.matrix[Y1 + j][X1 - j] == WALL):
                            temp1 += 1
                    for j in range (1, X1 - X2 - (Y2 - Y1) + 1):
                        if (self.map.matrix[Y2][X1 - (Y2 - Y1) - j] == WALL):
                            temp1 += 1
                    
                    for j in range (0, X1 - X2 - (Y2 - Y1) + 1):
                        if (self.map.matrix[Y1][X1 - j] == WALL):
                            temp2 += 1       
                    for j in range (1, Y2 - Y1 + 1):
                        if (self.map.matrix[Y1 + j][X2 + (Y2 - Y1) - j] == WALL):
                            temp2 += 1
                    
                    numWallIntersectionsBetweenThem = min(temp1, temp2)         
            
            temp1 = 0
            temp2 = 0           
            if (X2 <= X1 and Y1 >= Y2):
                for i in range (0, X1 - X2 + 1):
                    if (self.map.matrix[Y1][X1 - i] == WALL):
                        temp1 += 1
                for i in range (1, Y1 - Y2 + 1):
                    if (self.map.matrix[Y1 - i][X2] == WALL):
                        temp1 += 1
                        
                for i in range (0, Y1 - Y2 + 1):
                    if (self.map.matrix[Y1 - i][X1] == WALL):
                        temp2 += 1
                for i in range (1, X1 - X2 + 1):
                    if (self.map.matrix[Y2][X1 - i] == WALL):
                        temp2 += 1
                
            elif (X2 >= X1 and Y1 >= Y2):
                for i in range (0, X2 - X1 + 1):
                    if (self.map.matrix[Y1][X1 + i] == WALL):
                        temp1 += 1
                for i in range (1, Y1 - Y2 + 1):
                    if (self.map.matrix[Y1 - i][X2] == WALL):
                        temp1 += 1
                        
                for i in range (0, Y1 - Y2 + 1):
                    if (self.map.matrix[Y1 - i][X1] == WALL):
                        temp2 += 1
                for i in range (1, X2 - X1 + 1):
                    if (self.map.matrix[Y2][X1 + i] == WALL):
                        temp2 += 1
                        
            elif (X2 >= X1 and Y2 >= Y1):
                for i in range (0, X2 - X1 + 1):
                    if (self.map.matrix[Y1][X1 + i] == WALL):
                        temp1 += 1
                for i in range (1, Y2 - Y1 + 1):
                    if (self.map.matrix[Y1 + i][X2] == WALL):
                        temp1 += 1
                        
                for i in range (0, Y2 - Y1 + 1):
                    if (self.map.matrix[Y1 + i][X1] == WALL):
                        temp2 += 1
                for i in range (1, X2 - X1 + 1):
                    if (self.map.matrix[Y2][X1 + i] == WALL):
                        temp2 += 1
                        
            elif (X1 >= X2 and Y2 >= Y1):
                for i in range (0, X1 - X2 + 1):
                    if (self.map.matrix[Y1][X1 - i] == WALL):
                        temp1 += 1
                for i in range (1, Y2 - Y1 + 1):
                    if (self.map.matrix[Y1 + i][X2] == WALL):
                        temp1 += 1
                        
                for i in range (0, Y2 - Y1 + 1):
                    if (self.map.matrix[Y1 + i][X1] == WALL):
                        temp2 += 1
                for i in range (1, X1 - X2 + 1):
                    if (self.map.matrix[Y2][X1 - i] == WALL):
                        temp2 += 1
            
            numWallIntersectionsBetweenThem = min(numWallIntersectionsBetweenThem, min(temp1, temp2))
            return numWallIntersectionsBetweenThem
        
        def checkCorner (position: tuple[int, int]) -> bool:
            row = position[0]
            col = position[1]
            numRows = self.map.numRows
            numCols = self.map.numCols
            if (
                (row - 1 >= 0 and self.map.matrix[row - 1][col] == WALL and row + 1 < numRows and self.map.matrix[row + 1][col] == WALL and col - 1 >= 0 and self.map.matrix[row][col - 1] == WALL)
                or 
                (row - 1 >= 0 and self.map.matrix[row - 1][col] == WALL and row + 1 < numRows and self.map.matrix[row + 1][col] == WALL and col + 1 < numCols and self.map.matrix[row][col + 1] == WALL)
                or
                (col - 1 >= 0 and self.map.matrix[row][col - 1] == WALL and col + 1 < numCols and self.map.matrix[row][col + 1] == WALL and row - 1 >= 0 and self.map.matrix[row - 1][col] == WALL)
                or
                (col - 1 >= 0 and self.map.matrix[row][col - 1] == WALL and col + 1 < numCols and self.map.matrix[row][col + 1] == WALL and row + 1 < numRows and self.map.matrix[row + 1][col] == WALL)
                or
                (row == 0 and col - 1 >= 0 and self.map.matrix[row][col - 1] == WALL and row + 1 < numRows and self.map.matrix[row + 1][col] == WALL)
                or
                (row == 0 and col + 1 < numCols and self.map.matrix[row][col + 1] == WALL and row + 1 < numRows and self.map.matrix[row + 1][col] == WALL)
                or
                (row == numRows - 1 and col - 1 >= 0 and self.map.matrix[row][col - 1] == WALL and row - 1 >= 0 and self.map.matrix[row - 1][col] == WALL)
                or
                (row == numRows - 1 and col + 1 < numCols and self.map.matrix[row][col + 1] == WALL and row - 1 >= 0 and self.map.matrix[row - 1][col] == WALL)
                or
                (col == 0 and col + 1 < numCols and self.map.matrix[row][col + 1] == WALL and row + 1 < numRows and self.map.matrix[row + 1][col] == WALL)
                or
                (col == 0 and col + 1 < numCols and self.map.matrix[row][col + 1] == WALL and row - 1 >= 0 and self.map.matrix[row - 1][col] == WALL)
                or 
                (col == numCols - 1 and col - 1 >= 0 and self.map.matrix[row][col - 1] == WALL and row + 1 < numRows and self.map.matrix[row + 1][col] == WALL)
                or
                (col == numCols - 1 and col - 1 >= 0 and self.map.matrix[row][col - 1] == WALL and row - 1 >= 0 and self.map.matrix[row - 1][col] == WALL)
                or
                ((row, col) == (0, 0) and self.map.matrix[0][1] == WALL)
                or
                ((row, col) == (0, 0) and self.map.matrix[1][0] == WALL)
                or
                ((row, col) == (0, numCols - 1) and self.map.matrix[0][numCols - 2] == WALL)
                or
                ((row, col) == (0, numCols - 1) and self.map.matrix[1][numCols - 1] == WALL)
                or
                ((row, col) == (numRows - 1, 0) and self.map.matrix[numRows - 2][0] == WALL)
                or
                ((row, col) == (numRows - 1, 0) and self.map.matrix[numRows - 1][1] == WALL)
                or
                ((row, col) == (numRows - 1, numCols - 1) and self.map.matrix[numRows - 2][numCols - 1] == WALL)
                or
                ((row, col) == (numRows - 1, numCols - 1) and self.map.matrix[numRows - 1][numCols - 2] == WALL)
            ):
                return True
            
            return False
        
        #! Add all unvisited wall intersections to a list
        unvisitedWallIntersections: list[tuple[tuple[int, int], int]] = []
        startPositionForFinding = None
        if (self.goalPosition is None):
            startPositionForFinding = self.seekerPosition
        else:
            startPositionForFinding = self.goalPosition
        
        for intersection in self.listWallIntersections:
            if (not self.visitedMatrix[intersection[0]][intersection[1]]):
                listObservableCells = self.getObservableCells(intersection)
                
                numWalls = countNumWallsBetweenTwoPositions(startPositionForFinding, intersection)
                for cell in listObservableCells:
                    numWalls = min(countNumWallsBetweenTwoPositions(startPositionForFinding, cell), numWalls)
                unvisitedWallIntersections.append((intersection, numWalls))
                
        #! We will select wall intersections with the minimum num walls
        chosenWallIntersections: list[WallIntersection] = []
        for intersection in unvisitedWallIntersections:
            heappush(chosenWallIntersections, WallIntersection(intersection[0], startPositionForFinding, self.map.matrix, self.visitedMatrix, intersection[1], checkCorner(intersection[0])))
        
        if (len(chosenWallIntersections) == 0):
            return None
          
        #! Choose a wall intersection with the smallest optimal path cost from the current seeker position
        intersection = heappop(chosenWallIntersections)
        return intersection.state
            
    def getShortestPath (self, goalPosition: tuple[int, int]) -> list[tuple[int, int]]:
        #! Be sure that the path will be from the next step of the start position to the goal position
        goal = A_Star(self.seekerPosition, goalPosition, self.map.matrix, self.visitedMatrix)
        shortestPath = []
        
        while (goal is not None):
            shortestPath.append(goal.state)
            goal = goal.parent
        
        shortestPath = shortestPath[:-1]
        shortestPath = shortestPath[::-1]
        
        return shortestPath
    
    def identifyObservableHider (self):
        Position: tuple[int, int] = None
        
        for i in range (0, len(self.listObservableCells)):
            if (self.map.matrix[self.listObservableCells[i][0]][self.listObservableCells[i][1]] == HIDER):
                Position = self.listObservableCells[i]
            else:
                self.visitedMatrix[self.listObservableCells[i][0]][self.listObservableCells[i][1]] = True
                
        return Position
    
    def identifyObservableAnnouncement (self):
        for i in range (0, len(self.listObservableCells)):
            if (self.announcement is not None and self.listObservableCells[i] == self.announcement):
                return self.listObservableCells[i]
            
        return None
    
    def seekerTakeTurn (self):
        self.seekerPosition = self.path[self.pathMove]
        self.pathMove = self.pathMove + 1
        self.listObservableCells = self.getObservableCells(self.seekerPosition)
        if (self.IdentifiedHider is not None):
            return
        else:
            self.IdentifiedHider = self.identifyObservableHider()
            
        if (self.IdentifiedAnnouncement is None):
            self.IdentifiedAnnouncement = self.identifyObservableAnnouncement()
            if (self.IdentifiedAnnouncement is not None):
                self.IdentifiedHider = self.hiderPosition
        
        #! Observed hider --> Conduct to touch the hider
        if (self.IdentifiedHider is not None and self.goalPosition != self.IdentifiedHider):
            self.goalPosition = self.IdentifiedHider
            self.path = self.getShortestPath(self.goalPosition)
            self.pathMove = 0
            return
        
        if (self.seekerPosition == self.goalPosition or self.visitedMatrix[self.goalPosition[0]][self.goalPosition[1]]):
            #! Reached the position of the hider -> Stop
            if (self.IdentifiedHider is not None):
                return       
            else:
                self.goalPosition = self.getNearestWallIntersection()
                if (self.goalPosition is not None):
                    self.path = self.getShortestPath(self.goalPosition)
                    self.pathMove = 0
                else:
                    level = 1
                    found = False
                    maxLevel = max(self.seekerPosition[0], max(self.map.numRows - 1 - self.seekerPosition[0], max(self.seekerPosition[1], self.map.numCols - 1 - self.seekerPosition[1])))
                    
                    while (not found and level <= maxLevel):
                        for row in range (self.seekerPosition[0] - level, self.seekerPosition[0] + level + 1):
                            if (row >= 0 and row < self.map.numRows):
                                for col in range (self.seekerPosition[1] - level, self.seekerPosition[1] + level + 1):
                                    if (col >= 0 and col < self.map.numCols):
                                        if (not self.visitedMatrix[row][col]):
                                            self.goalPosition = (row, col)
                                            found = True
                                            break
                            
                            if (found):
                                break
                        
                        if (found):
                            break
                
                        level = level + 1
                        
                    if (self.goalPosition is not None):
                        self.path = self.getShortestPath(self.goalPosition)
                        self.pathMove = 0
                    else:
                        raise Exception ("Your map is missing the hider")
                    
    def level1 (self):
        """
        This function is created for saving all essential things in level 1 for displaying on the game screen
        It will return a list of things, each thing will encompass 5 things:
            + The position of the seeker
            + The position of the hider
            + The current score of the game
            + The list of cells that the seeker can observe at the current time
            + The announcement that the hider broadcast (It can be None if it does not exist)
        """
        listThingsInLevel1 = []
        listThingsInLevel1.append((self.seekerPosition, self.hiderPosition, self.score, self.listObservableCells, self.announcement))
                
        while (True):
            if (self.takeTurn == SEEKER):
                self.seekerTakeTurn()
                self.takeTurn = HIDER
                if (self.seekerPosition != self.hiderPosition):
                    self.numSeekerSteps = self.numSeekerSteps + 1
                    self.score = self.score - 1
                else:
                    self.score = self.score + 20
                    break
                
                listThingsInLevel1.append((self.seekerPosition, self.hiderPosition, self.score, self.listObservableCells, self.announcement))
            else:
                self.hiderTakeTurn()
                self.takeTurn = SEEKER
                if (self.seekerPosition != self.hiderPosition):
                    self.numHiderSteps = self.numHiderSteps + 1
                    if (self.announcementTime is not None and self.announcementTime < 1):
                        self.announcementTime = self.announcementTime + 1
                    else:
                        #! After 2 steps, the announcement disappears
                        if (self.announcementTime is not None):
                            self.announcement = None
                            self.announcementTime = None
                else:
                    break
        
        return listThingsInLevel1