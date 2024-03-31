import math

EMPTY = 0
WALL = 1
HIDER = 2
SEEKER = 3
OBSERVABLE = 4
OBSTACLE = 5

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHTBLUE = (173, 216, 230)
GRAY = (128, 128, 128)
LIGHTPINK = (255, 182, 193)
SKINCOLOR = (255, 224, 189)
RED = (255, 0, 0)
GREEN = (0, 171, 28)
YELLOW = (255, 215, 0)
BROWN = (128, 64, 0)

def dot_product(v1, v2):
    return sum(x * y for x, y in zip(v1, v2))

def vector_magnitude(v):
    return math.sqrt(sum(x ** 2 for x in v))

def angle_between_vectors(v1, v2):
    dot_prod = dot_product(v1, v2)
    mag_v1 = vector_magnitude(v1)
    mag_v2 = vector_magnitude(v2)
    if mag_v1 == 0 or mag_v2 == 0:
        return float('NaN')  # Handle division by zero
    cos_angle = dot_prod / (mag_v1 * mag_v2)
    angle_rad = math.acos(cos_angle)
    return math.degrees(angle_rad)
            
def manhattanDistance (point1: tuple[int, int], point2: tuple[int, int]):
    return abs(point2[0] - point1[0]) + abs(point2[1] - point1[1])

def getValidNeighbors (state: tuple[int, int], map: list[list[int]]) -> list[tuple[int, int]]:
        X, Y = state
        candidates = [(X + 1, Y - 1), (X + 1, Y + 1), (X - 1, Y - 1), (X - 1, Y + 1), (X + 1, Y), (X, Y - 1), (X, Y + 1), (X - 1, Y)]
        width = len(map)
        length = len(map[0])

        result = []
        for (x, y) in candidates:
            if 0 <= x <= width - 1 and 0 <= y <= length - 1:
                check = True
                if (map[x][y] in [WALL, OBSTACLE]):
                    check = False
                
                if (check):
                    result.append((x, y))
        return result

def getTrendMoveDirection (state: tuple[int, int], goal: tuple[int, int]) -> str:
    X = state[0]
    Y = state[1]
    goalX = goal[0]
    goalY = goal[1]
    
    listDirectionVectors = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
    listDirection = ["UP", "UPRIGHT", "RIGHT", "DOWNRIGHT", "DOWN", "DOWNLEFT", "LEFT", "UPLEFT"]
    vectorMove = (goalX - X, goalY - Y)
    
    minAngle = 361
    trendMoveDirection = None
    for i in range(8):
        angle = angle_between_vectors(vectorMove, listDirectionVectors[i])
        if (angle < minAngle):
            minAngle = angle
            trendMoveDirection = listDirection[i]
            
    return trendMoveDirection
    
def setOrderOfNeighbor (state: tuple[int, int], trendMoveDirection, neighbors: list[tuple[int, int]]) -> list[tuple[int, int]]:
    X = state[0]
    Y = state[1]
    order = None
    
    if (trendMoveDirection == "UP" or trendMoveDirection == "UPRIGHT"):
        order = [(X - 1, Y + 1), (X + 1, Y + 1), (X + 1, Y - 1), (X - 1, Y - 1), (X - 1, Y), (X, Y + 1), (X + 1, Y), (X, Y - 1)]
    elif (trendMoveDirection == "RIGHT" or trendMoveDirection == "DOWNRIGHT"):
        order = [(X + 1, Y + 1), (X + 1, Y - 1), (X - 1, Y - 1), (X - 1, Y + 1), (X, Y + 1), (X + 1, Y), (X, Y - 1), (X - 1, Y)]
    elif (trendMoveDirection == "DOWN" or trendMoveDirection == "DOWNLEFT"):
        order = [(X + 1, Y - 1), (X - 1, Y - 1), (X - 1, Y + 1), (X + 1, Y + 1), (X + 1, Y), (X, Y - 1), (X - 1, Y), (X, Y + 1)]
    elif (trendMoveDirection == "LEFT" or trendMoveDirection == "UPLEFT"):
        order = [(X - 1, Y - 1), (X - 1, Y + 1), (X + 1, Y + 1), (X + 1, Y - 1), (X, Y - 1), (X - 1, Y), (X, Y + 1), (X + 1, Y)]
        
    result = []
    for (x, y) in order:
        if ((x, y) in neighbors):
            result.append((x, y))
            
    return result

class Node:
    def __init__ (self, state: tuple[int, int], parent, goal: tuple[int, int], visited: bool = 0):
        self.state = state
        self.parent = parent
        self.pathCost = None
        
        if (parent is None):
            self.pathCost = 0
        else:
            self.pathCost = parent.pathCost + 1
            
        self.f = self.pathCost + manhattanDistance(self.state, goal) + 100 * visited
        
    def __lt__ (self, other):
        return self.f < other.f