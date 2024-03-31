"""
This file contains the configurations for the game.
Includes the pre-defined colors, dimensions, and other constants.
"""

WALL, HIDER, SEEKER, OBSERVABLE, OBSTACLE, ANNOUNCE, H_OBSERVABLE, OVERLAP = 1, 2, 3, 4, 5, 6, 7, 8

HEIGHT, WIDTH = 720, 1080
WHITE, BLACK = (255, 255, 255), (0, 0, 0)
RED, GREEN, BLUE = (255, 0, 0), (0, 255, 0), (0, 0, 255)

HOVER = (30, 233, 240)

LEGEND_BGC = (243, 203, 218)


BGC = (235, 215, 232)
WALLC = (156, 175, 170)
SEEKERC = (236, 84, 37)
HIDERC = (53, 228, 94)
OBSTACLEC = (116, 105, 182)
ANNOUNCEC = (0, 0, 0)
HIDER_OBSERVABLEC = (233, 231, 174)
SEEKER_OBSERVABLEC = (109, 221, 212)

OVERLAPC = tuple([int((a + b) / 2) for a, b in zip(HIDER_OBSERVABLEC, SEEKER_OBSERVABLEC)])

PATH = (223, 117, 69)

DELAY_TIME = 100  # ms
CHASE_RANGE_TIME = 50

FONT = "UI/Assets/MadimiOne-Regular.ttf"
FONT2 = "UI/Assets/OpenSans-Regular.ttf"