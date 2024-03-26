from Level_util import *

class Level3 (Level):
    """
        Will be updated later
    """ 
    def __init__ (self, map: Map):
        Level.__init__ (self, map)
        
        #! Define seeker and hiders for the game
        self.seekerPosition: tuple[int, int] = map.seekerPosition
        listHiderPositions: list[tuple[int, int]] = map.listHiderPositions.copy()
        self.listHiders: list[Hider] = []
        for position in listHiderPositions:
            self.listHiders.append(Hider(position, map = self.map.matrix))
        
        self.listSeekerObservableCells: list[tuple[int, int]] = self.getObservableCells(self.seekerPosition)
        self.listIdentifiedHiders: list[Hider] = self.identifyObservableHiders()
        
        #? Announcement will be broadcast by hider after each 8 steps and will exist in 2 steps
        """
        We create a dictionary of broadcast announcements
            + Key is the position of a certain announcement
            + Value is the position of the hider who broadcast that announcement 
        """
        self.announcementDict: dict[tuple[int, int], list[tuple[int, int]]] = dict()
            
    def hiderTakeTurn (self, hiderPosition: tuple[int, int]):
        pass
            
    def getShortestPath (self, startPosition: tuple[int, int], goalPosition: tuple[int, int]) -> list[tuple[int, int]]:
        #! Be sure that the path will be from the next step of the start position to the goal position
        goal = A_Star(startPosition, goalPosition, self.map.matrix)
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
                heappush(listHiderPositions, Hider(self.listObservableCells[i], self.seekerPosition, self.map.matrix))
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
            self.path = self.getShortestPath(self.seekerPosition, self.goalPosition)
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
                    self.path = self.getShortestPath(self.seekerPosition, self.goalPosition)
                    self.pathMove = 0
                else:
                    self.goalPosition = self.getNearestWallIntersection()
                    if (self.goalPosition is not None):
                        self.path = self.getShortestPath(self.seekerPosition, self.goalPosition)
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
                            self.path = self.getShortestPath(self.seekerPosition, self.goalPosition)
                            self.pathMove = 0
                        else:
                            raise Exception ("Your map is missing the hider")
                             
            else:
                self.goalPosition = self.getNearestWallIntersection()
                if (self.goalPosition is not None):
                    self.path = self.getShortestPath(self.seekerPosition, self.goalPosition)
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
                        self.path = self.getShortestPath(self.seekerPosition, self.goalPosition)
                        self.pathMove = 0
                    else:
                        raise Exception ("Your map is missing the hider")