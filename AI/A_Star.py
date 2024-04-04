from heapq import heappush, heappop
from AI.util import *

class Node:
    """
    Node class for A* algorithm.
    """
    def __init__ (self, state: tuple[int, int], parent, goal: tuple[int, int], visited: bool = 0):
        self.state = state
        self.parent = parent
        self.pathCost = None
        
        if (parent is None):
            self.pathCost = 0
        else:
            self.pathCost = parent.pathCost + 1
            
        self.f = self.pathCost + manhattanDistance(self.state, goal) + 100 * visited
        """
        Explanation for 100 * visited: 
        We want to prioritize the unvisited nodes, so we add a large number to the f value of the visited nodes.
        If neighbors of a node are visited, the agent can move normally to visited nodes without any problem.
        """
        
    def __lt__ (self, other):
        return self.f < other.f

def A_Star (start: tuple[int, int], goal: tuple[int, int], map: list[list[int]], visitedMatrix: list[list[bool]] = None) -> Node:
    """
    A* algorithm.
    At each node, if the parameter visitedMatrix is not None, 
    the cost of the node can be considered as the sum of the path cost, the heuristic cost, and the visited cost.
    """
    node: Node = None
    if (visitedMatrix is None):
        node = Node(start, None, goal)
    else:
        node = Node(start, None, goal, visitedMatrix[start[0]][start[1]])
    
    frontier = []
    reached: dict[tuple[int, int], Node] = dict()
    heappush(frontier, node)
    
    while (frontier):
        node = heappop(frontier)
        reached[node.state] = node
        
        if (node.state == goal):
            return node
        
        listValidNeighbors = getValidNeighbors(node.state, map)
        for neighbor in listValidNeighbors:
            neighborNode = None
            if (visitedMatrix is None):
                neighborNode = Node(neighbor, node, goal)
            else:
                neighborNode = Node(neighbor, node, goal, visitedMatrix[neighbor[0]][neighbor[1]])
            
            if (reached.get(neighbor) is None or (reached.get(neighbor) is not None and reached[neighbor].f > neighborNode.f)):
                heappush(frontier, neighborNode)
                reached[neighbor] = neighborNode
                
    return None