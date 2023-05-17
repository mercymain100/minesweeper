import pygame
import random
#värvid RGB-väärtustena
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

#Määrab ruudu laiuse ja kõrguse
WIDTH = 20
HEIGHT = 20

#Määra ruudu servade vahe
MARGIN = 5

#Loob tühija ruudustik
grid = []
for row in range(10):
    grid.append([])
    for column in range(10):
        grid[row].append({'value': '', 'revealed': False})
        
#Genereerib juhuslikud pommitsoonid
bombs = random.sample(range(100), 5)

#Paigutab pommid ruudustikule
for bomb in bombs:
    row = bomb // 10
    column = bomb % 10
    grid[row][column]['value'] = 'B'

pygame.init()

#Määrab akna suuruse
WINDOW_SIZE = [255, 255]
screen = pygame.display.set_mode(WINDOW_SIZE)
#Määrab akna pealkiri
pygame.display.set_caption("Minesweeper")

done = False

clock = pygame.time.Clock()

#Funktsioon, mis paljastab ruudustiku 
def reveal_cell(row, column):
    grid[row][column]['revealed'] = True
    if grid[row][column]['value'] == 'B':
        print("Sa vajutasid bommi peale!")
    else:
        print("Vajutasid tühja lahtri peale")

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Kui hiireklõps toimus, siis määra klõpsatud positsioon
            pos = pygame.mouse.get_pos()
            column = pos[0] // (WIDTH + MARGIN)
            row = pos[1] // (HEIGHT + MARGIN)
            #paljastab vastava ruudu
            reveal_cell(row, column)

# Täidab ekraan musta värviga
    screen.fill(BLACK)
    
# Joonista ruudustik ekraanile
    for row in range(10):
        for column in range(10):
            color = WHITE
            if grid[row][column]['revealed']:
                if grid[row][column]['value'] == 'B':
                    color = RED
                else:
                    color = GREEN
            pygame.draw.rect(screen,color,[(MARGIN + WIDTH) * column + MARGIN,(MARGIN + HEIGHT) * row + MARGIN,WIDTH,HEIGHT])

# Piirab fpsi 60 ticki sekundis
    clock.tick(60)
# Kuvab ekraanile uuendatud kaater kui kasutaja vajutab gridi peale
    pygame.display.flip()

pygame.quit()
