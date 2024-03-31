import pygame
from pygame.math import Vector2

from UI.Configs.config import *


class Widget:
    """
    Widget is the base class for all widgets that can be display on the screen.
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
        # Create a rect object at the position with the size
        self.rect = pygame.Rect(position.xy, size.xy)

    def __render__(self, display):
        pass

    def __update__(self, event):
        pass


class WidgetGroup:
    """
    WidgetGroup is a collection of widgets that can be rendered and updated together.
    """
    def __init__(self):
        self.widgets: list["Widget"] = []
    # Add a widget to the group
    def add(self, widget: Widget):
        self.widgets.append(widget)
    # Remove a widget from the group
    def pop(self, name: str, text: str = None):
        if not text:
            for i in range(len(self.widgets)):
                if self.widgets[i].__class__.__name__ == name:
                    self.widgets.pop(i)
                    return
        for i in range(len(self.widgets)):
            if (
                self.widgets[i].__class__.__name__ == name
                and self.widgets[i].text == text
            ):
                self.widgets.pop(i)
                return
    # Clear all the widgets with the chosen name
    def pop_all(self, name: str):
        index = 0
        while index < len(self.widgets):
            if self.widgets[index].__class__.__name__ == name:
                self.widgets.pop(index)
            else:
                index += 1
    # Render all the widgets in the group
    def __render__(self, display):
        for widget in self.widgets:
            widget.__render__(display)
    # Update all the widgets in the group
    def __update__(self, event):
        for widget in self.widgets:
            widget.__update__(event)

    def __str__(self):
        s: str = ""
        for widget in self.widgets:
            s += widget.__class__.__name__
            try:
                s += f": {widget.text}\n"
            except:
                s += "\n"
        return s


class Button(Widget):
    """
    A button widget that can be clicked and perform a callback function when clicked.
    """
    def __init__(
        self,
        text: str = None,
        call: callable = None,
        size: Vector2 = None,
        position: Vector2 = Vector2(0, 0),
        font=FONT,
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
        if not self.text: # Need text
            return
        color = self.text_color
        # Change the color of the button when hovered
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

    # Handle events related to the button
    def __handle_events__(self, ev):
        if ev.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(
            pygame.mouse.get_pos()
        ):
            self.call()
            self.interactable = False


class Text(Widget):
    """
    Displaying text on the screen.
    """
    def __init__(
        self,
        text: str = None,
        position: Vector2 = Vector2(0, 0),
        size: Vector2 = None,
        font=FONT,
        font_size: int = 20,
        color: tuple = (255, 255, 255),
        backgr: bool = True,
    ):
        if text == None:
            raise Exception("Text must have a text")
        if font_size < 0:
            raise Exception("Font size must be greater than 0")

        super().__init__(position, size)
        self.text = text
        self.font = pygame.font.Font(font, font_size)
        self.color = color
        self.backgr = backgr

    def __render__(self, display):
        if not self.text: # Text must be present
            return

        text = self.font.render(self.text, True, self.color)
        if self.backgr: # Draw a background for the text
            pygame.draw.rect(display, (255, 255, 255), self.rect)

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
    """
    Displaying an image on the screen.
    """
    def __init__(
        self,
        src: str = None,
        position: Vector2 = Vector2(0, 0),
        scale: float = 1.0,
        rotate: int = 0,
    ):
        if src == None:
            raise Exception("Image must have an image")
        if scale <= 0:
            raise Exception("Scale must be positive")
        self.image = src
        self.scale = scale
        self.rotate = rotate

        self.__initiate__()
        self.size = Vector2(self.image.get_size()[0], self.image.get_size()[1])

        super().__init__(
            position, Vector2(self.image.get_size()[0], self.image.get_size()[1])
        )

    def __initiate__(self):
        """
        Load the image, scale it and rotate it.
        """
        self.image = pygame.image.load(self.image)
        self.image = pygame.transform.scale_by(self.image, self.scale)
        self.image = pygame.transform.rotate(self.image, self.rotate)

    def __render__(self, display):
        """
        Render the image on the screen.
        Args:
            display (pygame.display): The display object to render the image on.
        """
        display.blit(
            self.image,
            (
                self.position.x + self.size.x / 2 - self.image.get_width() / 2,
                self.position.y + self.size.y / 2 - self.image.get_height() / 2,
            ),
        )


# 1wall, 2hider, 3seeker, 4seeker observable
# 5obstacle, 6announce, 7hider observable, 8overlap
class MapWidget(Widget):
    def __init__(
        self, mp: list[int], level=1, position=Vector2(0, 0), size=Vector2(0, 0)
    ):
        super().__init__(position, size)
        self.map = mp
        self.level = level
        
        # The cell size is determined by the size of the map and the screen
        self.cell_size = HEIGHT // max(len(self.map), len(self.map[0]))
        # Placing the map in the center of the screen with alignment
        self.top_gap = (HEIGHT - len(self.map) * self.cell_size) // 2
        self.left_gap = (WIDTH - len(self.map[0]) * self.cell_size) // 2

    def __render__(self, display):
        for i in range(len(self.map)):
            for j in range(len(self.map[0])):
                color = BGC
                # Change color based on the attribute of the cell
                match self.map[i][j]:
                    case 8:
                        color = OVERLAPC
                    case 7:
                        color = HIDER_OBSERVABLEC
                    case 6:
                        color = ANNOUNCEC
                    case 5:
                        color = OBSTACLEC
                    case 4:
                        color = SEEKER_OBSERVABLEC
                    case 3:
                        color = SEEKERC
                    case 2:
                        color = HIDERC
                    case 1:
                        color = WALLC
                    case _:
                        pass
                block = pygame.Rect(
                    j * self.cell_size + self.left_gap - 150,
                    i * self.cell_size + self.top_gap,
                    self.cell_size,
                    self.cell_size,
                )
                # Draw the cell
                pygame.draw.rect(display, color, block)
                # Draw the border of the cell if it is player
                if color == HIDERC or color == SEEKERC:
                    pygame.draw.rect(display, BLACK, block, 1)

    def __update__(self, event):
        pass


class Legend(Widget):
    """
    A legend widget that displays the key words and their corresponding colors.
    """
    def __init__(
        self,
        position: Vector2 = Vector2(0, 0),
        size: Vector2 = None,
        level: int = 1,
        key_words: list[tuple[str, tuple[int]]] = None,
        font=FONT,
        font_size: int = 20,
        background: bool = False,
        offset_x: int = 0,
    ):
        super().__init__(position, size)
        if not key_words:
            raise Exception("Legend must have key words")
        if level < 3:
            key_words.pop(6)
        self.font = pygame.font.Font(font, font_size)
        self.key_words = key_words
        self.bg = background
        self.offx = offset_x

    def __render__(self, display):
        """
        Render the legend on the screen.
        Args:
            display (pygame.display): The display object to render the legend on.
        """
        line_height = self.font.get_height() + 5
        if self.bg:
            pygame.draw.rect(display, LEGEND_BGC, self.rect)
            pygame.draw.rect(display, BLACK, self.rect, 2)

        display.blit(
            self.font.render("Legend", True, BLACK),
            (self.position.x + 90, self.position.y + 5),
        )
        for i, (key, color) in enumerate(self.key_words, 1):
            text = self.font.render(key, True, BLACK)
            display.blit(
                text,
                (
                    self.position.x + 5 + 35 + self.offx,
                    self.position.y + i * line_height + 5,
                ),
            )
            pygame.draw.rect(
                display,
                color,
                (
                    self.position.x + 5 + self.offx,
                    self.position.y + i * line_height + 5,
                    self.font.get_height(),
                    self.font.get_height(),
                ),
            )
