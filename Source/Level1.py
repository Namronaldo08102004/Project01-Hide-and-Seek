from Map import *
from random import choice
from A_Star import *
    
#TODO: Remember to fix the INDEX_ERROR
#TODO: Remember to eliminate the cur position in the loop "for" of level
#TODO: Everything can be None
class WallIntersection:
    def __init__ (self, state: tuple[int, int], seekerPosition: tuple[int, int], map, visitedMatrix):
        self.state = state
        self.seekerPosition = seekerPosition
        self.map = map
        self.visitedMatrix = visitedMatrix
        
        X1 = seekerPosition[1]
        X2 = self.state[1]
        Y1 = seekerPosition[0]
        Y2 = self.state[0]
        
        #! Calculate the number of walls in the shortest path (without any walls in the map) from the current seeker position to this wall intersection
        self.numWallIntersectionsBetweenThem = 0
        if (X2 <= X1 and Y1 >= Y2):
            if (Y1 - Y2 > X1 - X2):
                for j in range (0, X1 - X2 + 1):
                    if (self.map[Y1 - j][X1 - j] == WALL):
                        self.numWallIntersectionsBetweenThem += 1
                for j in range (1, (Y1 - Y2) - (X1 - X2) + 1):
                    if (self.map[Y1 - (X1 - X2) - j][X2] == WALL):
                        self.numWallIntersectionsBetweenThem += 1
            else:
                for j in range (0, (X1 - X2) - (Y1 - Y2) + 1):
                    if (self.map[Y1][X1 - j] == WALL):
                        self.numWallIntersectionsBetweenThem += 1
                for j in range (1, Y1 - Y2 + 1):
                    if (self.map[Y1 - j][X2 + Y1 - Y2 - j] == WALL):
                        self.numWallIntersectionsBetweenThem += 1
            
        elif (X2 >= X1 and Y1 >= Y2):
            if (Y1 - Y2 > X2 - X1):
                for j in range (0, (Y1 - Y2) - (X2 - X1) + 1):
                    if (self.map[Y1 - j][X1] == WALL):
                        self.numWallIntersectionsBetweenThem += 1
                for j in range (1, X2 - X1 + 1):
                    if (self.map[Y2 + (X2 - X1) - j][X1 + j] == WALL):
                        self.numWallIntersectionsBetweenThem += 1
            else:
                for j in range (0, Y1 - Y2 + 1):
                    if (self.map[Y1 - j][X1 + j] == WALL):
                        self.numWallIntersectionsBetweenThem += 1
                for j in range (1, X2 - X1 - (Y1 - Y2) + 1):
                    if (self.map[Y2][X1 + Y1 - Y2 + j] == WALL):
                        self.numWallIntersectionsBetweenThem += 1
                    
        elif (X2 >= X1 and Y2 >= Y1):
            if (Y2 - Y1 > X2 - X1):
                for j in range (0, X2 - X1 + 1):
                    if (self.map[Y1 + j][X1 + j] == WALL):
                        self.numWallIntersectionsBetweenThem += 1
                for j in range (1, Y2 - Y1 - (X2 - X1) + 1):
                    if (self.map[Y1 + (X2 - X1) + j][X2] == WALL):
                        self.numWallIntersectionsBetweenThem += 1
            else:
                for j in range (0, (X2 - X1) - (Y2 - Y1) + 1):
                    if (self.map[Y1][X1 + j] == WALL):
                        self.numWallIntersectionsBetweenThem += 1
                for j in range (1, Y2 - Y1 + 1):
                    if (self.map[Y1 + j][X2 - (Y2 - Y1) + j] == WALL):
                        self.numWallIntersectionsBetweenThem += 1
                    
        elif (X1 >= X2 and Y2 >= Y1):
            if (Y2 - Y1 > X1 - X2):
                for j in range (0, Y2 - Y1 - (X1 - X2) + 1):
                    if (self.map[Y1 + j][X1] == WALL):
                        self.numWallIntersectionsBetweenThem += 1
                for j in range (1, X1 - X2 + 1):
                    if (self.map[Y2 - (X1 - X2) + j][X1 - j] == WALL):
                        self.numWallIntersectionsBetweenThem += 1
            else:
                for j in range (0, Y2 - Y1 + 1):
                    if (self.map[Y1 + j][X1 - j] == WALL):
                        self.numWallIntersectionsBetweenThem += 1
                for j in range (1, X1 - X2 - (Y2 - Y1) + 1):
                    if (self.map[Y2][X1 - (Y2 - Y1) - j] == WALL):
                        self.numWallIntersectionsBetweenThem += 1
        
        temp1 = 0
        temp2 = 0           
        if (X2 <= X1 and Y1 >= Y2):
            for i in range (0, X1 - X2 + 1):
                if (self.map[Y1][X1 - i] == WALL):
                    temp1 += 1
            for i in range (1, Y1 - Y2 + 1):
                if (self.map[Y1 - i][X2] == WALL):
                    temp1 += 1
                    
            for i in range (0, Y1 - Y2 + 1):
                if (self.map[Y1 - i][X1] == WALL):
                    temp2 += 1
            for i in range (1, X1 - X2 + 1):
                if (self.map[Y2][X1 - i] == WALL):
                    temp2 += 1
            
        elif (X2 >= X1 and Y1 >= Y2):
            for i in range (0, X2 - X1 + 1):
                if (self.map[Y1][X1 + i] == WALL):
                    temp1 += 1
            for i in range (1, Y1 - Y2 + 1):
                if (self.map[Y1 - i][X2] == WALL):
                    temp1 += 1
                    
            for i in range (0, Y1 - Y2 + 1):
                if (self.map[Y1 - i][X1] == WALL):
                    temp2 += 1
            for i in range (1, X2 - X1 + 1):
                if (self.map[Y2][X1 + i] == WALL):
                    temp2 += 1
                    
        elif (X2 >= X1 and Y2 >= Y1):
            for i in range (0, X2 - X1 + 1):
                if (self.map[Y1][X1 + i] == WALL):
                    temp1 += 1
            for i in range (1, Y2 - Y1 + 1):
                if (self.map[Y1 + i][X2] == WALL):
                    temp1 += 1
                    
            for i in range (0, Y2 - Y1 + 1):
                if (self.map[Y1 + i][X1] == WALL):
                    temp2 += 1
            for i in range (1, X2 - X1 + 1):
                if (self.map[Y2][X1 + i] == WALL):
                    temp2 += 1
                    
        elif (X1 >= X2 and Y2 >= Y1):
            for i in range (0, X1 - X2 + 1):
                if (self.map[Y1][X1 - i] == WALL):
                    temp1 += 1
            for i in range (1, Y2 - Y1 + 1):
                if (self.map[Y1 + i][X2] == WALL):
                    temp1 += 1
                    
            for i in range (0, Y2 - Y1 + 1):
                if (self.map[Y1 + i][X1] == WALL):
                    temp2 += 1
            for i in range (1, X1 - X2 + 1):
                if (self.map[Y2][X1 - i] == WALL):
                    temp2 += 1
        
        self.numWallIntersectionsBetweenThem = min(self.numWallIntersectionsBetweenThem, min(temp1, temp2))
        self.distance = manhattanDistance(self.state, seekerPosition)
        
        #! Check whether the wall intersection is at a corner in the map
        self.checkCorner = False
        row = self.state[0]
        col = self.state[1]
        numRows = len(self.map)
        numCols = len(self.map[0])
        if (
            (row - 1 >= 0 and self.map[row - 1][col] == WALL and row + 1 < numRows and self.map[row + 1][col] == WALL and col - 1 >= 0 and self.map[row][col - 1] == WALL)
            or 
            (row - 1 >= 0 and self.map[row - 1][col] == WALL and row + 1 < numRows and self.map[row + 1][col] == WALL and col + 1 < numCols and self.map[row][col + 1] == WALL)
            or
            (col - 1 >= 0 and self.map[row][col - 1] == WALL and col + 1 < numCols and self.map[row][col + 1] == WALL and row - 1 >= 0 and self.map[row - 1][col] == WALL)
            or
            (col - 1 >= 0 and self.map[row][col - 1] == WALL and col + 1 < numCols and self.map[row][col + 1] == WALL and row + 1 < numRows and self.map[row + 1][col] == WALL)
            or
            (row == 0 and col - 1 >= 0 and self.map[row][col - 1] == WALL and row + 1 < numRows and self.map[row + 1][col] == WALL)
            or
            (row == 0 and col + 1 < numCols and self.map[row][col + 1] == WALL and row + 1 < numRows and self.map[row + 1][col] == WALL)
            or
            (row == numRows - 1 and col - 1 >= 0 and self.map[row][col - 1] == WALL and row - 1 >= 0 and self.map[row - 1][col] == WALL)
            or
            (row == numRows - 1 and col + 1 < numCols and self.map[row][col + 1] == WALL and row - 1 >= 0 and self.map[row - 1][col] == WALL)
            or
            (col == 0 and col + 1 < numCols and self.map[row][col + 1] == WALL and row + 1 < numRows and self.map[row + 1][col] == WALL)
            or
            (col == 0 and col + 1 < numCols and self.map[row][col + 1] == WALL and row - 1 >= 0 and self.map[row - 1][col] == WALL)
            or 
            (col == numCols - 1 and col - 1 >= 0 and self.map[row][col - 1] == WALL and row + 1 < numRows and self.map[row + 1][col] == WALL)
            or
            (col == numCols - 1 and col - 1 >= 0 and self.map[row][col - 1] == WALL and row - 1 >= 0 and self.map[row - 1][col] == WALL)
            or
            ((row, col) == (0, 0) and self.map[0][1] == WALL)
            or
            ((row, col) == (0, 0) and self.map[1][0] == WALL)
            or
            ((row, col) == (0, numCols - 1) and self.map[0][numCols - 2] == WALL)
            or
            ((row, col) == (0, numCols - 1) and self.map[1][numCols - 1] == WALL)
            or
            ((row, col) == (numRows - 1, 0) and self.map[numRows - 2][0] == WALL)
            or
            ((row, col) == (numRows - 1, 0) and self.map[numRows - 1][1] == WALL)
            or
            ((row, col) == (numRows - 1, numCols - 1) and self.map[numRows - 2][numCols - 1] == WALL)
            or
            ((row, col) == (numRows - 1, numCols - 1) and self.map[numRows - 1][numCols - 2] == WALL)
        ):
            self.checkCorner = True
        
    def __lt__ (self, other):
        if (self.numWallIntersectionsBetweenThem == other.numWallIntersectionsBetweenThem):
            if (self.checkCorner == other.checkCorner):
                if (self.distance == other.distance):
                    goal1 = A_Star(self.seekerPosition, self.state, self.map, self.visitedMatrix)
                    goal2 = A_Star(self.seekerPosition, other.state, self.map, self.visitedMatrix)
                    shortestPath1 = []
                    shortestPath2 = []
                    
                    while (goal1 is not None):
                        shortestPath1.append(goal1.state)
                        goal1 = goal1.parent
                    while (goal2 is not None):
                        shortestPath2.append(goal2.state)
                        goal2 = goal2.parent
                    
                    return len(shortestPath1) < len(shortestPath2)
                
                return self.distance < other.distance
            
            return self.checkCorner < other.checkCorner
        
        return self.numWallIntersectionsBetweenThem < other.numWallIntersectionsBetweenThem

class Level1:
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
        self.map: Map = map
        self.score: int = 0
        self.numSeekerSteps: int = 0 #? Increase this attribute by 1 if seeker took its turn and the game is not over
        self.numHiderSteps: int = 0 #? Increase this attribute by 1 if hider took its turn and the game is not over
        self.takeTurn: int = SEEKER
        
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
        self.listObservableCells: list[tuple[int, int]] = self.getObservableCells()
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
            self.goalPosition: tuple[int, int] = self.getNearestWallIntersection(self.seekerPosition)
            self.path: list[tuple[int, int]] = self.getShortestPath(self.goalPosition)
            self.pathMove: int = 0
    
    def broadcastAnnouncement (self) -> tuple[int, int]:
        listPositions = []
        
        for level in range (1, 3):
            for row in range (self.hiderPosition[0] - level, self.hiderPosition[0] + level + 1):
                if (row >= 0 and row < self.map.numRows):
                    for col in range (self.hiderPosition[1] - level, self.hiderPosition[1] + level + 1):
                        if (col >= 0 and col < self.map.numCols and (row, col) != self.hiderPosition):
                            listPositions.append((row, col))
                    
        randomPosition = choice(listPositions)
        return randomPosition
    
    def hiderTakeTurn (self):
        if (self.numHiderSteps == 0 or self.numHiderSteps % 8 != 0):
            return
        
        #! The hider will broadcast an announcement after each 8 steps and set the time for this announcement
        self.announcement = self.broadcastAnnouncement()
        self.announcementTime = 0
        
    def getObservableCells (self):
        radius_3_matrix: list[list[bool]] = []
        seeker_position_in_matrix: tuple[int, int] = None
        for row in range (self.seekerPosition[0] - 3, self.seekerPosition[0] + 4):
            if (row >= 0 and row < self.map.numRows):
                tempList: list[int] = []
            
                for col in range (self.seekerPosition[1] - 3, self.seekerPosition[1] + 4):
                    if (col >= 0 and col < self.map.numCols):
                        if (self.map.matrix[row][col] == WALL):
                            tempList.append(False)
                        else:
                            tempList.append(True)
                            
                        if ((row, col) == self.seekerPosition):
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
        for row in range (self.seekerPosition[0] - 3, self.seekerPosition[0] + 4):
            if (row >= 0 and row < self.map.numRows):
                index_col = 0
                
                for col in range (self.seekerPosition[1] - 3, self.seekerPosition[1] + 4):
                    if (col >= 0 and col < self.map.numCols):
                        if (radius_3_matrix[index_row][index_col] and (row, col) != self.seekerPosition):
                            listObservablePositions.append((row, col))
                        index_col = index_col + 1
                        
                index_row = index_row + 1
                    
        return listObservablePositions
    
    def getNearestWallIntersection (self, curPosition: tuple[int, int]) -> tuple[int, int]:
        #! Be sure that the result is unvisited before
        # level = 1
        # found = False
        # maxLevel = max(curPosition[0], max(self.map.numRows - 1 - curPosition[0], max(curPosition[1], self.map.numCols - 1 - curPosition[1])))
        
        # while (not found and level <= maxLevel):
        #     for row in range (curPosition[0] - level, curPosition[0] + level + 1):
        #         if (row >= 0 and row < self.map.numRows):
        #             for col in range (curPosition[1] - level, curPosition[1] + level + 1):
        #                 if (col >= 0 and col < self.map.numCols):
        #                     if (self.map.matrix[row][col] == WALL and (row + 1 < self.map.numRows and self.map.matrix[row + 1][col] == WALL)
        #                         and (col + 1 < self.map.numCols and self.map.matrix[row][col + 1] == WALL)):
        #                         if (not self.visitedMatrix[row + 1][col + 1] and self.map.matrix[row + 1][col + 1] != WALL):
        #                             return (row + 1, col + 1)
                            
        #                     if (self.map.matrix[row][col] == WALL and (row + 1 < self.map.numRows and self.map.matrix[row + 1][col] == WALL)
        #                         and (col - 1 >= 0 and self.map.matrix[row][col - 1] == WALL)):
        #                         if (not self.visitedMatrix[row + 1][col - 1] and self.map.matrix[row + 1][col - 1] != WALL):
        #                             return (row + 1, col - 1)
                            
        #                     if (self.map.matrix[row][col] == WALL and (row - 1 >= 0 and self.map.matrix[row - 1][col] == WALL)
        #                         and (col - 1 >= 0 and self.map.matrix[row][col - 1] == WALL)):
        #                         if (not self.visitedMatrix[row - 1][col - 1] and self.map.matrix[row - 1][col - 1] != WALL):
        #                             return (row - 1, col - 1)
                            
        #                     if (self.map.matrix[row][col] == WALL and (row - 1 >= 0 and self.map.matrix[row - 1][col] == WALL)
        #                         and (col + 1 < self.map.numCols and self.map.matrix[row][col + 1] == WALL)):
        #                         if (not self.visitedMatrix[row - 1][col + 1] and self.map.matrix[row - 1][col + 1] != WALL):
        #                             return (row - 1, col + 1)
                                
        #                     if ((row, col) == (0, self.map.numCols - 1) or (row, col) == (0, 0)
        #                         or (row, col) == (self.map.numRows - 1, self.map.numCols - 1)
        #                         or (row, col) == (self.map.numRows - 1, 0)):
        #                         if (not self.visitedMatrix[row][col] and self.map.matrix[row][col] != WALL):
        #                             return (row, col)
                            
        #                     if ((col == self.map.numCols - 1 or col == 0) and self.map.matrix[row][col] == WALL):
        #                         if (row - 1 >= 0 and not self.visitedMatrix[row - 1][col] and self.map.matrix[row - 1][col] != WALL):
        #                             return (row - 1, col)

        #                         if (row + 1 < self.map.numRows and not self.visitedMatrix[row + 1][col] and self.map.matrix[row + 1][col] != WALL):
        #                             return (row + 1, col)
                            
        #                     if ((row == self.map.numRows - 1 or row == 0) and self.map.matrix[row][col] == WALL):
        #                         if (col - 1 >= 0 and not self.visitedMatrix[row][col - 1] and self.map.matrix[row][col - 1] != WALL):
        #                             return (row, col - 1)

        #                         if (col + 1 < self.map.numCols and not self.visitedMatrix[row][col + 1] and self.map.matrix[row][col + 1] != WALL):
        #                             return (row, col + 1)
    
        #     level = level + 1
        
        #! Add all unvisited wall intersections to a list
        unvisitedWallIntersections: list[WallIntersection] = []
        for intersection in self.listWallIntersections:
            if (not self.visitedMatrix[intersection[0]][intersection[1]]):
                heappush(unvisitedWallIntersections, WallIntersection(intersection, self.seekerPosition, self.map.matrix, self.visitedMatrix))
        
        if (len(unvisitedWallIntersections) == 0):
            return None
          
        #! Choose a wall intersection with the smallest optimal path cost from the current seeker position
        intersection = heappop(unvisitedWallIntersections)
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
        self.listObservableCells = self.getObservableCells()
        if (self.IdentifiedHider is not None):
            return
        else:
            self.IdentifiedHider = self.identifyObservableHider()
            
        if (self.IdentifiedAnnouncement is None):
            self.IdentifiedAnnouncement = self.identifyObservableAnnouncement()
        
        #! Observed hider --> Conduct to touch the hider
        if (self.IdentifiedHider is not None and self.goalPosition != self.IdentifiedHider):
            self.goalPosition = self.IdentifiedHider
            self.path = self.getShortestPath(self.goalPosition)
            self.pathMove = 0
            return
        
        #! Observed an announcement while not observing the hider or observed an announcement before --> Conduct to move to the position of that announcement
        if (self.IdentifiedHider is None and self.listUnvisitedPositionsAroundAnnouncement is None and 
            self.IdentifiedAnnouncement is not None and self.goalPosition != self.IdentifiedAnnouncement):
            self.goalPosition = self.IdentifiedAnnouncement
            self.path = self.getShortestPath(self.goalPosition)
            self.pathMove = 0
            return
        
        if (self.seekerPosition == self.goalPosition):
            #! Reached the position of the hider -> Stop
            if (self.IdentifiedHider is not None):
                return
            #! Reached the position of the announcement -> Get unvisited positions in the radius of 3 around this announcement.
            elif (self.listUnvisitedPositionsAroundAnnouncement is None and self.IdentifiedAnnouncement is not None): 
                listUnvisitedPositions = []
                
                for level in range (1, 3):
                    for row in range (self.IdentifiedAnnouncement[0] - level, self.IdentifiedAnnouncement[0] + level + 1):
                        if (row >= 0 and row < self.map.numRows):
                            for col in range (self.IdentifiedAnnouncement[1] - level, self.IdentifiedAnnouncement[1] + level + 1):
                                if (col >= 0 and col < self.map.numCols and not self.visitedMatrix[row][col] and self.IdentifiedAnnouncement != (row, col)):
                                    listUnvisitedPositions.append((row, col))

                self.listUnvisitedPositionsAroundAnnouncement = listUnvisitedPositions.copy()
                self.goalPosition = self.listUnvisitedPositionsAroundAnnouncement[0]
                self.listUnvisitedPositionsAroundAnnouncement = self.listUnvisitedPositionsAroundAnnouncement[1:]
                self.path = self.getShortestPath(self.goalPosition)
                self.pathMove = 0
            #! Reached one unvisited position in the radius of 3 around the old announcement
            elif (self.listUnvisitedPositionsAroundAnnouncement is not None and len(self.listUnvisitedPositionsAroundAnnouncement) != 0):
                self.goalPosition = self.listUnvisitedPositionsAroundAnnouncement[0]
                self.listUnvisitedPositionsAroundAnnouncement = self.listUnvisitedPositionsAroundAnnouncement[1:]
                self.path = self.getShortestPath(self.goalPosition)
                self.pathMove = 0          
            else:
                self.goalPosition = self.getNearestWallIntersection(self.seekerPosition)
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