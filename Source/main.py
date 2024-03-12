import sys
from Map import *             
        
if len(sys.argv) != 2:
    sys.exit("Usage: python main.py input.txt")  
    
newMaze = Map(sys.argv[1])
newMaze.output_image("maze.png")  