import pygame

from UI.Configs.config import *
from UI.Screen.DisplayMap import *
from UI.Screen.Screen import Screen
from UI.Utils.getMap import *
from UI.Utils.move import *
from UI.Widget.widget import *


class RunScreen(Screen):
    """
    This class is used to select maps and allow the game to run.
    """
    def __init__(self, level: int = 1, display=None):
        super().__init__()
        self.level = level
        pygame.display.set_caption(f"Hide and Seek - Level {level}")
        self.display = display

        self.old_score = 0
        self.back2HC = False
        self.ran = False
        self.give_up = False

    def __initiate__(self):
        """
        Load available maps and initiate the screen.
        """
        super().__initiate__()
        self.drop_open = False
        self.select = -1
        self.file_path = "Maps/" + (
            "Single_Hider" if self.level == 1 else "Multi_Hiders"
        )
        self.available_maps = list_map(self.file_path)
        self.cur_map = None
        self.__update__(pygame.event.Event(pygame.NOEVENT))

    def __update__(self, event):
        """
        Update the screen based on the event.
        Args:
            event (pygame.event): the event that the user triggered
        """
        self.widgets = WidgetGroup()
        # Show the back button if the map list is not open
        if not self.drop_open:
            back = Button(
                text="Back",
                position=Vector2(WIDTH - 280, HEIGHT - 100),
                size=Vector2(100, 40),
                call=lambda: self.backing(),
                color=BLACK,
                hover_color=HOVER,
                font_size=30,
            )
            self.widgets.add(back)
        # Show the selected map
        if self.select != -1 and self.cur_map:
            mp = MapWidget(self.cur_map, self.level)
            self.widgets.add(mp)
            if not self.drop_open:
                start = Button(
                    text="Begin" if not self.ran else "Restart",
                    position=Vector2(WIDTH - 150, HEIGHT - 100),
                    size=Vector2(100, 40),
                    call=lambda: self.begin_move() if not self.ran else self.restart(),
                    color=BLACK,
                    hover_color=HOVER,
                    font_size=30,
                )
                self.widgets.add(start)
        # If the game has stopped and the seeker gives up
        if self.ran and self.give_up and not self.drop_open:
            txt = Text(
                text="Seeker gives up",
                position=Vector2(WIDTH // 2 + 283, HEIGHT // 2 + 190),
                size=Vector2(180, 50),
                color=RED,
                font_size=30,
                backgr=False,
            )
            self.widgets.add(txt)
        # Show the score of the last game
        if self.old_score != 0 and not self.drop_open:
            txt = Text(
                text=f"Score: {self.old_score}",
                position=Vector2(WIDTH // 2 + 280, HEIGHT // 2 - 150),
                size=Vector2(180, 50),
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
            position=Vector2(WIDTH // 2 + 300, HEIGHT // 2 - 150 - 50),
            size=Vector2(180, 50),
            call=lambda: self.drop(),
            color=BLACK,
            hover_color=HOVER,
            font_size=26,
        )
        self.widgets.add(self.drop_down_box)
        triangle = Image(
            src="UI/Assets/UpsideDownTri.png",
            position=Vector2(WIDTH // 2 + 235, HEIGHT // 2 - 150 - 53),
            # size=Vector2(50, 50),
            scale=0.3,
            rotate=0 if self.drop_open else 90,
        )
        self.widgets.add(triangle)
        if self.drop_open:
            # All available maps to be chosen
            for i in range(len(self.available_maps)):
                but = Button(
                    text=self.available_maps[i],
                    position=Vector2(WIDTH // 2 + 300, HEIGHT // 2 - 150 + i * 40),
                    size=Vector2(120, 40),
                    call=lambda i=i: self.load_map(i),
                    color=BLACK,
                    hover_color=HOVER,
                    font_size=26,
                )
                self.widgets.add(but)
        else:
            # The graph color legend
            legend = Legend(
                position=Vector2(WIDTH // 2 + 276, HEIGHT // 2 - 80),
                size=Vector2(193, 245) if self.level <= 2 else Vector2(193, 270),
                level=self.level,
                font_size=20,
                key_words=[
                    ("Wall", WALLC),
                    ("Obstacle", OBSTACLEC),
                    ("Announcement", ANNOUNCEC),
                    ("Hider", HIDERC),
                    ("Seeker", SEEKERC),
                    ("Seeker's Vision", SEEKER_OBSERVABLEC),
                    ("Hiders' Vision", HIDER_OBSERVABLEC),
                ],
                font=FONT2,
                background=True,
                offset_x=3,
            )
            self.widgets.add(legend)

        self.widgets.__update__(event)

    # Render all the current widgets on the chosen display
    def __render__(self, display):
        super().__render__(display)
        self.widgets.__render__(display)
        # print(str(self.widgets))

    def drop(self):
        self.drop_open = not self.drop_open
    # Read the selected map and prepare the game to run
    def load_map(self, i):
        self.cur_map = read_map(f"{self.file_path}/{self.available_maps[i]}")
        self.drop_open = False
        self.select = i + 1
        self.old_score = 0
        self.ran = False

    def backing(self):
        self.back2HC = True
    # Start the game, allow each step to be printed on the screen
    def begin_move(self):
        if self.level == 4:
            print("Level 4 has not been implemented yet")
            return
        run = DisplayMap(self.cur_map, self.level, self.display, self.widgets)
        self.old_score, self.give_up = run.getResult()
        self.ran = True
        self.__update__(pygame.event.Event(pygame.NOEVENT))
    # If the game is over, load the game again, prepare for the next game
    def restart(self):
        self.old_score = 0
        self.ran = False
        self.cur_map = read_map(
            f"{self.file_path}/{self.available_maps[self.select-1]}"
        )

    def pausing(self):
        pass
