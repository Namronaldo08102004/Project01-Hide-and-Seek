import pygame
from copy import deepcopy
from Configs.config import *
from Source.Level1 import *
from Source.Level2 import *
from Source.Level3 import *
from Utils.move import *
from Widget.widget import *


class DisplayMap:
    def __init__(self, cur_map, level, display, widgets):
        self.cur_map = cur_map
        self.level = level
        self.display = display
        self.widgets = widgets

        self.score = 0
        self.give_up = False
        self.redirect()

    def redirect(self):
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
        if len(map.listHiderPositions) == 0:
            raise Exception("This map has no hider")
        elif len(map.listHiderPositions) > 1:
            raise Exception("This is not a map for Level 1")

        game = Level1(map)

        listThings = game.level1()
        prev = next(listThings)

        for thing in listThings:
            score = thing[2]
            seeker_pos = thing[0]

            # nó sẽ lấy hướng đi
            direction = getDirection(prev[0], seeker_pos)

            # di chuyển
            self.cur_map = recov_obser(mp=self.cur_map, loc=prev[3])
            self.cur_map = moveTiles(mp=self.cur_map, mv=direction, loc=prev[0])
            self.cur_map = assign_obser(mp=self.cur_map, loc=thing[3])

            tmp = (0, 0)
            if thing[4]:
                tmp = self.cur_map[thing[4][0]][thing[4][1]]
                self.cur_map[thing[4][0]][thing[4][1]] = 6
            # in ra màn hình
            self.printMap(score)
            # Recover the announcement position
            if thing[4]:
                self.cur_map[thing[4][0]][thing[4][1]] = tmp
            # cập nhật lại prev
            prev = thing
        self.score = score

    def runLevel2(self):
        map = Map(self.cur_map)
        if len(map.listHiderPositions) == 0:
            raise Exception("The map has no hider")

        game = Level2(map)

        listThings = game.level2()
        prev = next(listThings)

        for thing in listThings:
            score = thing[2]
            seeker_pos = thing[0]

            # nó sẽ lấy hướng đi
            direction = getDirection(prev[0], seeker_pos)

            # di chuyển
            self.cur_map = recov_obser(mp=self.cur_map, loc=prev[3])
            self.cur_map = moveTiles(mp=self.cur_map, mv=direction, loc=prev[0])
            self.cur_map = assign_obser(mp=self.cur_map, loc=thing[3])

            # Announcement
            tmp = []
            if thing[4]:
                for x, y in thing[4]:
                    tmp.append(self.cur_map[x][y])
                    self.cur_map[x][y] = 6

            # in ra màn hình
            self.printMap(score)

            if thing[4]:
                for i, (x, y) in enumerate(thing[4]):
                    self.cur_map[x][y] = tmp[i]

            # cập nhật lại prev
            prev = thing
        self.score = score

    def runLevel3(self):
        map = Map(self.cur_map)
        if len(map.listHiderPositions) == 0:
            raise Exception("The map has no hider")

        game = Level3(map)

        listThings = game.level3()
        prev = deepcopy(next(listThings))

        for cur in listThings:
            self.give_up = cur[-1]
            score = cur[2]
            directionSeeker = getDirection(prev[0], cur[0])
            directionHider = []
            hider_obv = []
            
            pt1, pt2 = 0, 0
            while pt1 < len(prev[1]) and pt2 < len(cur[1]):
                if prev[1][pt1] == cur[1][pt2]:
                    directionHider.append(getDirection(prev[1][pt1].state, cur[1][pt2].state))
                    hider_obv += cur[1][pt2].hiderObservableCells
                    pt1 += 1
                    pt2 += 1
                else:
                    pt1 += 1
            
            
            # for i in range(len(cur[1])):
            #     directionHider.append(getDirection(prev[1][i].state, cur[1][i].state))
            #     hider_obv += cur[1][i].hiderObservableCells

            # Move seeker
            self.cur_map = moveTiles(mp=self.cur_map, mv=directionSeeker, loc=prev[0])
            # Move hiders
            # for i in range(len(cur[1])):
            #     # print(prev[1][i].state, directionHider[i])
            #     self.cur_map = moveTiles(
            #         mp=self.cur_map,
            #         mv=directionHider[i],
            #         loc=prev[1][i].state,
            #         person=2,
            #     )
            pt1, pt2 = 0, 0
            while pt1 < len(prev[1]) and pt2 < len(cur[1]):
                if prev[1][pt1] == cur[1][pt2]:
                    self.cur_map = moveTiles(mp=self.cur_map, mv=directionHider[pt2], loc=prev[1][pt1].state, person=2)
                    pt1 += 1
                    pt2 += 1
                else:
                    pt1 += 1
            # new obser
            self.cur_map = assign_obser(mp=self.cur_map, loc=cur[3], person=SEEKER)
            self.cur_map = assign_obser(mp=self.cur_map, loc=hider_obv, person=HIDER)

            # Announcement
            tmp = []
            if cur[4]:
                for x, y in cur[4]:
                    tmp.append(self.cur_map[x][y])
                    self.cur_map[x][y] = 6
            self.printMap(score)

            self.cur_map = recov_obser(mp=self.cur_map, loc=cur[3])
            self.cur_map = recov_obser(mp=self.cur_map, loc=hider_obv)

            if self.give_up:
                break
            # Recover announcement
            if cur[4]:
                for i, (x, y) in enumerate(cur[4]):
                    self.cur_map[x][y] = tmp[i]
            prev = deepcopy(cur)
        self.score = score

    def printMap(self, score):
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                quit()
        mp = MapWidget(self.cur_map, self.level)
        txt = Text(
            text=f"Score: {score}",
            position=Vector2(WIDTH // 2 + 280, HEIGHT // 2 - 150),
            size=Vector2(180, 50),
            color=BLACK,
            font_size=26,
        )
        # print(str(self.widgets))
        self.widgets.pop("Text")
        self.widgets.pop("MapWidget")

        self.widgets.add(txt)
        self.widgets.add(mp)
        # print(str(self.widgets))

        # In lại ra màn hình
        self.widgets.__render__(self.display)
        pygame.display.flip()
        pygame.time.wait(DELAY_TIME)

    def getScore(self):
        return self.score

    def checkQuit(self):
        while not self.stop_event.is_set():
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    quit()
