from copy import deepcopy

import pygame
from AI.Level1 import *
from AI.Level2 import *
from AI.Level3 import *

from UI.Configs.config import *
from UI.Widget.widget import *
from UI.Utils.move import *


class DisplayMap:
    """
    Handle running the game and print each step to the screen.
    """

    def __init__(self, cur_map, level, display, widgets):
        self.cur_map = cur_map
        self.level = level
        self.display = display
        self.widgets = widgets

        self.score = 0
        self.give_up = False
        self.redirect()

    def redirect(self):
        """
        Redirect to the corresponding level.
        """
        if self.level == 1:
            self.runLevel1()
        elif self.level == 2:
            self.runLevel2()
        elif self.level == 3:
            self.runLevel3()
        # elif self.level == 4:
        #     self.runLevel4()

    def runLevel1(self):
        map = Map(self.cur_map)
        # Check for the map conditions
        if len(map.listHiderPositions) == 0:
            raise Exception("This map has no hider")
        elif len(map.listHiderPositions) > 1:
            raise Exception("This is not a map for Level 1")

        game = Level1(map)

        listThings = game.level1()
        prev = next(listThings)
        # Loop through each step
        for thing in listThings:
            score = thing[2]  # Current score
            seeker_pos = thing[0]

            # The direction the the seeker takes
            direction = getDirection(prev[0], seeker_pos)

            # Delete the old observable cells
            self.cur_map = recov_obser(mp=self.cur_map, loc=prev[3])
            # Move the seeker
            self.cur_map = moveTiles(mp=self.cur_map, mv=direction, loc=prev[0])
            # Assign the new observable cells
            self.cur_map = assign_obser(mp=self.cur_map, loc=thing[3])

            # If there is annoucement
            tmp = (0, 0)
            if thing[4]:
                tmp = self.cur_map[thing[4][0]][thing[4][1]]
                self.cur_map[thing[4][0]][thing[4][1]] = 6
            # Print the current map to the screen
            self.printMap(score)
            # Recover the announcement position
            if thing[4]:
                self.cur_map[thing[4][0]][thing[4][1]] = tmp
            # Let the current step be the previous step
            prev = thing
        self.score = score

    def runLevel2(self):
        map = Map(self.cur_map)
        # Check the map conditions
        if len(map.listHiderPositions) == 0:
            raise Exception("The map has no hider")

        game = Level2(map)

        listThings = game.level2()
        prev = next(listThings)

        for thing in listThings:
            score = thing[2]
            seeker_pos = thing[0]

            # Get the seeker's direction
            direction = getDirection(prev[0], seeker_pos)

            # Delete the old observable cells, move the seeker, assign the new observable cells
            self.cur_map = recov_obser(mp=self.cur_map, loc=prev[3])
            self.cur_map = moveTiles(mp=self.cur_map, mv=direction, loc=prev[0])
            self.cur_map = assign_obser(mp=self.cur_map, loc=thing[3])

            # If there is announcement
            tmp = []
            if thing[4]:
                for x, y in thing[4]:
                    tmp.append(self.cur_map[x][y])
                    self.cur_map[x][y] = 6

            # Print the map
            self.printMap(score)

            if thing[4]: # Recover the announcement
                for i, (x, y) in enumerate(thing[4]):
                    self.cur_map[x][y] = tmp[i]

            # Update the previous to the current
            prev = thing
        self.score = score

    def runLevel3(self):
        # Check the map conditions
        map = Map(self.cur_map)
        if len(map.listHiderPositions) == 0:
            raise Exception("The map has no hider")

        game = Level3(map)

        listThings = game.level3()
        prev = deepcopy(next(listThings)) # Get the first step

        for cur in listThings:
            self.give_up = cur[-1] # Giving up sign
            score = cur[2] # Current score

            hider_obv = []
            pt1, pt2 = 0, 0
            # Get all of the hider's observable cells at the current step
            while pt1 < len(prev[1]) and pt2 < len(cur[1]):
                if prev[1][pt1] == cur[1][pt2]:
                    hider_obv += cur[1][pt2].hiderObservableCells
                    pt1 += 1
                    pt2 += 1
                else:
                    pt1 += 1
            # Move seeker and hiders (and clear old observable cells)
            self.cur_map = setSeeker(self.cur_map, cur[0])
            self.cur_map = setHiders(self.cur_map, [x.state for x in cur[1]])
            # Assign the new observable cells
            self.cur_map = assign_obser(mp=self.cur_map, loc=cur[3], person=SEEKER)
            self.cur_map = assign_obser(mp=self.cur_map, loc=hider_obv, person=HIDER)

            # Announcement
            tmp = []
            if cur[4]:
                for x, y in cur[4]:
                    tmp.append(self.cur_map[x][y])
                    self.cur_map[x][y] = 6
            # Print the map      
            self.printMap(score)

            # Recover announcement
            if cur[4]:
                for i, (x, y) in enumerate(cur[4]):
                    self.cur_map[x][y] = tmp[i]
            if self.give_up: # If the seeker gives up, quit the game
                break
            prev = deepcopy(cur) # Update the previous step
        self.score = score

    def printMap(self, score):
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                quit()
        # Print the current map and the score
        mp = MapWidget(self.cur_map, self.level)
        txt = Text(
            text=f"Score: {score}",
            position=Vector2(WIDTH // 2 + 280, HEIGHT // 2 - 150),
            size=Vector2(180, 50),
            color=BLACK,
            font_size=26,
        )
        
        # Remove the old map and score
        self.widgets.pop("Text")
        self.widgets.pop("MapWidget")
        # Add the new map and score
        self.widgets.add(txt)
        self.widgets.add(mp)

        # Re-render the widgets
        self.widgets.__render__(self.display)
        pygame.display.flip()
        
        # If the level is >= 3, when the seeker chase the hider
        # The game will update slower to let the user see the chase
        if self.level >= 3:
            for i in range(len(self.cur_map)):
                broke = False
                for j in range(len(self.cur_map[0])):
                    if self.cur_map[i][j] == OVERLAP:
                        broke = True
                        break
                if broke:
                    pygame.time.wait(CHASE_RANGE_TIME)
                    break
        # Delay the game at each step
        pygame.time.wait(DELAY_TIME)

    # Return the result of the game
    def getResult(self):
        return self.score, self.give_up
