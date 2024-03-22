import pygame
from Configs.config import *
from Screen.HomeScreen import HomeScreen
from Screen.RunScreen import RunScreen


class App:
    def __init__(self):
        self.display = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Hide and Seek")
        self.clock = pygame.time.Clock()
        self.isRunning = True
        pygame.init()
        self.screen_queue = []

    def __initiate__(self, screen):
        self.screen_queue.append(screen)
        self.screen_queue[-1].__initiate__()

    def __render__(self, display):
        self.screen_queue[-1].__render__(display)
        pygame.display.flip()

    def __update__(self, event):
        self.screen_queue[-1].__update__(event)

    def change_screen(self):
        if self.screen_queue[-1].__class__.__name__ == "HomeScreen":
            if self.screen_queue[-1].level == 5:
                self.isRunning = False
            elif self.screen_queue[-1].level != -1:
                self.screen_queue.append(RunScreen(self.screen_queue[-1].level, self.display))
                self.screen_queue[-1].__initiate__()

    def run(self):
        while self.isRunning:
            self.handle_events()
            self.__render__(self.display)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.isRunning = False
                pygame.quit()
                quit()
            else:
                self.__update__(event)

        self.change_screen()


app = App()
app.__initiate__(HomeScreen())
app.run()
