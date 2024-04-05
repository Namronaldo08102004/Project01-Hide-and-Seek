from AI.Level_util import *

class Level1 (Level):
    """
        Our strategy for level 1 is sequentialy finding the nearest wall intersection from the current position in the map.
        When reached a certain wall intersection:
            + If there is not hider around this wall position, we will move to the next nearest wall intersection.
            + If there is hider, conduct to touch that hider.
        Through the process of moving among other wall intersections, we keep a matrix for checking visited cells which are
        identified to not include hider, and we hope that we can find the only hider through the process
        
        On this strategy, we optimize the process of finding the nearest wall intersection by building
        a heuristic function to estimate the distance from the current position to the wall intersection, based on two elements:
            + The number of walls between the current position and the wall intersection (on Bresenham lines and Manhattan lines)
            + Whether the wall intersection is a corner or not.
        If two wall intersections have the same heuristic value, we will choose the wall intersection which has the shorter path
        
        Besides, to optimize the score of game, instead of moving to the cell which are identified the nearest wall intersection,
        if that cell is in observable cells of the seeker and it does not include the hider, we will move to the next nearest wall intersection
        
        On the road to move among wall intersections, if the seeker can observe the hider or the announcement,
        it will conduct to touch the hider
        
        If there is not any hiders found, we will check unvisited cells and move sequentially to each cell in the order from nearest
        to furtherest.
    """ 
    def __init__ (self, map: Map):
        Level.__init__ (self, map)
        
        self.giveUp: bool = False #! This attribute is True when the seeker realizes that it cannot find the hider (there is no ways to go to remaining hiders)
        
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
                if (self.map.matrix[row][col] in [WALL, OBSTACLE] and (row + 1 < self.map.numRows and self.map.matrix[row + 1][col] in [WALL, OBSTACLE])
                    and (col + 1 < self.map.numCols and self.map.matrix[row][col + 1] in [WALL, OBSTACLE])):
                    if (self.map.matrix[row + 1][col + 1] not in [WALL, OBSTACLE]):
                        self.listWallIntersections.append((row + 1, col + 1))
                
                if (self.map.matrix[row][col] in [WALL, OBSTACLE] and (row + 1 < self.map.numRows and self.map.matrix[row + 1][col] in [WALL, OBSTACLE])
                    and (col - 1 >= 0 and self.map.matrix[row][col - 1] in [WALL, OBSTACLE])):
                    if (self.map.matrix[row + 1][col - 1] not in [WALL, OBSTACLE]):
                        self.listWallIntersections.append((row + 1, col - 1))
                
                if (self.map.matrix[row][col] in [WALL, OBSTACLE] and (row - 1 >= 0 and self.map.matrix[row - 1][col] in [WALL, OBSTACLE])
                    and (col - 1 >= 0 and self.map.matrix[row][col - 1] in [WALL, OBSTACLE])):
                    if (self.map.matrix[row - 1][col - 1] not in [WALL, OBSTACLE]):
                        self.listWallIntersections.append((row - 1, col - 1))
                
                if (self.map.matrix[row][col] in [WALL, OBSTACLE] and (row - 1 >= 0 and self.map.matrix[row - 1][col] in [WALL, OBSTACLE])
                    and (col + 1 < self.map.numCols and self.map.matrix[row][col + 1] in [WALL, OBSTACLE])):
                    if (self.map.matrix[row - 1][col + 1] not in [WALL, OBSTACLE]):
                        self.listWallIntersections.append((row - 1, col + 1))
                    
                if ((row, col) == (0, self.map.numCols - 1) or (row, col) == (0, 0)
                    or (row, col) == (self.map.numRows - 1, self.map.numCols - 1)
                    or (row, col) == (self.map.numRows - 1, 0)):
                    if (self.map.matrix[row][col] not in [WALL, OBSTACLE]):
                        self.listWallIntersections.append((row, col))
                
                if ((col == self.map.numCols - 1 or col == 0) and self.map.matrix[row][col] in [WALL, OBSTACLE]):
                    if (row - 1 >= 0 and self.map.matrix[row - 1][col] not in [WALL, OBSTACLE]):
                        self.listWallIntersections.append((row - 1, col))

                    if (row + 1 < self.map.numRows and self.map.matrix[row + 1][col] not in [WALL, OBSTACLE]):
                        self.listWallIntersections.append((row + 1, col))
                
                if ((row == self.map.numRows - 1 or row == 0) and self.map.matrix[row][col] in [WALL, OBSTACLE]):
                    if (col - 1 >= 0 and self.map.matrix[row][col - 1] not in [WALL, OBSTACLE]):
                        self.listWallIntersections.append((row, col - 1))

                    if (col + 1 < self.map.numCols and self.map.matrix[row][col + 1] not in [WALL, OBSTACLE]):
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
            
            if (self.path is None):
                self.giveUp = True
            else:
                self.pathMove = 0
                
        elif (self.IdentifiedHider is None and self.IdentifiedAnnouncement is not None):
            self.goalPosition = self.IdentifiedAnnouncement
            self.path = self.getShortestPath(self.seekerPosition, self.goalPosition, self.visitedMatrix)
            
            if (self.path is None):
                self.giveUp = True
            else:
                self.pathMove = 0
                
        else:
            self.goalPosition: tuple[int, int] = self.getNearestWallIntersection()
            self.path: list[tuple[int, int]] = self.getShortestPath(self.seekerPosition, self.goalPosition, self.visitedMatrix)
            self.pathMove: int = 0
            
    def hiderTakeTurn (self):
        """
        This function is created for the hider to take a turn in the game
        Our convention for the hider is that it will broadcast an announcement after each 8 steps
        An announcement will exist in 2 steps and then disappear
        """
        if (self.numHiderSteps % 8 != 7):
            return
        
        #! The hider will broadcast an announcement after each 8 steps and set the time for this announcement
        self.announcement = self.broadcastAnnouncement(self.hiderPosition)
        self.announcementTime = 0
    
    def getNearestWallIntersection (self) -> tuple[int, int]:
        """
        This function is created for finding the nearest wall intersection from a start position, which can be the seeker position or the old wall intersection
        """
        
        #! Identify the start position for finding the nearest wall intersection
        startPositionForFinding = None
        if (self.goalPosition is None):
            startPositionForFinding = self.seekerPosition
        else:
            startPositionForFinding = self.goalPosition
        
        #! Add all unvisited wall intersections to a list, coming with the minimum number of walls between the start position and the wall intersection
        unvisitedWallIntersections: list[tuple[tuple[int, int], int]] = []
        for intersection in self.listWallIntersections:
            if (not self.visitedMatrix[intersection[0]][intersection[1]]):
                listObservableCells = self.getObservableCells(intersection)
                
                numWalls = self.countNumWallsBetweenTwoPositions(startPositionForFinding, intersection)
                for cell in listObservableCells:
                    numWalls = min(self.countNumWallsBetweenTwoPositions(startPositionForFinding, cell), numWalls)
                unvisitedWallIntersections.append((intersection, numWalls))
        
        #! Find the nearest wall intersection
        """
        Our heuristic function is: h = d - 0.9 * isCorner
        with d is the distance from the start position to the wall intersection
        and isCorner is 1 if the wall intersection is a corner, otherwise, it is 0
        
        0.9 can be replaced by another value, which is less than 1, because:
            + We can prioritize the wall intersections which are corners if the value d of two wall intersections is the same
            + 0.9 or any value less than 1 can reduce the ambiguity of the equal heuristic values
        
        We will choose the wall intersection which has the minimum heuristic value
        If two wall intersections have the same heuristic value, we will choose the wall intersection which has the shorter path
        
        If an intersection was identified, but there is no paths to go to that intersection, we will ignore that intersection
        If there is not any wall intersection, we will return None
        """        
        nearestWallIntersection: tuple[int, int] = None
        minHeuristic = 1000000000
        AStar = None
        for intersection in unvisitedWallIntersections:
            isCorner = self.checkCorner(intersection[0])
            if (intersection[1] - 0.9 * isCorner < minHeuristic):
                shortestPath = self.getShortestPath(startPositionForFinding, intersection[0], self.visitedMatrix)
                if (shortestPath is not None): #? If the seeker can reach the wall intersection
                    nearestWallIntersection = intersection[0]
                    AStar = len(shortestPath)
                    minHeuristic = intersection[1] - 0.9 * isCorner
            elif (intersection[1] - 0.9 * isCorner == minHeuristic):
                shortestPath = self.getShortestPath(startPositionForFinding, intersection[0], self.visitedMatrix)
                if (shortestPath is not None and (AStar is None or (AStar is not None and len(shortestPath) < AStar))):
                    nearestWallIntersection = intersection[0]
                    AStar = len(shortestPath)
        
        return nearestWallIntersection
    
    def identifyObservableHider (self):
        """
        This function is created for identifying the hider in the observable cells of the seeker
        If a cell is identified not including the hider, we will set the value of the cell in the visited matrix to True
        """
        
        Position: tuple[int, int] = None
        
        for i in range (0, len(self.listObservableCells)):
            if (self.map.matrix[self.listObservableCells[i][0]][self.listObservableCells[i][1]] == HIDER):
                Position = self.listObservableCells[i]
            else:
                self.visitedMatrix[self.listObservableCells[i][0]][self.listObservableCells[i][1]] = True
                
        return Position
    
    def identifyObservableAnnouncement (self):
        """
        This function is created for identifying the announcement in the observable cells of the seeker
        """
        
        for i in range (0, len(self.listObservableCells)):
            if (self.announcement is not None and self.listObservableCells[i] == self.announcement):
                return self.listObservableCells[i]
            
        return None
    
    def seekerTakeTurn (self):
        """
        This function is created for the seeker to take a turn in the game
        """
        
        #! Move to the next position in the path and update the list of observable cells
        self.seekerPosition = self.path[self.pathMove]
        self.pathMove = self.pathMove + 1
        self.listObservableCells = self.getObservableCells(self.seekerPosition)
        
        #! If the seeker is in the process of chasing the hider, the program will not update any new information
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
            
            #! The path can be None if it does not exist, meaning that the seeker cannot reach the hider
            if (self.path is None):
                self.giveUp = True #! Then the seeker will give up
            else:    
                self.pathMove = 0
                
            return
        
        if (self.seekerPosition == self.goalPosition or self.visitedMatrix[self.goalPosition[0]][self.goalPosition[1]]):
            #! Reached the position of the hider -> Stop
            if (self.IdentifiedHider is not None):
                return       
            else:
                #! Reached the wall intersection -> Find the next wall intersection
                self.goalPosition = self.getNearestWallIntersection()
                if (self.goalPosition is not None):
                    self.path = self.getShortestPath(self.seekerPosition, self.goalPosition, self.visitedMatrix)
                    self.pathMove = 0
                #! There is not any wall intersection -> Find the nearest unvisited cell
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
                                            self.path = self.getShortestPath(self.seekerPosition, self.goalPosition, self.visitedMatrix)
                                            
                                            if (self.path is not None):
                                                self.pathMove = 0
                                                found = True
                                                break
                            
                            if (found):
                                break
                        
                        if (found):
                            break
                
                        level = level + 1
                    
                    #! There is not any unvisited cell or there does not exist any paths to go to the unvisited cell -> Give up  
                    if (not found):
                        self.giveUp = True
                        return
                    
    def level1 (self):
        """
        This function is created for saving all essential things in level 1 for displaying on the game screen
        It will return a list of things, each thing will encompass 5 things:
            + The position of the seeker
            + The position of the hider
            + The current score of the game
            + The list of cells that the seeker can observe at the current time
            + The announcement that the hider broadcast (It can be None if it does not exist)
            + Give Up or not
        """
        listThingsInLevel1 = []
        listThingsInLevel1.append((self.seekerPosition, self.hiderPosition, self.score, self.listObservableCells, self.announcement, self.giveUp))
        yield listThingsInLevel1[-1]
                
        while (not self.giveUp):
            if (self.takeTurn == SEEKER):
                self.seekerTakeTurn()
                self.takeTurn = HIDER
                if (self.seekerPosition != self.hiderPosition):
                    self.numSeekerSteps = self.numSeekerSteps + 1
                    self.score = self.score - 1
                    listThingsInLevel1.append((self.seekerPosition, self.hiderPosition, self.score, self.listObservableCells, self.announcement, self.giveUp))
                    yield listThingsInLevel1[-1]
                else:
                    self.score = self.score + 20
                    listThingsInLevel1.append((self.seekerPosition, self.hiderPosition, self.score, self.listObservableCells, self.announcement, self.giveUp))
                    yield listThingsInLevel1[-1]
                    break
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
                
        if (self.giveUp):
            listThingsInLevel1.append((self.seekerPosition, self.hiderPosition, self.score, self.listObservableCells, self.announcement, self.giveUp))
            yield listThingsInLevel1[-1]
        
        return None