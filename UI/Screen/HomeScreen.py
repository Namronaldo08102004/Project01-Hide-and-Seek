from UI.Configs.config import *
from UI.Screen.Screen import Screen
from UI.Widget.widget import *


class HomeScreen(Screen):
    """
    HomeScreen class is used to display the home screen of the game.
    Allow user to select the desired level to play.
    """

    def __init__(self):
        super().__init__()

    def __initiate__(self):
        """
        Initiate the home screen.
        Create buttons for the user to select the level or quit.
        """
        super().__initiate__()
        pygame.display.set_caption("Hide and Seek")

        self.image = Image(
            "UI/Assets/HideNSeek.png", Vector2(WIDTH // 2 - 150, 30), 1 / 2
        )
        self.level = -1

        w = WIDTH // 2 - 50
        h = HEIGHT // 2 + 20
        color = BLACK
        font_size = 26
        step = 40
        self.lv1 = Button(
            text="Level 1",
            position=Vector2(w, h),
            size=Vector2(100, 40),
            call=lambda: self.callback("Level 1"),
            color=color,
            hover_color=HOVER,
            font_size=font_size,
        )
        self.lv2 = Button(
            text="Level 2",
            position=Vector2(w, h + step),
            size=Vector2(100, 40),
            call=lambda: self.callback("Level 2"),
            color=color,
            hover_color=HOVER,
            font_size=font_size,
        )
        self.lv3 = Button(
            text="Level 3",
            position=Vector2(w, h + step * 2),
            size=Vector2(100, 40),
            call=lambda: self.callback("Level 3"),
            color=color,
            hover_color=HOVER,
            font_size=font_size,
        )
        self.lv4 = Button(
            text="Level 4",
            position=Vector2(w, h + step * 3),
            size=Vector2(100, 40),
            call=lambda: self.callback("Level 4"),
            color=color,
            hover_color=HOVER,
            font_size=font_size,
        )
        self.quit = Button(
            text="Quit",
            position=Vector2(w, h + step * 4),
            size=Vector2(100, 40),
            call=lambda: self.callback("Quit"),
            color=color,
            hover_color=(250, 98, 98),
            font_size=font_size,
        )
        # self.widgets.add(self.background)
        self.widgets.add(self.image)
        self.widgets.add(self.lv1)
        self.widgets.add(self.lv2)
        self.widgets.add(self.lv3)
        self.widgets.add(self.lv4)
        self.widgets.add(self.quit)

    def __render__(self, display):
        """
        Render the home screen on the display.
        """
        super().__render__(display)
        self.widgets.__render__(display)

    def callback(self, txt: str = None):
        """
        If the button is clicked, update the level.
        Args:
            txt (str, optional): The chosen level. Defaults to None.
        """
        if txt == "Quit":
            self.level = 5
        else:
            self.level = int(txt.split(" ")[-1])

        if self.level not in {1, 2, 3, 4}:
            print("Level not available")
            self.level = 5
        return
