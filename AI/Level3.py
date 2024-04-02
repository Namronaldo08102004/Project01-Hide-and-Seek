from AI.Level_util import *

class Hider:
    """
    This class is used to create hider objects, served for comparing two hider objects in level 2 and moving hiders in level 3
    """
    def __init__ (self, state: tuple[int, int], map, id: int = None):
        self.id = id #? This attribute is used to compare two hider objects
        self.state = state
        self.map = map
        
        self.hiderObservableCells = self.getObservableCellsOfHider(self.state)
        self.identifiedSeeker = None #? This attribute is used to pass into parameters of A_Star function in __lt__ method
    
    """
    Three below methods are used to compare two hider objects, as well as to hash them when we add them into a set
    (We used set structure in level 2)
    """
    def __eq__ (self, other):
        if (self.id is not None and other.id is not None):
            return self.id == other.id
        return self.state == other.state
    
    def __ne__ (self, other):
        if (self.id is not None and other.id is not None):
            return self.id != other.id
        return self.state != other.state
    
    def __hash__ (self):
        return hash(self.state)
    
    def getObservableCellsOfHider (self, hiderPosition: tuple[int, int]):
        """
        Get the observable cells of the hider.
        """
        mapNumRows = len(self.map)
        mapNumCols = len(self.map[0])
        
        """
        Firstly, we create a boolean matrix with the maximum size of 5x5 around the hider position (We only get valid cells in the map)
        We initially assign False to the cells that are walls or obstacles, and True to the other cells
        Through instantiate this matrix, we can get the exact position of the hider in the matrix, which supports us to identify the observable cells
        """
        radius_2_matrix: list[list[bool]] = []
        hider_position_in_matrix: tuple[int, int] = None
        for row in range (hiderPosition[0] - 2, hiderPosition[0] + 3):
            if (row >= 0 and row < mapNumRows):
                tempList: list[int] = []
            
                for col in range (hiderPosition[1] - 2, hiderPosition[1] + 3):
                    if (col >= 0 and col < mapNumCols):
                        if (self.map[row][col] in [WALL, OBSTACLE]):
                            tempList.append(False)
                        else:
                            tempList.append(True)
                            
                        if ((row, col) == hiderPosition):
                            hider_position_in_matrix = (len(radius_2_matrix), len(tempList) - 1)
                    
                radius_2_matrix.append(tempList)
        
        """
        We will use the below cases to assign False to the cells that are not observable by the hider
        Consider cells in the radius 1 around the hider position
            + If the cell is a wall or an obstacle, we will assign False to cells in the larger radius (refered in the guidelines of lecturer)
            + We also consider aside cells of a certain cell in the radius 1, because if two aside cells are walls or obstacles, 
            we can assign False to cells which are in the area created by the map, two lines from the hider position to those two aside cells
            
             ------ ------ ------ ------ ------
            |  UO  |  UO  |  UO  |      |      |
            |      |      |      |      |      |
             ------ ------ ------ ------ ------
            |      | Wall | Wall |      |      |
            |      |      |      |      |      |
             ------ ------ ------ ------ ------
            |      |      | Hider|      |      |
            |      |      |      |      |      |
             ------ ------ ------ ------ ------
            |      |      |      |      |      |
            |      |      |      |      |      |
             ------ ------ ------ ------ ------
            |      |      |      |      |      |
            |      |      |      |      |      |
             ------ ------ ------ ------ ------
            
            UO: Unobservable
            
        """
               
        X = hider_position_in_matrix[0]
        Y = hider_position_in_matrix[1]
        numRows = len(radius_2_matrix)
        numCols = len(radius_2_matrix[0])
                
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
        
        """
        From the boolean matrix, we can get the observable cells of the hider in the original map
        """
        listObservablePositions = []
        index_row = 0
        for row in range (hiderPosition[0] - 2, hiderPosition[0] + 3):
            if (row >= 0 and row < mapNumRows):
                index_col = 0
                
                for col in range (hiderPosition[1] - 2, hiderPosition[1] + 3):
                    if (col >= 0 and col < mapNumCols):
                        if (radius_2_matrix[index_row][index_col] and (row, col) != hiderPosition):
                            listObservablePositions.append((row, col))
                        index_col = index_col + 1
                        
                index_row = index_row + 1
                    
        return listObservablePositions
    
    def identifyObservableSeeker (self, seekerPosition: tuple[int, int]):
        """
        This function is used to identify whether the seeker is in the observable cells of the hider
            + If the seeker is in the observable cells, we will return its position
            + Otherwise, we will return None
        """
        Position: tuple[int, int] = None
        
        for cell in self.hiderObservableCells:
            if (cell == seekerPosition):
                Position = cell
                break
                
        return Position

class Level3 (Level):
    """
    The strategy of this level for the seeker is identical to two previous levels, except for the following points:
        + The seeker still maintains a matrix of visited cells, but it does not consider this attribute in finding the
        shortest path to the nearest wall intersection or hiders and announcements. The visited matrix just be used to mark
        unvisited wall intersections or when the seeker wants to move to a certain cell if all the wall intersections are visited.
        
        + When the seeker meets a hider, it will use the Nash theory in Game Theory to find the best move for both the seeker and the hider.
        The idea of this algorithm will be presented in the description of the function getBestMoveWhenHiderMeetSeeker.
        
        + About hiders, because it can move, so we set for each hider to move intelligently when it meets the seeker.
        Our improvement for hiders will be presented in the description of the function hiderTakeTurn.
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
        The below attribute is used to store the state of the seeker before catching the hider, two elements in each stae are:
            + The position of the seeker before catching the hider
            + The position of the seeker in the next move
        """
        self.roadOfSeekerWhenCatchHider: list[tuple[tuple[int, int], tuple[int, int]]] = []
        
        """
        This attribute stores hiders which are permanently ignored by the seeker
        If the number of ignored hiders is equal to the number of hiders currently in the map, the seeker will give up
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
                #! The only difference of this function between Level 3 and two previous levels is not using self.visitedMatrix in the below line
                shortestPath = self.getShortestPath(startPositionForFinding, intersection[0])
                if (shortestPath is not None): #? If the seeker can reach the wall intersection
                    nearestWallIntersection = intersection[0]
                    AStar = len(shortestPath)
                    minHeuristic = intersection[1] - 0.9 * isCorner
            elif (intersection[1] - 0.9 * isCorner == minHeuristic):
                shortestPath = self.getShortestPath(startPositionForFinding, intersection[0])
                if (shortestPath is not None and (AStar is None or (AStar is not None and len(shortestPath) < AStar))):
                    nearestWallIntersection = intersection[0]
                    AStar = len(shortestPath)
        
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
            
            + Until now, if there are many tuples satisfying the above statement, we consider two cases:
                o If the first taker is the seeker, we will choose the cell that the number of cells the hider can move to not be caught in the next move is the smallest
                o If the first taker is the hider, we will sequentially consider the following conditions, prioritized from the highest to the lowest:
                    - If the cell is a wall intersection that we still move diagonally if moving to that intersection, choose that cell
                    - If the cell can allow hider to have the largest number of escape cells (we suppose that the hider thinks that the seeker 
                    will minimize the number of cells the hider can move to not be caught in the next move), choose that cell
                    - If the cell can allow hider to observe the largest number of cells excluding wall intersections, choose that cell
                    
        Besides, in valid neighbors of the hider when the taker is hider, we will discard the neighbors which are the positions of other hiders to avoid the collapsion
        We also set the order of the neighbors of the current hider position when hider takes turn based on the trend of the movement from the seeker to the hider,
        which can help hider consider cells forward instead of towards the seeker.
        """
        hiderPosition = hider.state
        
        if (self.takeTurn == SEEKER):
            listSeekerValidNeighbor = getValidNeighbors(seekerPosition, self.map.matrix)
            listHiderValidNeighbor = getValidNeighbors(hiderPosition, self.map.matrix)

            nashTable: list[list[tuple[int, int]]] = []
            for i in range (0, len(listSeekerValidNeighbor)):
                lst = []
                
                shortestPath = self.getShortestPath(listSeekerValidNeighbor[i], hiderPosition)
                if (shortestPath is None):
                    return None
                X = len(shortestPath)
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
                
                shortestPath = self.getShortestPath(listHiderValidNeighbor[i], seekerPosition)
                if (shortestPath is None):
                    return None
                X = len(shortestPath)
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
        
        #! If the seeker is going to a certain wall intersection
        if (self.gotoIntersection):
            self.seekerPosition = self.seekerPath[self.seekerPathMove]
            self.seekerPathMove = self.seekerPathMove + 1
            self.listSeekerObservableCells = self.getObservableCells(self.seekerPosition)
            
            #! Update the list of identified hiders
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
        
        #! If the seeker is going to a certain hider
        elif (self.gotoHider):
            if (len(self.listIdentifiedHiders) != 0):
                goal = self.listIdentifiedHiders[0]
                hiderPosition = goal.state
                
                NextMove = self.getBestMoveWhenHiderMeetSeeker(self.seekerPosition, goal)
                if (NextMove is not None and (self.seekerPosition, NextMove) not in self.roadOfSeekerWhenCatchHider):
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
                                                self.seekerPath = self.getShortestPath(self.seekerPosition, self.seekerGoalPosition, self.visitedMatrix)
                                                
                                                if (self.seekerPath is not None):
                                                    self.seekerPathMove = 0
                                                    found = True
                                                    break
                                
                                if (found):
                                    break
                            
                            if (found):
                                break
                    
                            level = level + 1
                            
                        if (not found):
                            self.giveUp = True
                            return
                        
                    self.gotoIntersection = True
                    self.gotoHider = False
                    return
            
            #! This case was built to handle the situation when the hider jumps to the seeker's position to suicide
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
                                            self.seekerPath = self.getShortestPath(self.seekerPosition, self.seekerGoalPosition, self.visitedMatrix)
                                            
                                            if (self.seekerPath is not None):
                                                self.seekerPathMove = 0
                                                found = True
                                                break
                            
                            if (found):
                                break
                        
                        if (found):
                            break
                
                        level = level + 1
                        
                    if (not found):
                        self.giveUp = True
                        return
                    
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
                                                self.seekerPath = self.getShortestPath(self.seekerPosition, self.seekerGoalPosition, self.visitedMatrix)
                                                
                                                if (self.seekerPath is not None):
                                                    self.seekerPathMove = 0
                                                    found = True
                                                    break
                                
                                if (found):
                                    break
                            
                            if (found):
                                break
                    
                            level = level + 1
                            
                        if (not found):
                            self.giveUp = True
                            return
                    
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
                                            self.seekerPath = self.getShortestPath(self.seekerPosition, self.seekerGoalPosition, self.visitedMatrix)
                                            
                                            if (self.seekerPath is not None):
                                                self.seekerPathMove = 0
                                                found = True
                                                break
                            
                            if (found):
                                break
                        
                        if (found):
                            break
                
                        level = level + 1
                        
                    if (not found):
                        self.giveUp = True
                        return
                
                self.gotoIntersection = True
                self.gotoHider = False
    
    def hiderTakeTurn (self, hider: Hider):
        """
        This function is created to help hider take turn in the game
        
        We will consider the following cases:
            + If the hider is not being chased by the seeker, the hider will take the best move to maximize the number of observable cells.
            This helps hider to avoid standing at corners or wall intersections, which can be easily caught by the seeker
            
            + If the hider is being chased by the seeker, the hider will take the best move to avoid being caught by the seeker
            based on the method getBestMoveWhenHiderMeetSeeker
            Besides, if the hider is being chased by the seeker but cannot observe the seeker, the attribute isBeingChased will helps
            hider to realize that it is still being chased by the seeker, and choose the best move for the next step
        """
        
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