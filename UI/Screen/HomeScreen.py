from Configs.config import *
from Screen.Screen import Screen
from Widget.widget import *


class HomeScreen(Screen):
    def __init__(self):
        super().__init__()

    def __initiate__(self):
        super().__initiate__()

        self.image = Image("Assets/HideNSeek.png", Vector2(WIDTH // 2 - 150, 30), 1 / 2)

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
        super().__render__(display)
        self.widgets.__render__(display)

    def callback(self, txt: str = None):
        if txt == "Quit":
            self.level = 5
        else:
            self.level = int(txt.split(" ")[-1])
        
        #! temp return
        if self.level != 1:
            print("Level not available")
            self.level = 5
        return
