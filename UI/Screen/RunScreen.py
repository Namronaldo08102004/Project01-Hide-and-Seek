import pygame
from Configs.config import *
from Screen.Screen import Screen
from Utils.getMap import *
from Utils.move import *
from Widget.widget import *
from Source.Level1 import *


class RunScreen(Screen):
    def __init__(self, level: int = 1, display=None):
        super().__init__()
        self.level = level
        pygame.display.set_caption(f"Hide and Seek - Level {level}")
        self.display = display

    def __initiate__(self):
        super().__initiate__()
        self.drop_open = False
        self.select = -1
        self.available_maps = list_map("Maps")
        self.cur_map = None
        self.__update__(pygame.event.Event(pygame.NOEVENT))

    def __update__(self, event):
        self.widgets = WidgetGroup()
        self.drop_down_box = Button(
            text=(
                "Select Map"
                if self.select == -1
                else self.available_maps[self.select - 1]
            ),
            position=Vector2(WIDTH // 2 + 300, HEIGHT // 2 - 100 - 50),
            size=Vector2(120, 50),
            call=lambda: self.drop(),
            color=BLACK,
            hover_color=HOVER,
            font_size=26,
        )
        self.widgets.add(self.drop_down_box)
        if self.drop_open:
            for i in range(len(self.available_maps)):
                but = Button(
                    text=self.available_maps[i],
                    position=Vector2(WIDTH // 2 + 300, HEIGHT // 2 - 100 + i * 40),
                    size=Vector2(120, 40),
                    call=lambda i=i: self.load_map(i),
                    color=BLACK,
                    hover_color=HOVER,
                    font_size=26,
                )
                self.widgets.add(but)
        if self.select != -1 and self.cur_map:
            mp = MapWidget(self.cur_map, self.level)
            self.widgets.add(mp)
            if not self.drop_open:
                start = Button(
                    text="Begin",
                    position=Vector2(WIDTH // 2 + 300, HEIGHT // 2 + 100),
                    size=Vector2(120, 50),
                    call=lambda: self.begin_move(),
                    color=BLACK,
                    hover_color=HOVER,
                    font_size=26,
                )
                self.widgets.add(start)

        self.widgets.__update__(event)

    def __render__(self, display):
        super().__render__(display)
        self.widgets.__render__(display)
        # print(str(self.widgets))

    def drop(self):
        self.drop_open = not self.drop_open

    def load_map(self, i):
        self.cur_map = read_map(f"Maps/{self.available_maps[i]}")
        self.drop_open = False
        self.select = i + 1

    # hàm này nó sẽ gọi khi bấm nút start
    # Data hiện đag có sẽ là level và cái map đã đọc sẵn theo format 1, 2, 3, 4, 5
    def begin_move(self):
        game = None
        if (self.level == 1):
            map = Map(self.cur_map)
            game = Level1(map)
            
            listThings = game.level1()
            first = next(listThings)
            
            for thing in listThings:
                score = thing[2]
                seeker_pos = thing[0]
                
                # nó sẽ lấy hướng đi
                direction = getDirection(first[0], seeker_pos)
                
                # di chuyển
                self.cur_map = moveTiles(mp=self.cur_map, mv=direction, loc=first[0])
                
                # in ra màn hình
                self.printMap(score)
                
                # cập nhật lại first
                first = thing
        else:
            return
    
    def printMap (self, score):
        mp = MapWidget(self.cur_map, self.level)
        mp.__render__(self.display)
        txt = Text(
            text=f"Score: {score}",
            position=Vector2(WIDTH // 2 + 300, HEIGHT // 2 + 200),
            size=Vector2(120, 50),
            color=BLACK,
            font_size=26,
        )
        txt.__render__(self.display)
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