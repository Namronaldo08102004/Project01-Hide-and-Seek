from Source.Level_util import *

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
            self.path = self.getShortestPath(self.seekerPosition, self.goalPosition, self.visitedMatrix)
            self.pathMove = 0
        else:
            self.goalPosition: tuple[int, int] = self.getNearestWallIntersection()
            self.path: list[tuple[int, int]] = self.getShortestPath(self.seekerPosition, self.goalPosition, self.visitedMatrix)
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
                            heappush(listCorrespondingHiders, Hider(correspondingHider, self.seekerPosition, self.map.matrix, self.visitedMatrix))
                        
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
                            heappush(listCorrespondingHiders, Hider(correspondingHider, self.seekerPosition, self.map.matrix, self.visitedMatrix))
                        
                self.listIdentifiedHiders = list(set(self.listIdentifiedHiders).union(set(listCorrespondingHiders)))
        
        #! Observed any hider --> Conduct to touch that hider
        if (len(self.listIdentifiedHiders) != 0 and not checkGoalPositionInListIdentifiedHiders(self.goalPosition, self.listIdentifiedHiders)):
            goal = heappop(self.listIdentifiedHiders)
            self.goalPosition = goal.state
            heappush(self.listIdentifiedHiders, goal)
            self.path = self.getShortestPath(self.seekerPosition, self.goalPosition, self.visitedMatrix)
            self.pathMove = 0
            return
        
        if (self.seekerPosition == self.goalPosition or self.visitedMatrix[self.goalPosition[0]][self.goalPosition[1]]):
            self.visitedMatrix[self.goalPosition[0]][self.goalPosition[1]] = True
            #! Reached the position of the hider
            if (len(self.listIdentifiedHiders) != 0 and checkGoalPositionInListIdentifiedHiders(self.goalPosition, self.listIdentifiedHiders)):
                removeHider = None
                for hider in self.listIdentifiedHiders:
                    if (self.goalPosition == hider.state):
                        removeHider = hider
                        break
                
                self.listIdentifiedHiders.remove(removeHider)
                self.listHiderPositions.remove(self.goalPosition)
                
                if (len(self.listHiderPositions) == 0):
                    return
                
                if (len(self.listIdentifiedHiders) != 0):
                    goal = heappop(self.listIdentifiedHiders)
                    self.goalPosition = goal.state
                    heappush(self.listIdentifiedHiders, goal)
                    self.path = self.getShortestPath(self.seekerPosition, self.goalPosition, self.visitedMatrix)
                    self.pathMove = 0
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
                    
    def level2 (self):
        """
        This function is created for saving all essential things in level 1 for displaying on the game screen
        It will return a list of things, each thing will encompass 5 things:
            + The position of the seeker
            + The list of positions of all hiders
            + The current score of the game
            + The list of cells that the seeker can observe at the current time
            + The announcement that the hider broadcast (It can be None if it does not exist)
        """
        listThingsInLevel2 = []
        listThingsInLevel2.append((self.seekerPosition, self.listHiderPositions, self.score, self.listObservableCells, self.announcementDict))
        yield listThingsInLevel2[-1]
                
        while (True):
            if (self.takeTurn == SEEKER):
                tempListHiderPositions = self.listHiderPositions.copy()
                self.seekerTakeTurn()
                self.takeTurn = HIDER
                if (len(self.listHiderPositions) != 0 and self.seekerPosition not in tempListHiderPositions):
                    self.numSeekerSteps = self.numSeekerSteps + 1
                    self.score = self.score - 1
                    listThingsInLevel2.append((self.seekerPosition, self.listHiderPositions, self.score, self.listObservableCells, self.announcementDict))
                    yield listThingsInLevel2[-1]
                else:
                    self.score = self.score + 20
                    listThingsInLevel2.append((self.seekerPosition, self.listHiderPositions, self.score, self.listObservableCells, self.announcementDict))
                    yield listThingsInLevel2[-1]
                    
                    if (len(self.listHiderPositions) == 0):
                        break

            else:
                for hider in self.listHiderPositions:
                    self.hiderTakeTurn(hider)
                self.takeTurn = SEEKER
                self.numHiderSteps = self.numHiderSteps + 1
                
                if (self.numHiderSteps != 0 and self.numHiderSteps != 1 and 
                    (self.numHiderSteps % 8 == 0 or self.numHiderSteps % 8 == 1)):
                    continue
                else:
                    #! After 2 steps, the announcement disappears
                    if (len(self.announcementDict) != 0):                        
                        self.announcementDict = dict()
        
        return None