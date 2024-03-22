import pygame
from Configs.config import *
from pygame.math import Vector2
from Widget.widget import *


class Screen:
    def __init__(self, background: str = None):
        if self.__class__.__name__ == "Screen":
            raise Exception("Screen cannot be instantiated")

        self.background = background
        self.level = -1

    def __initiate__(self):
        if not self.background:
            self.background = pygame.image.load("Assets/BG.webp")
            self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))

        self.widgets = WidgetGroup()

    def __update__(self, event):
        self.widgets.__update__(event)

    def __render__(self, display):
        display.blit(self.background, (0, 0))
        self.widgets.__render__(display)
