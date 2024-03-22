import pygame
from Configs.config import *
from pygame.math import Vector2


class Widget:
    """
    Widget is the base class for all widgets.
    position: Vector2 - the position of the widget
    size: Vector2 - the size of the widget
    """

    def __init__(self, position: Vector2, size: Vector2):
        if self.__class__.__name__ == "Widget":
            raise Exception("Widget cannot be instantiated")
        if position == None:
            raise Exception("Widget must have a position")
        if size == None:
            raise Exception("Widget must have a size")

        self.position = position
        self.size = size
        self.rect = pygame.Rect(position.xy, size.xy)

    def __render__(self, display):
        pass

    def __update__(self, event):
        pass


class WidgetGroup:
    def __init__(self):
        self.widgets: list["Widget"] = []

    def add(self, widget: Widget):
        self.widgets.append(widget)

    def pop(self, name: str):
        for i in range(len(self.widgets)):
            if self.widgets[i].__class__.__name__ == name:
                self.widgets.pop(i)
                break

    def __render__(self, display):
        for widget in self.widgets:
            widget.__render__(display)

    def __update__(self, event):
        for widget in self.widgets:
            widget.__update__(event)
    
    def __str__(self):
        s: str = ""
        for widget in self.widgets:
            s += widget.__class__.__name__ + "\t"
        return s


class Button(Widget):
    def __init__(
        self,
        text: str = None,
        call: callable = None,
        size: Vector2 = None,
        position: Vector2 = Vector2(0, 0),
        font="OpenSans-Regular.ttf",
        font_size: int = 20,
        color: tuple = (255, 255, 255),
        hover_color: tuple = (255, 0, 0),
        delay_time: int = 1,
    ):
        super().__init__(position, size)
        if text == None:
            raise Exception("Button must have a text")
        if not callable(call):
            raise Exception("Callback must be callable")
        if delay_time < 0:
            raise Exception("Delay time must be greater than 0")
        if font_size < 0:
            raise Exception("Font size must be greater than 0")
        self.call = call
        self.font = pygame.font.Font(font, font_size)
        self.text_color = color
        self.hover = hover_color
        self.text = text
        self.delay_time = delay_time
        self.interactable = True
        self.interact_time = 2

    def __render__(self, display):
        if not self.text:
            return
        color = self.text_color
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            color = self.hover
        # render the text in the center of the button
        text = self.font.render(self.text, True, color)
        # pygame.draw.rect(display, (0, 0, 0), self.rect, 2)
        display.blit(
            text,
            (
                self.position.x + self.size.x / 2 - text.get_width() / 2,
                self.position.y + self.size.y / 2 - text.get_height() / 2,
            ),
        )

    def __update__(self, event):
        if not self.interactable:  # Reset the interactable state after a delay
            self.interact_time -= 1 / 60
            if self.interact_time <= 0:
                self.interactable = True
                self.interact_time = 2
            return
        self.__handle_events__(event)

    def __handle_events__(self, ev):
        if ev.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(
            pygame.mouse.get_pos()
        ):
            self.call()
            self.interactable = False


class Text(Widget):
    def __init__(
        self,
        text: str = None,
        position: Vector2 = Vector2(0, 0),
        size: Vector2 = None,
        font="OpenSans-Regular.ttf",
        font_size: int = 20,
        color: tuple = (255, 255, 255),
    ):
        if text == None:
            raise Exception("Text must have a text")
        if font_size < 0:
            raise Exception("Font size must be greater than 0")

        super().__init__(position, size)
        self.text = text
        self.font = pygame.font.Font(font, font_size)
        self.color = color

    def __render__(self, display):
        if not self.text:
            return

        text = self.font.render(self.text, True, self.color)
        display.blit(
            text,
            (
                self.position.x + self.size.x / 2 - text.get_width() / 2,
                self.position.y + self.size.y / 2 - text.get_height() / 2,
            ),
        )

    def __update__(self, event):
        pass


class Image(Widget):
    def __init__(
        self, src: str = None, position: Vector2 = Vector2(0, 0), scale: float = 1.0
    ):
        if src == None:
            raise Exception("Image must have an image")
        if scale <= 0:
            raise Exception("Scale must be positive")
        self.image = src
        self.scale = scale

        self.__initiate__()
        self.size = Vector2(self.image.get_size()[0], self.image.get_size()[1])

        super().__init__(
            position, Vector2(self.image.get_size()[0], self.image.get_size()[1])
        )

    def __initiate__(self):
        self.image = pygame.image.load(self.image)
        self.image = pygame.transform.scale_by(self.image, self.scale)

    def __render__(self, display):
        display.blit(
            self.image,
            (
                self.position.x + self.size.x / 2 - self.image.get_width() / 2,
                self.position.y + self.size.y / 2 - self.image.get_height() / 2,
            ),
        )


class MapWidget(Widget):
    def __init__(
        self, mp: list[int], level=1, position=Vector2(0, 0), size=Vector2(0, 0)
    ):
        super().__init__(position, size)
        self.map = mp
        self.level = level

        self.cell_size = 600 // max(len(self.map), len(self.map[0]))
        self.top_gap = (HEIGHT - len(self.map) * self.cell_size) // 2
        self.left_gap = (WIDTH - len(self.map[0]) * self.cell_size) // 2

    def __render__(self, display):
        for i in range(len(self.map)):
            for j in range(len(self.map[0])):
                color = BGC
                match self.map[i][j]:
                    case 1:
                        color = WALLC
                    case 2:
                        color = HIDERC
                    case 3:
                        color = SEEKERC
                    case 4:
                        color = OBSERVABLEC
                    case 5:
                        color = OBSTACLEC
                    case _:
                        pass
                block = pygame.Rect(
                    j * self.cell_size + self.left_gap - 150,
                    i * self.cell_size + self.top_gap,
                    self.cell_size,
                    self.cell_size,
                )
                pygame.draw.rect(display, color, block)

    def __update__(self, event):
        pass
