import pygame

from UI.Configs.config import *
from UI.Screen.HomeScreen import HomeScreen
from UI.Screen.RunScreen import RunScreen


class App:
    """
    The main class of the application. It is responsible for handling the main loop of the game.
    """
    def __init__(self):
        """
        Initializes the display, clock, and the screen queue.
        It also initiates the HomeScreen.
        """
        self.display = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.isRunning = True
        pygame.init()
        self.screen_queue = []
        
        self.__initiate__(HomeScreen())

    def __initiate__(self, screen):
        """
        Add the screen to the screen queue and initiate it.
        """
        self.screen_queue.append(screen)
        self.screen_queue[-1].__initiate__()

    def __render__(self, display):
        """
        Render the latest screen in the screen queue.
        """
        self.screen_queue[-1].__render__(display)
        pygame.display.flip()

    def __update__(self, event):
        """
        Update the latest screen in the screen queue with the inputing event.
        """
        self.screen_queue[-1].__update__(event)

    def change_screen(self):
        """
        Change the screen based on the current screen.
        If the HomeScreen is run and the level is not -1, then add a RunScreen to the screen queue.
        """
        
        # If the current screen is HomeScreen
        # and the level is not -1
        if self.screen_queue[-1].__class__.__name__ == "HomeScreen":
            if self.screen_queue[-1].level == 5:
                self.isRunning = False
            elif self.screen_queue[-1].level != -1:
                self.screen_queue.append(
                    RunScreen(self.screen_queue[-1].level, self.display)
                )
                self.screen_queue[-1].__initiate__()
        # The back button is clicked, return to homescreen
        elif self.screen_queue[-1].__class__.__name__ == "RunScreen":
            if self.screen_queue[-1].back2HC:
                self.screen_queue.pop()
                self.screen_queue[-1].__initiate__()

    def run(self):
        """
        The main loop of the application.
        """
        while self.isRunning:
            self.handle_events()
            self.__render__(self.display)

    def handle_events(self):
        """
        Handle the events of the application.
        Includes the quit event and user events.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.isRunning = False
                pygame.quit()
                quit()
            else:
                self.__update__(event)

        self.change_screen()