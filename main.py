import pygame
import random
# Määrab värvid
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# See määrab iga ruudustiku asukoha LAIUSE ja KÕRGUSE
WIDTH = 20
HEIGHT = 20

# See määrab iga lahtri vahelise veerise
MARGIN = 5

# Loo 2-mõõtmeline massiiv
grid = []
for row in range(10):
        # Lisage tühi massiiv, mis mahutab iga lahtri
        # selles reas
    grid.append([])
    for column in range(10):
        grid[row].append(0)

# genereerib 5 suvalist bommi
bombs = random.sample(range(100), 5)

for bomb in bombs:
    row = bomb // 10
    column = bomb % 10
    grid[row][column] = 1

# alustab pygame
pygame.init()

# Määrab ekraani KÕRGUSE ja LAIUSE
WINDOW_SIZE = [255, 255]
screen = pygame.display.set_mode(WINDOW_SIZE)

# Määrab ekraani pealkirija
pygame.display.set_caption("Array Backed Grid")

# Korda, kuni kasutaja vajutab close nupule
done = False

# Kui kiiresti ekraan uuendab
clock = pygame.time.Clock()

# -------- Põhiprogrammi tsükkel -----------
while not done:
    for event in pygame.event.get(): # Kasutaja tegi midagi
        if event.type == pygame.QUIT: # Kui kasutaja vajutas close
            done = True # Märgib et done ja lõpetab tsükkli
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Kasutaja vajutab hiirega et saada positsiooni
            pos = pygame.mouse.get_pos()
            # Muudab ekraani x/y koordinaadid ruudustiku koordinaatideks
            column = pos[0] // (WIDTH + MARGIN)
            row = pos[1] // (HEIGHT + MARGIN)
            # Määrab selle asukohaks üks
            grid[row][column] = 1
            print("Click ", pos, "Grid coordinates: ", row, column)

    # Määrab ekraani tausta
    screen.fill(BLACK)
    # Joonistab ruudustiku
    for row in range(10):
        for column in range(10):
            color = WHITE
            if grid[row][column] == 1:
                color = GREEN
            pygame.draw.rect(screen,
                             color,
                             [(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN,
                              WIDTH,
                              HEIGHT])

    # Limiit: 60 fps
    clock.tick(60)
    # Uuendab ekraani sellega mida teinud oleme
    pygame.display.flip()

pygame.quit()
