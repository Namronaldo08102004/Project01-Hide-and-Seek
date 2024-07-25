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
            self.path = self.getShortestPath(self.seekerPosition, self.goalPosition, self.visitedMatrix)
            self.pathMove = 0
        elif (self.IdentifiedHider is None and self.IdentifiedAnnouncement is not None):
            self.goalPosition = self.IdentifiedAnnouncement
            self.path = self.getShortestPath(self.seekerPosition, self.goalPosition, self.visitedMatrix)
            self.pathMove = 0
        else:
            self.goalPosition: tuple[int, int] = self.getNearestWallIntersection()
            self.path: list[tuple[int, int]] = self.getShortestPath(self.seekerPosition, self.goalPosition, self.visitedMatrix)
            self.pathMove: int = 0
            
    def hiderTakeTurn (self):
        if (self.numHiderSteps % 8 != 7):
            return
        
        #! The hider will broadcast an announcement after each 8 steps and set the time for this announcement
        self.announcement = self.broadcastAnnouncement(self.hiderPosition)
        self.announcementTime = 0
    
    def getNearestWallIntersection (self) -> tuple[int, int]:
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
                
                numWalls = self.countNumWallsBetweenTwoPositions(startPositionForFinding, intersection)
                for cell in listObservableCells:
                    numWalls = min(self.countNumWallsBetweenTwoPositions(startPositionForFinding, cell), numWalls)
                unvisitedWallIntersections.append((intersection, numWalls))
                
        nearestWallIntersection: tuple[int, int] = None
        minHeuristic = 1000000000
        AStar = None
        for intersection in unvisitedWallIntersections:
            isCorner = self.checkCorner(intersection[0])
            if (intersection[1] - 0.9 * isCorner < minHeuristic):
                nearestWallIntersection = intersection[0]
                shorestPath = self.getShortestPath(startPositionForFinding, nearestWallIntersection, self.visitedMatrix)
                AStar = len(shorestPath)
                minHeuristic = intersection[1] - 0.9 * isCorner
            elif (intersection[1] - 0.9 * isCorner == minHeuristic):
                shorestPath = self.getShortestPath(startPositionForFinding, intersection[0], self.visitedMatrix)
                if (AStar is None or (AStar is not None and len(shorestPath) < AStar)):
                    nearestWallIntersection = intersection[0]
                    AStar = len(shorestPath)
        
        return nearestWallIntersection
    
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
            self.path = self.getShortestPath(self.seekerPosition, self.goalPosition, self.visitedMatrix)
            self.pathMove = 0
            return
        
        if (self.seekerPosition == self.goalPosition or self.visitedMatrix[self.goalPosition[0]][self.goalPosition[1]]):
            #! Reached the position of the hider -> Stop
            if (self.IdentifiedHider is not None):
                return       
            else:
                self.goalPosition = self.getNearestWallIntersection()
                if (self.goalPosition is not None):
                    self.path = self.getShortestPath(self.seekerPosition, self.goalPosition, self.visitedMatrix)
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
                        self.path = self.getShortestPath(self.seekerPosition, self.goalPosition, self.visitedMatrix)
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