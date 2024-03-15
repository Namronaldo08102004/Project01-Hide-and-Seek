from homescreen import *

class Puzzle:
    def __init__(self):
        self.home = HOME()
        self.choice = self.home.Run()
        
if __name__ == "__main__":
    puzzle = Puzzle()
    print(puzzle.choice)
    puzzle.home.Quit()