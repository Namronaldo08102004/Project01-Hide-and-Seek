EMPTY = 0
WALL = 1
HIDER = 2
SEEKER = 3

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
            
def manhattanDistance (point1: tuple[int, int], point2: tuple[int, int]):
    return abs(point2[0] - point1[0]) + abs(point2[1] - point1[1])

def getValidNeighbors (state: tuple[int, int], map: list[list[int]]) -> list[tuple[int, int]]:
        X, Y = state
        candidates = [(X + 1, Y - 1), (X + 1, Y), (X, Y - 1), (X + 1, Y + 1), (X - 1, Y - 1), (X, Y + 1), (X - 1, Y), (X - 1, Y + 1)]
        width = len(map)
        length = len(map[0])

        result = []
        for (x, y) in candidates:
            if 0 <= x <= width - 1 and 0 <= y <= length - 1:
                check = True
                if (map[x][y] == WALL):
                    check = False
                
                if (check):
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