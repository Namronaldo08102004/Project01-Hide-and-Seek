import pygame
from Configs.config import *
from Screen.Screen import Screen
from Screen.DisplayMap import *
from Utils.getMap import *
from Utils.move import *
from Widget.widget import *

class RunScreen(Screen):
    def __init__(self, level: int = 1, display=None):
        super().__init__()
        self.level = level
        pygame.display.set_caption(f"Hide and Seek - Level {level}")
        self.display = display
        
        self.old_score = 0

    def __initiate__(self):
        super().__initiate__()
        self.drop_open = False
        self.select = -1
        self.available_maps = list_map("Maps")
        self.cur_map = None
        self.__update__(pygame.event.Event(pygame.NOEVENT))

    def __update__(self, event):
        self.widgets = WidgetGroup()
        if self.old_score != 0:
            txt = Text(
                text=f"Score: {self.old_score}",
                position=Vector2(WIDTH // 2 + 300, HEIGHT // 2 + 200),
                size=Vector2(120, 50),
                color=BLACK,
                font_size=26,
            )
            self.widgets.add(txt)
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
        self.old_score = 0
        
    def begin_move(self):
        run = DisplayMap(self.cur_map, self.level, self.display, self.widgets)
        self.old_score = run.getScore()
        
    def pausing(self):
        pass
    
