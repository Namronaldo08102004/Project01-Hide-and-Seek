from Source.Level_util import *

class Level3 (Level):
    """
        Will be updated later
    """ 
    def __init__ (self, map: Map):
        Level.__init__ (self, map)
        
        #! This matrix is defined just for identifying wall intersections which are visited
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
        listHiderPositions: list[tuple[int, int]] = map.listHiderPositions.copy()
        self.listHiders: list[Hider] = []
        for i in range (0, len(listHiderPositions)):
            self.listHiders.append(Hider(listHiderPositions[i], map = self.map.matrix, id = i))
            self.listHiders[-1].identifiedSeeker = self.listHiders[-1].identifyObservableSeeker(self.seekerPosition)
        
        self.listSeekerObservableCells: list[tuple[int, int]] = self.getObservableCells(self.seekerPosition)
        self.listIdentifiedHiders: list[Hider] = self.identifyObservableHiders()
        
        #? Announcement will be broadcast by hider after each 8 steps and will exist in 2 steps
        """
        We create a dictionary of broadcast announcements
            + Key is the position of a certain announcement
            + Value is the position of the hider who broadcast that announcement 
        """
        self.announcementDict: dict[tuple[int, int], list[tuple[int, int]]] = dict()
        
        #! Get the goal position for the next move of the seeker
        self.seekerGoalPosition: tuple[int, int] = None
        self.seekerPath: list[tuple[int, int]] = None
        self.seekerPathMove: int = 0
        self.gotoIntersection: bool = False
        self.gotoHider: bool = False
        
        if (len(self.listIdentifiedHiders) != 0):
            self.gotoHider = True
        else:
            self.seekerGoalPosition: tuple[int, int] = self.getNearestWallIntersection()
            self.seekerPath: list[tuple[int, int]] = self.getShortestPath(self.seekerPosition, self.seekerGoalPosition)
            self.seekerPathMove: int = 0
            
            self.gotoIntersection = True
        
        """
        The below attribute is used to store the state of the seeker before catching the hider, three elements in the list are:
            + The position of the seeker before catching the hider
            + The position of the seeker in the next move
            + The number of remaining hiders in the map
        """
        self.roadOfSeekerWhenCatchHider: list[tuple[tuple[int, int], tuple[int, int]]] = []
        
        """
        This attribute stores hiders which are permanently ignored by the seeker
        If the number of ignored hiders is equal to the number of hiders currently in the map, the seeker will stop the game
        """
        self.ignoredHiders: list[Hider] = []
        self.giveUp: bool = False
        
        self.isBeingChased: bool = False #! Used for hider while being chased by the seeker
        
    def getNearestWallIntersection (self) -> tuple[int, int]:
        #! Add all unvisited wall intersections to a list
        unvisitedWallIntersections: list[tuple[tuple[int, int], int]] = []
        startPositionForFinding = None
        if (self.seekerGoalPosition is None):
            startPositionForFinding = self.seekerPosition
        else:
            startPositionForFinding = self.seekerGoalPosition
        
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
                shorestPath = self.getShortestPath(startPositionForFinding, nearestWallIntersection)
                AStar = len(shorestPath)
                minHeuristic = intersection[1] - 0.9 * isCorner
            elif (intersection[1] - 0.9 * isCorner == minHeuristic):
                shorestPath = self.getShortestPath(startPositionForFinding, intersection[0])
                if (AStar is None or (AStar is not None and len(shorestPath) < AStar)):
                    nearestWallIntersection = intersection[0]
                    AStar = len(shorestPath)
        
        return nearestWallIntersection
    
    def identifyObservableHiders (self):
        listHiderPositions: list[Hider] = []
        
        for i in range (0, len(self.listSeekerObservableCells)):
            isHider: bool = False
            foundHider = None
            for j in range (0, len(self.listHiders)):
                if (self.listSeekerObservableCells[i] == self.listHiders[j].state):
                    isHider = True
                    foundHider = self.listHiders[j]
                    break
            
            if (isHider):
                listHiderPositions.append(foundHider)
            else:
                self.visitedMatrix[self.listSeekerObservableCells[i][0]][self.listSeekerObservableCells[i][1]] = True
                
        return listHiderPositions
    
    def identifyObservableAnnouncements (self):
        listAnnouncementPositions: list[tuple[int, int]] = []
        
        for i in range (0, len(self.listSeekerObservableCells)):
            if (self.announcementDict.get(self.listSeekerObservableCells[i]) is not None):
                listAnnouncementPositions.append(self.listSeekerObservableCells[i])
            
        return listAnnouncementPositions
    
    def getBestMoveWhenHiderMeetSeeker (self, seekerPosition: tuple[int, int], hider: Hider) -> tuple[int, int]:
        """
        This function helps seeker as well as hider take the best move when they meet each other, using "Nash theory" in Game Theory
        Based on the idea of Nash theory, we will build a table which stores tuples of values
        + If the player is the seeker
            Then each tuple of value will be (x,y), with:
                + x: The length of the shortest path from seeker to hider if the seeker move to a certain cell around it
                + y: The length of the shortest path from hider to seeker if the hider move to a certain cell around it after
                    the seeker has taken their turn before (i.e the movement corresponding the value x)
        + If the player is the hider, the idea of building the table is the same with the above explanation, we just swap the role
        of two players.
        
        We will choose the best move such that:
            + Firstly, in each move of the first taker (can be seeker or hider), we get all of tuples (x,y) with y is the best option for the second taker
            + After taking all the tuples satisfying the above statement, we will choose tuples with x is the best option for the first taker.
            + If there are many tuples satisfying that x is the best option, choose tuples with y is the worst option for the second taker
            + Currently, If there are many tuples satisfying, we obtain the first tuple.
        """
        hiderPosition = hider.state
        
        if (self.takeTurn == SEEKER):
            listSeekerValidNeighbor = getValidNeighbors(seekerPosition, self.map.matrix)
            listHiderValidNeighbor = getValidNeighbors(hiderPosition, self.map.matrix)

            nashTable: list[list[tuple[int, int]]] = []
            for i in range (0, len(listSeekerValidNeighbor)):
                lst = []
                X = len(self.getShortestPath(listSeekerValidNeighbor[i], hiderPosition))
                for j in range (0, len(listHiderValidNeighbor)):
                    Y = len(self.getShortestPath(listHiderValidNeighbor[j], listSeekerValidNeighbor[i]))
                    lst.append((X, Y))
                    
                nashTable.append(lst)
                    
            listTuplesWithBestY = []
            for i in range (0, len(listSeekerValidNeighbor)):
                maxY = -1
                
                for j in range (0, len(listHiderValidNeighbor)):
                    if (nashTable[i][j][1] > maxY):
                        maxY = nashTable[i][j][1]
                        
                for j in range (0, len(listHiderValidNeighbor)):
                    if (nashTable[i][j][1] == maxY):
                        listTuplesWithBestY.append(nashTable[i][j])
                        break
                
            bestNextPosition = None
            minX = self.map.numRows * self.map.numCols
            Y = self.map.numRows * self.map.numCols
            minNumCellsHiderCanRunToNotBeCaught = self.map.numRows * self.map.numCols
            
            for i in range (0, len(listSeekerValidNeighbor)):
                if (listTuplesWithBestY[i][0] < minX):
                    minX = listTuplesWithBestY[i][0]
                    Y = listTuplesWithBestY[i][1]
                    minNumCellsHiderCanRunToNotBeCaught = len(list(set(listHiderValidNeighbor) - (set(getValidNeighbors(listSeekerValidNeighbor[i], self.map.matrix)).union([listSeekerValidNeighbor[i]]))))
                    
                    bestNextPosition = listSeekerValidNeighbor[i]
                elif (listTuplesWithBestY[i][0] == minX and listTuplesWithBestY[i][1] < Y):
                    Y = listTuplesWithBestY[i][1]
                    minNumCellsHiderCanRunToNotBeCaught = len(list(set(listHiderValidNeighbor) - (set(getValidNeighbors(listSeekerValidNeighbor[i], self.map.matrix)).union([listSeekerValidNeighbor[i]]))))
                    
                    bestNextPosition = listSeekerValidNeighbor[i]
                elif (listTuplesWithBestY[i][0] == minX and listTuplesWithBestY[i][1] == Y
                      and len(list(set(listHiderValidNeighbor) - (set(getValidNeighbors(listSeekerValidNeighbor[i], self.map.matrix)).union([listSeekerValidNeighbor[i]])))) 
                      < minNumCellsHiderCanRunToNotBeCaught):
                    minNumCellsHiderCanRunToNotBeCaught = len(list(set(listHiderValidNeighbor) - (set(getValidNeighbors(listSeekerValidNeighbor[i], self.map.matrix)).union([listSeekerValidNeighbor[i]]))))
                    bestNextPosition = listSeekerValidNeighbor[i]
                        
            return bestNextPosition
        
        elif (self.takeTurn == HIDER):
            listHiderValidNeighbor = getValidNeighbors(hiderPosition, self.map.matrix)
            while (True):
                removedNeighbor = None
                
                for neighbor in listHiderValidNeighbor:
                    for Hider in self.listHiders:
                        if (neighbor == Hider.state):
                            removedNeighbor = neighbor
                            break
                            
                    if (removedNeighbor is not None):
                        break
                
                if (removedNeighbor is None):
                    break
                else:
                    listHiderValidNeighbor.remove(removedNeighbor)
                    
            if (len(listHiderValidNeighbor) == 0):
                return hiderPosition
                    
            listHiderValidNeighbor = setOrderOfNeighbor(hiderPosition, getTrendMoveDirection(seekerPosition, hiderPosition), listHiderValidNeighbor)
            listSeekerValidNeighbor = getValidNeighbors(seekerPosition, self.map.matrix)

            nashTable: list[list[tuple[int, int]]] = []
            for i in range (0, len(listHiderValidNeighbor)):
                lst = []
                X = len(self.getShortestPath(listHiderValidNeighbor[i], seekerPosition))
                for j in range (0, len(listSeekerValidNeighbor)):
                    Y = len(self.getShortestPath(listSeekerValidNeighbor[j], listHiderValidNeighbor[i]))
                    lst.append((X, Y))
                    
                nashTable.append(lst)
                    
            listTuplesWithBestY = []
            for i in range (0, len(listHiderValidNeighbor)):
                minY = self.map.numRows * self.map.numCols
                
                for j in range (0, len(listSeekerValidNeighbor)):
                    if (nashTable[i][j][1] < minY):
                        minY = nashTable[i][j][1]
                        
                for j in range (0, len(listSeekerValidNeighbor)):
                    if (nashTable[i][j][1] == minY):
                        listTuplesWithBestY.append(nashTable[i][j])
                        break
                
            bestNextPosition = None
            maxX = -1
            Y = -1
            isIntersection: bool = None
            maxNumCellsExcludeIntersectionsHiderCanMoveToNotBeCaughtInTheNextMove = -1
            maxNumObservableCellsExcludeIntersections = -1
            
            for i in range (0, len(listHiderValidNeighbor)):
                if (listTuplesWithBestY[i][0] > maxX):
                    maxX = listTuplesWithBestY[i][0]
                    Y = listTuplesWithBestY[i][1]
                    
                    if (listHiderValidNeighbor[i] in self.listWallIntersections and len(getValidNeighbors(listHiderValidNeighbor[i], self.map.matrix)) <= 2):
                        isIntersection = True
                    else:
                        isIntersection = False
                    
                    maxNumCellsExcludeIntersectionsHiderCanMoveToNotBeCaughtInTheNextMove = min([len(list((set(getValidNeighbors(listHiderValidNeighbor[i], self.map.matrix)) 
                                                                                      - (set(getValidNeighbors(seekerNeighbor, self.map.matrix)).union([seekerNeighbor]))) - set(self.listWallIntersections)))
                                                                             for seekerNeighbor in listSeekerValidNeighbor])
                    maxNumObservableCellsExcludeIntersections = min([len(list((set(hider.getObservableCellsOfHider(hiderObservableCell))
                                                                          .union(set([listHiderValidNeighbor[i]]))) - set(self.listWallIntersections))) 
                                                                     for hiderObservableCell in list(set(hider.getObservableCellsOfHider(listHiderValidNeighbor[i])).union(set([listHiderValidNeighbor[i]])))])
                    
                    bestNextPosition = listHiderValidNeighbor[i]
                elif (listTuplesWithBestY[i][0] == maxX and listTuplesWithBestY[i][1] > Y):
                    Y = listTuplesWithBestY[i][1]
                    
                    if (listHiderValidNeighbor[i] in self.listWallIntersections and len(getValidNeighbors(listHiderValidNeighbor[i], self.map.matrix)) <= 2):
                        isIntersection = True
                    else:
                        isIntersection = False
                    
                    maxNumCellsExcludeIntersectionsHiderCanMoveToNotBeCaughtInTheNextMove = min([len(list((set(getValidNeighbors(listHiderValidNeighbor[i], self.map.matrix)) 
                                                                                      - (set(getValidNeighbors(seekerNeighbor, self.map.matrix)).union([seekerNeighbor]))) - set(self.listWallIntersections)))
                                                                             for seekerNeighbor in listSeekerValidNeighbor])
                    maxNumObservableCellsExcludeIntersections = min([len(list((set(hider.getObservableCellsOfHider(hiderObservableCell))
                                                                          .union(set([listHiderValidNeighbor[i]]))) - set(self.listWallIntersections))) 
                                                                     for hiderObservableCell in list(set(hider.getObservableCellsOfHider(listHiderValidNeighbor[i])).union(set([listHiderValidNeighbor[i]])))])
                        
                    bestNextPosition = listHiderValidNeighbor[i]
                elif (listTuplesWithBestY[i][0] == maxX and listTuplesWithBestY[i][1] == Y
                      and ((listHiderValidNeighbor[i] not in self.listWallIntersections) or 
                           len(getValidNeighbors(listHiderValidNeighbor[i], self.map.matrix)) >= 3) and isIntersection):
                    isIntersection = False
                    maxNumCellsExcludeIntersectionsHiderCanMoveToNotBeCaughtInTheNextMove = min([len(list((set(getValidNeighbors(listHiderValidNeighbor[i], self.map.matrix)) 
                                                                                      - (set(getValidNeighbors(seekerNeighbor, self.map.matrix)).union([seekerNeighbor]))) - set(self.listWallIntersections)))
                                                                             for seekerNeighbor in listSeekerValidNeighbor])
                    maxNumObservableCellsExcludeIntersections = min([len(list((set(hider.getObservableCellsOfHider(hiderObservableCell))
                                                                          .union(set([listHiderValidNeighbor[i]]))) - set(self.listWallIntersections))) 
                                                                     for hiderObservableCell in list(set(hider.getObservableCellsOfHider(listHiderValidNeighbor[i])).union(set([listHiderValidNeighbor[i]])))])
                        
                    bestNextPosition = listHiderValidNeighbor[i]
                elif (listTuplesWithBestY[i][0] == maxX and listTuplesWithBestY[i][1] == Y 
                      and ((listHiderValidNeighbor[i] not in self.listWallIntersections) or 
                           len(getValidNeighbors(listHiderValidNeighbor[i], self.map.matrix)) >= 3) and not isIntersection
                      and min([len(list((set(getValidNeighbors(listHiderValidNeighbor[i], self.map.matrix)) 
                                         - (set(getValidNeighbors(seekerNeighbor, self.map.matrix)).union([seekerNeighbor]))) - set(self.listWallIntersections)))
                               for seekerNeighbor in listSeekerValidNeighbor]) > maxNumCellsExcludeIntersectionsHiderCanMoveToNotBeCaughtInTheNextMove):
                    maxNumCellsExcludeIntersectionsHiderCanMoveToNotBeCaughtInTheNextMove = min([len(list((set(getValidNeighbors(listHiderValidNeighbor[i], self.map.matrix)) 
                                                                                      - (set(getValidNeighbors(seekerNeighbor, self.map.matrix)).union([seekerNeighbor]))) - set(self.listWallIntersections)))
                                                                             for seekerNeighbor in listSeekerValidNeighbor])
                    maxNumObservableCellsExcludeIntersections = min([len(list((set(hider.getObservableCellsOfHider(hiderObservableCell))
                                                                          .union(set([listHiderValidNeighbor[i]]))) - set(self.listWallIntersections))) 
                                                                     for hiderObservableCell in list(set(hider.getObservableCellsOfHider(listHiderValidNeighbor[i])).union(set([listHiderValidNeighbor[i]])))])
                        
                    bestNextPosition = listHiderValidNeighbor[i]
                elif (listTuplesWithBestY[i][0] == maxX and listTuplesWithBestY[i][1] == Y
                      and ((listHiderValidNeighbor[i] not in self.listWallIntersections) or 
                           len(getValidNeighbors(listHiderValidNeighbor[i], self.map.matrix)) >= 3) and not isIntersection
                      and min([len(list((set(getValidNeighbors(listHiderValidNeighbor[i], self.map.matrix)) 
                                         - (set(getValidNeighbors(seekerNeighbor, self.map.matrix)).union([seekerNeighbor]))) - set(self.listWallIntersections)))
                               for seekerNeighbor in listSeekerValidNeighbor]) == maxNumCellsExcludeIntersectionsHiderCanMoveToNotBeCaughtInTheNextMove
                      and min([len(list((set(hider.getObservableCellsOfHider(hiderObservableCell))
                                         .union(set([listHiderValidNeighbor[i]]))) - set(self.listWallIntersections))) 
                               for hiderObservableCell in list(set(hider.getObservableCellsOfHider(listHiderValidNeighbor[i])).union(set([listHiderValidNeighbor[i]])))])
                      > maxNumObservableCellsExcludeIntersections):
                    
                    maxNumObservableCellsExcludeIntersections = min([len(list((set(hider.getObservableCellsOfHider(hiderObservableCell))
                                                                          .union(set([listHiderValidNeighbor[i]]))) - set(self.listWallIntersections))) 
                                                                     for hiderObservableCell in list(set(hider.getObservableCellsOfHider(listHiderValidNeighbor[i])).union(set([listHiderValidNeighbor[i]])))])
                    
                    bestNextPosition = listHiderValidNeighbor[i]
                        
            return bestNextPosition
    
    def seekerTakeTurn (self):
        def checkGoalPositionInListIdentifiedHiders (goalPosition: tuple[int, int], listIdentifiedHiders: list[Hider]):
            for hider in listIdentifiedHiders:
                if goalPosition == hider.state:
                    return True
            
            return False
        
        def union (list1: list[Hider], list2: list[Hider]) -> list[Hider]:
            for cell in list2:
                if cell not in list1:
                    list1.append(cell)
                    
            return list1
        
        def diff (list1: list[Hider], list2: list[Hider]) -> list[Hider]:
            for cell in list2:
                if cell in list1:
                    list1.remove(cell)
                    
            return list1
        
        if (len(self.ignoredHiders) == len(self.listHiders)):
            self.giveUp = True
            return
        
        if (self.gotoIntersection):
            self.seekerPosition = self.seekerPath[self.seekerPathMove]
            self.seekerPathMove = self.seekerPathMove + 1
            self.listSeekerObservableCells = self.getObservableCells(self.seekerPosition)
            
            self.listIdentifiedHiders = self.identifyObservableHiders()
            listIdentifiedAnnouncements = self.identifyObservableAnnouncements()
            
            if (listIdentifiedAnnouncements):
                listCorrespondingHiders: list[Hider] = []
                for announcement in listIdentifiedAnnouncements:
                    correspondingHiders = self.announcementDict[announcement]
                    
                    for correspondingHider in correspondingHiders:
                        if (correspondingHider != self.seekerGoalPosition):
                        #! At this time, self.seekerGoalPosition is a position where a certain hider is standing
                            for hider in self.listHiders:
                                if (correspondingHider == hider.state and hider not in self.ignoredHiders):
                                    listCorrespondingHiders.append(hider)
                                    break
                        
                self.listIdentifiedHiders = union(self.listIdentifiedHiders, listCorrespondingHiders)
            self.listIdentifiedHiders = diff(self.listIdentifiedHiders, self.ignoredHiders)
            
            #! Observed any hider --> Conduct to touch that hider
            if (len(self.listIdentifiedHiders) != 0 and not checkGoalPositionInListIdentifiedHiders(self.seekerGoalPosition, self.listIdentifiedHiders)):
                self.gotoHider = True
                self.gotoIntersection = False
                return
            
        elif (self.gotoHider):
            if (len(self.listIdentifiedHiders) != 0):
                goal = self.listIdentifiedHiders[0]
                hiderPosition = goal.state
                
                NextMove = self.getBestMoveWhenHiderMeetSeeker(self.seekerPosition, goal)
                if ((self.seekerPosition, NextMove) not in self.roadOfSeekerWhenCatchHider):
                    self.roadOfSeekerWhenCatchHider.append((self.seekerPosition, NextMove))
                    
                    self.seekerPosition = NextMove
                    self.seekerGoalPosition = hiderPosition
                    self.listSeekerObservableCells = self.getObservableCells(self.seekerPosition)
                    
                    tempListIdentifiedHiders = self.identifyObservableHiders()
                    listIdentifiedAnnouncements = self.identifyObservableAnnouncements()
                    
                    if (listIdentifiedAnnouncements):
                        listCorrespondingHiders: list[Hider] = []
                        for announcement in listIdentifiedAnnouncements:
                            correspondingHiders = self.announcementDict[announcement]
                            
                            for correspondingHider in correspondingHiders:
                                if (correspondingHider != self.seekerGoalPosition): 
                                #! At this time, self.seekerGoalPosition is a position where a certain hider is standing
                                    for hider in self.listHiders:
                                        if (correspondingHider == hider.state and hider not in self.ignoredHiders):
                                            listCorrespondingHiders.append(hider)
                                            break
                                
                        self.listIdentifiedHiders = union(self.listIdentifiedHiders, listCorrespondingHiders)
                        self.listIdentifiedHiders = diff(self.listIdentifiedHiders, self.ignoredHiders)
                    
                    #! Get the union of the old list of identified hiders and the new one
                    self.listIdentifiedHiders = union(self.listIdentifiedHiders, tempListIdentifiedHiders)
                    self.listIdentifiedHiders = diff(self.listIdentifiedHiders, self.ignoredHiders)
                    
                    if (self.seekerPosition != self.seekerGoalPosition):
                        return
                
                #! The seeker realized that it cannot catch this hider
                else:
                    self.roadOfSeekerWhenCatchHider = []
                    
                    #! Remove the hider from the list of identified hiders
                    removeHider = None
                    for hider in self.listIdentifiedHiders:
                        if (hiderPosition == hider.state):
                            removeHider = hider
                            break
                    
                    self.listIdentifiedHiders.remove(removeHider)
                    self.ignoredHiders.append(removeHider)
                    
                    self.seekerGoalPosition = self.getNearestWallIntersection()
                    if (self.seekerGoalPosition is not None):
                        self.seekerPath = self.getShortestPath(self.seekerPosition, self.seekerGoalPosition)
                        self.seekerPathMove = 0
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
                                                self.seekerGoalPosition = (row, col)
                                                found = True
                                                break
                                
                                if (found):
                                    break
                            
                            if (found):
                                break
                    
                            level = level + 1
                            
                        if (self.seekerGoalPosition is not None):
                            self.seekerPath = self.getShortestPath(self.seekerPosition, self.seekerGoalPosition, self.visitedMatrix)
                            self.seekerPathMove = 0
                        else:
                            raise Exception ("Your map is missing the hider")
                        
                    self.gotoIntersection = True
                    self.gotoHider = False
                    return
            
            else:
                self.seekerGoalPosition = self.getNearestWallIntersection()
                if (self.seekerGoalPosition is not None):
                    self.seekerPath = self.getShortestPath(self.seekerPosition, self.seekerGoalPosition)
                    self.seekerPathMove = 0
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
                                            self.seekerGoalPosition = (row, col)
                                            found = True
                                            break
                            
                            if (found):
                                break
                        
                        if (found):
                            break
                
                        level = level + 1
                        
                    if (self.seekerGoalPosition is not None):
                        self.seekerPath = self.getShortestPath(self.seekerPosition, self.seekerGoalPosition, self.visitedMatrix)
                        self.seekerPathMove = 0
                    else:
                        raise Exception ("Your map is missing the hider")
                    
                self.gotoIntersection = True
                self.gotoHider = False
                return

        checkNoHider: bool = True
        if (self.seekerGoalPosition in self.listSeekerObservableCells):
            for cell in self.listSeekerObservableCells:
                if (len(self.listIdentifiedHiders) != 0 and checkGoalPositionInListIdentifiedHiders(cell, self.listIdentifiedHiders)):
                    checkNoHider = False
                    break
        else:
            checkNoHider = False
        
        if (self.seekerPosition == self.seekerGoalPosition or checkNoHider):
            #! Reached the position of the hider
            if (len(self.listIdentifiedHiders) != 0 and checkGoalPositionInListIdentifiedHiders(self.seekerGoalPosition, self.listIdentifiedHiders)):
                removeHider = None
                for hider in self.listIdentifiedHiders:
                    if (self.seekerGoalPosition == hider.state):
                        removeHider = hider
                        break
                
                self.listIdentifiedHiders.remove(removeHider)
                
                removeHider = None
                for hider in self.listHiders:
                    if (self.seekerGoalPosition == hider.state):
                        removeHider = hider
                        break
                    
                self.listHiders.remove(removeHider)
                
                self.roadOfSeekerWhenCatchHider = []
                
                if (len(self.listHiders) == 0):
                    return
                
                if (len(self.listIdentifiedHiders) != 0):
                    self.gotoIntersection = False
                    self.gotoHider = True
                    return
                else:
                    self.seekerGoalPosition = self.getNearestWallIntersection()
                    if (self.seekerGoalPosition is not None):
                        self.seekerPath = self.getShortestPath(self.seekerPosition, self.seekerGoalPosition)
                        self.seekerPathMove = 0
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
                                                self.seekerGoalPosition = (row, col)
                                                found = True
                                                break
                                
                                if (found):
                                    break
                            
                            if (found):
                                break
                    
                            level = level + 1
                            
                        if (self.seekerGoalPosition is not None):
                            self.seekerPath = self.getShortestPath(self.seekerPosition, self.seekerGoalPosition, self.visitedMatrix)
                            self.seekerPathMove = 0
                        else:
                            raise Exception ("Your map is missing the hider")
                    
                    self.gotoIntersection = True
                    self.gotoHider = False
                            
            else:
                self.visitedMatrix[self.seekerGoalPosition[0]][self.seekerGoalPosition[1]] = True
                self.seekerGoalPosition = self.getNearestWallIntersection()
                if (self.seekerGoalPosition is not None):
                    self.seekerPath = self.getShortestPath(self.seekerPosition, self.seekerGoalPosition)
                    self.seekerPathMove = 0
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
                                            self.seekerGoalPosition = (row, col)
                                            found = True
                                            break
                            
                            if (found):
                                break
                        
                        if (found):
                            break
                
                        level = level + 1
                        
                    if (self.seekerGoalPosition is not None):
                        self.seekerPath = self.getShortestPath(self.seekerPosition, self.seekerGoalPosition, self.visitedMatrix)
                        self.seekerPathMove = 0
                    else:
                        raise Exception ("Your map is missing the hider")
                
                self.gotoIntersection = True
                self.gotoHider = False
    
    def hiderTakeTurn (self, hider: Hider):
        announcementBroadcastByHider = None
        if (len(self.announcementDict) != 0):
            for announcement in self.announcementDict:
                if (hider.state in self.announcementDict[announcement]):
                    announcementBroadcastByHider = announcement
                    break
        
        tempIdentifiedSeeker = hider.identifiedSeeker        
        hider.identifiedSeeker = hider.identifyObservableSeeker(self.seekerPosition)
        if (tempIdentifiedSeeker is not None or hider.identifiedSeeker is not None or self.isBeingChased):
            if (hider.identifiedSeeker is not None):
                bestPosition = self.getBestMoveWhenHiderMeetSeeker(hider.identifiedSeeker, hider)
            elif (tempIdentifiedSeeker is not None):
                bestPosition = self.getBestMoveWhenHiderMeetSeeker(tempIdentifiedSeeker, hider)
            else:
                self.isBeingChased = False
                return
            
            if (announcementBroadcastByHider is not None):
                self.announcementDict[announcementBroadcastByHider].remove(hider.state)
                self.announcementDict[announcementBroadcastByHider].append(bestPosition)
                
            hider.state = bestPosition
            
            if (hider.identifiedSeeker is not None and hider.state == hider.identifiedSeeker):
                self.listIdentifiedHiders.remove(hider)
                self.listHiders.remove(hider)
                return
            else:
                hider.hiderObservableCells = hider.getObservableCellsOfHider(hider.state)
                
            self.isBeingChased = True
        else:
            NextPosition: tuple[int, int] = hider.state
            maxNumObservableCells = len(hider.hiderObservableCells)
            listValidNeighbors = getValidNeighbors(hider.state, self.map.matrix)
            
            while (True):
                removedNeighbor = None
                
                for neighbor in listValidNeighbors:
                    for Hider in self.listHiders:
                        if (neighbor == Hider.state):
                            removedNeighbor = neighbor
                            break
                            
                    if (removedNeighbor is not None):
                        break
                
                if (removedNeighbor is None):
                    break
                else:
                    listValidNeighbors.remove(removedNeighbor)
            
            for cell in listValidNeighbors:
                observable = hider.getObservableCellsOfHider(cell)
                if (len(observable) > maxNumObservableCells):
                    maxNumObservableCells = len(observable)
                    NextPosition = cell
                    
            if (hider.state != NextPosition):
                if (announcementBroadcastByHider is not None):
                    self.announcementDict[announcementBroadcastByHider].remove(hider.state)
                    self.announcementDict[announcementBroadcastByHider].append(NextPosition)
                    
                hider.state = NextPosition
                hider.hiderObservableCells = hider.getObservableCellsOfHider(hider.state)
                
            hider.identifiedSeeker = hider.identifyObservableSeeker(self.seekerPosition)
                
        if (self.numHiderSteps % 8 == 7):
            #! The hider will broadcast an announcement after each 8 steps and set the time for this announcement
            announcement = self.broadcastAnnouncement(hider.state)
            if (self.announcementDict.get(announcement) is None):
                self.announcementDict[announcement] = [hider.state]
            else:
                self.announcementDict[announcement].append(hider.state)
                
    def level3 (self):
        """
        This function is created for saving all essential things in level 1 for displaying on the game screen
        It will return a list of things, each thing will encompass 5 things:
            + The position of the seeker
            + The list of positions of all hiders
            + The current score of the game
            + The list of cells that the seeker can observe at the current time
            + With each hider, the list of cells that the hider can observe at the current time
            + The announcement that the hider broadcast (It can be None if it does not exist)
            + Give Up or not
        """
        listThingsInLevel3 = []
        listThingsInLevel3.append((self.seekerPosition, self.listHiders, self.score, self.listSeekerObservableCells, self.announcementDict, self.giveUp))
        yield listThingsInLevel3[-1]
                
        while (not self.giveUp):
            prevNumHiders = len(self.listHiders)
                
            if (self.takeTurn == SEEKER):
                self.seekerTakeTurn()
                
                self.takeTurn = HIDER
                if (len(self.listHiders) != 0 and len(self.listHiders) == prevNumHiders):
                    self.numSeekerSteps = self.numSeekerSteps + 1
                    self.score = self.score - 1
                    listThingsInLevel3.append((self.seekerPosition, self.listHiders, self.score, self.listSeekerObservableCells, self.announcementDict, self.giveUp))
                    yield listThingsInLevel3[-1]
                else:
                    self.score = self.score + 20
                    listThingsInLevel3.append((self.seekerPosition, self.listHiders, self.score, self.listSeekerObservableCells, self.announcementDict, self.giveUp))
                    yield listThingsInLevel3[-1]
                    
                    if (len(self.listHiders) == 0):
                        break

            else:   
                for hider in self.listHiders:
                    self.hiderTakeTurn(hider)
                self.takeTurn = SEEKER
                self.numHiderSteps = self.numHiderSteps + 1
                
                if (not (self.numHiderSteps != 0 and self.numHiderSteps != 1 and 
                    (self.numHiderSteps % 8 == 0 or self.numHiderSteps % 8 == 1))):
                    #! After 2 steps, the announcement disappears
                    if (len(self.announcementDict) != 0):
                        self.announcementDict = dict()
                        
                if (len(self.listHiders) == 0 or len(self.listHiders) != prevNumHiders):
                    self.score = self.score + 20
                    listThingsInLevel3.append((self.seekerPosition, self.listHiders, self.score, self.listSeekerObservableCells, self.announcementDict, self.giveUp))
                    yield listThingsInLevel3[-1]
                    
                    if (len(self.listHiders) == 0):
                        break
                else:
                    listThingsInLevel3.append((self.seekerPosition, self.listHiders, self.score, self.listSeekerObservableCells, self.announcementDict, self.giveUp))
                    yield listThingsInLevel3[-1]
                
        if (self.giveUp):
            listThingsInLevel3.append((self.seekerPosition, self.listHiders, self.score, self.listSeekerObservableCells, self.announcementDict, self.giveUp))
            yield listThingsInLevel3[-1]
        
        return None