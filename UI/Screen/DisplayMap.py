# import multiprocessing as mtpc
import threading

import pygame
from Configs.config import *
from Source.Level1 import *
from Source.Level2 import *
from Utils.move import *
from Widget.widget import *


class DisplayMap:
    def __init__(self, cur_map, level, display, widgets):
        self.cur_map = cur_map
        self.level = level
        self.display = display
        self.widgets = widgets

        self.score = 0

        self.stop_event = threading.Event()
        self.thread1 = threading.Thread(target=self.redirect)
        self.thread2 = threading.Thread(target=self.checkQuit)

        # self.thread1.start()
        # self.thread2.start()
        # self.thread1.join()
        # self.thread2.join()
        # self.event.wait()
        self.redirect()

    def redirect(self):
        if self.level == 1:
            self.runLevel1()
        elif self.level == 2:
            self.runLevel2()
        # elif self.level == 3:
        #     self.runLevel3()
        # elif self.level == 4:
        #     self.runLevel4()
        self.stop_event.set()

    def runLevel1(self):
        map = Map(self.cur_map)
        if (len(map.listHiderPositions) != 1):
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
        
    def runLevel2 (self):
        map = Map(self.cur_map)
        if (len(map.listHiderPositions) < 2):
                raise Exception("This is not a map for Level 2")
        
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
            # in ra màn hình
            self.printMap(score)

            # cập nhật lại prev
            prev = thing
        self.score = score

    def printMap(self, score):
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                quit()
        mp = MapWidget(self.cur_map, self.level)
        txt = Text(
            text=f"Score: {score}",
            position=Vector2(WIDTH // 2 + 300, HEIGHT // 2 + 200),
            size=Vector2(150, 50),
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
