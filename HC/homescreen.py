import os
import sys

import pygame

HEIGHT, WIDTH = 720, 1080
WHITE, BLACK = (255, 255, 255), (0, 0, 0)
RED, GREEN, BLUE = (255, 0, 0), (0, 255, 0), (0, 0, 255)

hover = (30, 233, 240)
BG = (235, 215, 232)
WALL = (31, 161, 212)
SEEKER = (236, 84, 37)
HIDER = (53, 228, 94)
PATH = (223, 117, 69)

texts = ["Level 1", "Level 2", "Level 3", "Level 4", "About", "Quit"]


class HOME:
    def __init__(
        self, screen: pygame.Surface, font: pygame.font.Font, background: pygame.Surface
    ):
        self.screen = screen
        self.font = font
        self.background = background
        self.image = pygame.image.load("Assets/HideNSeek.png").convert_alpha()
        self.image = pygame.transform.scale_by(self.image, 1 / 2)

        self.text_renders = [self.font.render(text, True, BLACK) for text in texts]
        self.text_rects = [
            text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50 + i * 40))
            for i, text in enumerate(self.text_renders)
        ]
        self.selected = -1

    def Quit(self):
        pygame.quit()
        sys.exit()

    def Selecting(self):
        for i, (rend, rect) in enumerate(zip(self.text_renders, self.text_rects)):
            # hover = rect.collidepoint(pygame.mouse.get_pos())
            color = hover if rect.collidepoint(pygame.mouse.get_pos()) else BLACK
            rend = self.font.render(texts[i], True, color)

            self.screen.blit(rend, rect)

    def Run(self) -> int:
        running = True
        while running:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    running = False
                elif ev.type == pygame.MOUSEBUTTONDOWN and self.selected == -1:
                    for i, text_rect in enumerate(self.text_rects):
                        if text_rect.collidepoint(ev.pos):
                            self.selected = i
            # self.screen.fill(WHITE)
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(
                self.image, (WIDTH // 2 - self.image.get_size()[0] // 2, 30)
            )

            if self.selected == -1:
                self.Selecting()
            else:
                return self.selected
            pygame.display.flip()

        self.Quit()


def move(mp: list, move: str = 'd'):
    # step = 0
    # mv = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
    cur = (0, 0)
    for i in range(len(mp)):
        for j in range(len(mp[0])):
            if mp[i][j] == "3":
                cur = (i, j)
    if cur[0] == len(mp) - 1:
        return mp
    if move == "d":
        mp[cur[0]][cur[-1]], mp[cur[0] + 1][cur[-1]] = (
            mp[cur[0] + 1][cur[-1]],
            mp[cur[0]][cur[-1]],
        )
    elif move == 'l':
        mp[cur[0]][cur[-1]], mp[cur[0]][cur[-1] - 1] = (
            mp[cur[0]][cur[-1] - 1],
            mp[cur[0]][cur[-1]],
        )
    elif move == 'r':
        mp[cur[0]][cur[-1]], mp[cur[0]][cur[-1] + 1] = (
            mp[cur[0]][cur[-1] + 1],
            mp[cur[0]][cur[-1]],
        )
    return mp


class Map:
    def __init__(
        self,
        screen: pygame.Surface,
        font: pygame.font.Font,
        background: pygame.Surface,
        level: int = 1,
        drop_down_rect: pygame.Rect = None,
    ):
        self.screen = screen
        self.font = font
        self.background = background
        self.map = []
        self.row, self.col = 0, 0

        self.cell_size, self.top_border, self.left_border = 0, 0, 0

        self.level = level
        self.available_maps = []
        self.selected_map = None
        self.drop_open = False
        self.drop_down_rect = drop_down_rect
        self.find_map()

    def find_map(self):
        folder = "Level" + str(self.level)
        files = os.listdir(folder)
        self.available_maps = [f for f in files if f.endswith(".txt")]

    def choose_map(self):
        while True:
            pygame.draw.rect(self.screen, WHITE, self.drop_down_rect)
            pygame.draw.rect(self.screen, BLACK, self.drop_down_rect, 2)
            s = (
                self.available_maps[self.selected_map]
                if self.selected_map is not None
                else "Select"
            )

            text = self.font.render(s, True, BLACK)
            text_rect = text.get_rect(center=self.drop_down_rect.center)
            self.screen.blit(text, text_rect)

            if self.drop_open:
                opt_rect = []
                for i, opt in enumerate(self.available_maps):
                    rect = pygame.Rect(
                        self.drop_down_rect.left,
                        self.drop_down_rect.bottom + i * self.drop_down_rect.height,
                        self.drop_down_rect.width,
                        self.drop_down_rect.height,
                    )
                    pygame.draw.rect(self.screen, WHITE, rect)
                    pygame.draw.rect(self.screen, BLACK, rect, 2)
                    text = self.font.render(opt, True, BLACK)
                    text_rect = text.get_rect(center=rect.center)
                    self.screen.blit(text, text_rect)
                    opt_rect.append(rect)
                self.opt_rect = opt_rect
            break

    def load_button(self, button: pygame.Rect):
        # pygame.draw.rect(self.screen, WHITE, button)
        # pygame.draw.rect(self.screen, BLACK, button, 2)
        text = self.font.render("Load", True, BLACK)
        text_rect = text.get_rect(center=button.center)
        self.screen.blit(text, text_rect)

    def load_map(self) -> bool:
        if self.selected_map is None:
            return False
        path = "Level" + str(self.level) + "/" + self.available_maps[self.selected_map]
        with open(path, "r") as f:
            self.row, self.col = f.readline().split()
            self.row, self.col = int(self.row), int(self.col)
            self.map = []
            for _ in range(self.row):
                self.map.append(list(f.readline().split()))

        self.cell_size = 600 // max(len(self.map), len(self.map[0]))
        self.top = (HEIGHT - self.cell_size * len(self.map)) / 2
        self.left = (HEIGHT - self.cell_size * len(self.map[0])) / 2
        return True

    def draw_map(self):
        for i in range(len(self.map)):
            for j in range(len(self.map[0])):
                color = BG  # grey
                if self.map[i][j] == "1":
                    color = WALL
                elif self.map[i][j] == "2":
                    color = HIDER
                elif self.map[i][j] == "3":
                    color = SEEKER
                block = pygame.Rect(
                    j * self.cell_size + self.left,
                    i * self.cell_size + self.top,
                    self.cell_size,
                    self.cell_size,
                )
                pygame.draw.rect(self.screen, color, block)

    def start_(self, button: pygame.Rect):
        pygame.draw.rect(self.screen, WHITE, button)
        pygame.draw.rect(self.screen, BLACK, button, 2)
        text = self.font.render("Start", True, BLACK)
        text_rect = text.get_rect(center=button.center)
        self.screen.blit(text, text_rect)

    def start_game(self):
        for _ in range(10):
            move(self.map)
            self.draw_map()
            pygame.time.delay(250)
            pygame.display.flip()
        for _ in range(10):
            move(self.map, 'r')
            self.draw_map()
            pygame.time.delay(250)
            pygame.display.flip()


class Display:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.font = pygame.font.Font(None, 36)
        self.clock = pygame.time.Clock()

        self.background = pygame.image.load("Assets/BG.webp")
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))

        self.homeScreen = HOME(self.screen, self.font, self.background)

        self.drop_down_rect = pygame.Rect(800, 250, 150, 50)
        self.map = Map(self.screen, self.font, self.background, 1, self.drop_down_rect)
        self.level = -1

    def intro(self):
        self.level = self.homeScreen.Run()

    def run(self):
        self.intro()
        load_button = pygame.Rect(800, 300, 150, 50)
        start_button = pygame.Rect(800, 400, 150, 50)
        i = 1
        while True:
            update = False
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif ev.type == pygame.MOUSEBUTTONDOWN:
                    update = True
                    if self.drop_down_rect.collidepoint(ev.pos):
                        self.map.drop_open = not self.map.drop_open
                    elif self.map.drop_open:
                        for i, rect in enumerate(self.map.opt_rect):
                            if rect.collidepoint(ev.pos):
                                self.map.selected_map = i
                                self.map.drop_open = False
                                break
                    elif load_button.collidepoint(ev.pos):
                        self.map.load_map()

                    elif (
                        start_button.collidepoint(ev.pos)
                        and self.map.selected_map is not None
                    ):
                        self.map.start_game()
                        update = False

            if update or i == 1:
                i -= 1
                self.screen.blit(self.background, (0, 0))
                self.map.choose_map()
                if not self.map.drop_open:
                    self.map.load_button(load_button)
                    self.map.start_(start_button)
                self.map.draw_map()
                pygame.display.flip()
                self.clock.tick(60)


if __name__ == "__main__":
    puzzle = Display()
    puzzle.run()
