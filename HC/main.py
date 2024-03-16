import pygame

pygame.init()
screen = pygame.display.set_mode((1080, 720))
clock = pygame.time.Clock()


lst = []
file_name = "map1.txt"
with open(file_name, "r") as f:
    row, col = f.readline().split()
    row, col = int(row), int(col)
    for _ in range(row):
        lst.append(list(f.readline().split()))

cell_size = 600 // max(len(lst), len(lst[0]))
top = (720 - cell_size * len(lst)) / 2
left = (720 - cell_size * len(lst[0])) / 2

while True:
    for i in range(len(lst)):
        for j in range(len(lst[0])):
            color = (122, 122, 122)
            if lst[i][j] == "3":
                color = (255, 0, 0)
            elif lst[i][j] == "1":
                color = (0, 0, 255)
            elif lst[i][j] == "2":
                color = (0, 255, 0)
            block = pygame.Rect(
                j * cell_size + left, i * cell_size + top, cell_size, cell_size
            )
            pygame.draw.rect(screen, color, block)
    pygame.display.flip()
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
