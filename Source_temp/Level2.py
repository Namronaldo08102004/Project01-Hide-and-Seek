from Level_util import *

class Hider:
    def __init__ (self, state: tuple[int, int], startPosition: tuple[int, int], map, visitedMatrix):
        self.state = state
        self.startPosition = startPosition
        self.map = map
        self.visitedMatrix = visitedMatrix
        
    def __lt__ (self, other):
        goal1 = A_Star(self.startPosition, self.state, self.map, self.visitedMatrix)
        goal2 = A_Star(self.startPosition, other.state, self.map, self.visitedMatrix)
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

class Level2 (Level):
    """
        Our strategy for level 2 is same with level 1
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
        
        #! Define seeker and hiders for the game
        self.seekerPosition: tuple[int, int] = map.seekerPosition
        self.listHiderPositions: list[tuple[int, int]] = map.listHiderPositions.copy()
        
        self.listObservableCells: list[tuple[int, int]] = self.getObservableCells(self.seekerPosition)
        self.listIdentifiedHiders: list[Hider] = self.identifyObservableHiders()
        
        #? Announcement will be broadcast by hider after each 8 steps and will exist in 2 steps
        """
        We create a dictionary of broadcast announcements
            + Key is the position of a certain announcement
            + Value is the position of the hider who broadcast that announcement 
        """
        self.announcementDict: dict[tuple[int, int], list[tuple[int, int]]] = dict()
        
        #! Get the goal position for the next move
        self.goalPosition: tuple[int, int] = None
        self.path: list[tuple[int, int]] = None
        self.pathMove: int = 0
        if (len(self.listIdentifiedHiders) != 0):
            goal = heappop(self.listIdentifiedHiders)
            self.goalPosition = goal.state
            heappush(self.listIdentifiedHiders, goal)
            self.path = self.getShortestPath(self.goalPosition)
            self.pathMove = 0
        else:
            self.goalPosition: tuple[int, int] = self.getNearestWallIntersection()
            self.path: list[tuple[int, int]] = self.getShortestPath(self.goalPosition)
            self.pathMove: int = 0
            
    def hiderTakeTurn (self, hiderPosition: tuple[int, int]):
        if (self.numHiderSteps % 8 != 7):
            return
        
        #! The hider will broadcast an announcement after each 8 steps and set the time for this announcement
        announcement = self.broadcastAnnouncement(hiderPosition)
        if (self.announcementDict.get(announcement) is None):
            self.announcementDict[announcement] = [hiderPosition]
        else:
            self.announcementDict[announcement].append(hiderPosition)
    
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
                numWalls = countNumWallsBetweenTwoPositions(startPositionForFinding, intersection)
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
    
    def identifyObservableHiders (self):
        listHiderPositions: list[Hider] = []
        
        for i in range (0, len(self.listObservableCells)):
            if (self.listObservableCells[i] in self.listHiderPositions):
                heappush(listHiderPositions, Hider(self.listObservableCells[i], self.seekerPosition, self.map.matrix, self.visitedMatrix))
            else:
                self.visitedMatrix[self.listObservableCells[i][0]][self.listObservableCells[i][1]] = True
                
        return listHiderPositions
    
    def identifyObservableAnnouncements (self):
        listAnnouncementPositions: list[tuple[int, int]] = []
        
        for i in range (0, len(self.listObservableCells)):
            if (self.announcementDict.get(self.listObservableCells[i]) is not None):
                listAnnouncementPositions.append(self.listObservableCells[i])
            
        return listAnnouncementPositions
    
    def seekerTakeTurn (self):
        def checkGoalPositionInListIdentifiedHiders (goalPosition: tuple[int, int], listIdentifiedHiders: list[Hider]):
            for hider in listIdentifiedHiders:
                if goalPosition == hider.state:
                    return True
            
            return False
        
        self.seekerPosition = self.path[self.pathMove]
        self.pathMove = self.pathMove + 1
        self.listObservableCells = self.getObservableCells(self.seekerPosition)
        
        if (len(self.listIdentifiedHiders) != 0):
            tempListIdentifiedHiders = self.identifyObservableHiders()
            listIdentifiedAnnouncements = self.identifyObservableAnnouncements()
            
            if (listIdentifiedAnnouncements):
                listCorrespondingHiders: list[Hider] = []
                for announcement in listIdentifiedAnnouncements:
                    correspondingHiders = self.announcementDict[announcement]
                    
                    for correspondingHider in correspondingHiders:
                        if (not self.visitedMatrix[correspondingHider[0]][correspondingHider[1]]):
                            listCorrespondingHiders.append(Hider(correspondingHider, self.seekerPosition, self.map.matrix, self.visitedMatrix))
                        
                self.listIdentifiedHiders = list(set(self.listIdentifiedHiders).union(set(listCorrespondingHiders)))
            
            #! Get the union of the old list of identified hiders and the new one
            self.listIdentifiedHiders = list(set(self.listIdentifiedHiders).union(set(tempListIdentifiedHiders)))
            
            if (self.seekerPosition != self.goalPosition):
                return
        else:
            self.listIdentifiedHiders = self.identifyObservableHiders()
            listIdentifiedAnnouncements = self.identifyObservableAnnouncements()
            
            if (listIdentifiedAnnouncements):
                listCorrespondingHiders: list[Hider] = []
                for announcement in listIdentifiedAnnouncements:
                    correspondingHiders = self.announcementDict[announcement]
                    
                    for correspondingHider in correspondingHiders:
                        if (not self.visitedMatrix[correspondingHider[0]][correspondingHider[1]]):
                            listCorrespondingHiders.append(Hider(correspondingHider, self.seekerPosition, self.map.matrix, self.visitedMatrix))
                        
                self.listIdentifiedHiders = list(set(self.listIdentifiedHiders).union(set(listCorrespondingHiders)))
        
        #! Observed any hider --> Conduct to touch that hider
        if (len(self.listIdentifiedHiders) != 0 and not checkGoalPositionInListIdentifiedHiders(self.goalPosition, self.listIdentifiedHiders)):
            goal = heappop(self.listIdentifiedHiders)
            self.goalPosition = goal.state
            heappush(self.listIdentifiedHiders, goal)
            self.path = self.getShortestPath(self.goalPosition)
            self.pathMove = 0
            return
        
        if (self.seekerPosition == self.goalPosition or self.visitedMatrix[self.goalPosition[0]][self.goalPosition[1]]):
            self.visitedMatrix[self.goalPosition[0]][self.goalPosition[1]] = True
            #! Reached the position of the hider
            if (len(self.listIdentifiedHiders) != 0 and checkGoalPositionInListIdentifiedHiders(self.goalPosition, self.listIdentifiedHiders)):
                _ = heappop(self.listIdentifiedHiders)
                self.listHiderPositions.remove(self.goalPosition)
                
                if (len(self.listHiderPositions) == 0):
                    return
                
                if (len(self.listIdentifiedHiders) != 0):
                    goal = heappop(self.listIdentifiedHiders)
                    self.goalPosition = goal.state
                    heappush(self.listIdentifiedHiders, goal)
                    self.path = self.getShortestPath(self.goalPosition)
                    self.pathMove = 0
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