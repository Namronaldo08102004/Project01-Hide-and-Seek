import sys

import pygame

HEIGHT, WIDTH = 720, 1080
WHITE, BLACK = (255, 255, 255), (0, 0, 0)
RED, GREEN, BLUE = (255, 0, 0), (0, 255, 0), (0, 0, 255)

texts = ["Level 1", "Level 2", "Level 3", "Level 4", "About", "Quit"]

class HOME:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.font = pygame.font.Font(None, 36)
        self.clock = pygame.time.Clock()

        self.image = pygame.image.load("Assets/HideNSeek.png").convert_alpha()
        self.image = pygame.transform.scale_by(self.image, 1 / 2)
        self.background = pygame.image.load("Assets/BG.webp")
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))

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
            color = RED if rect.collidepoint(pygame.mouse.get_pos()) else BLACK
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

