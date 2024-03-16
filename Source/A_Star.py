from heapq import heappush, heappop
from util import *

def A_Star (start: tuple[int, int], goal: tuple[int, int], map: list[list[int]], visitedMatrix: list[list[bool]]) -> Node:
    node: Node = Node(start, None, goal, visitedMatrix[start[0]][start[1]])
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
            neighborNode = Node(neighbor, node, goal, visitedMatrix[neighbor[0]][neighbor[1]])
            if (reached.get(neighbor) is None or (reached.get(neighbor) is not None and reached[neighbor].f > neighborNode.f)):
                heappush(frontier, neighborNode)
                reached[neighbor] = neighborNode
                
    return None