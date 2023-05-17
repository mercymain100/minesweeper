import pygame
import random

# värvid RGB-väärtustena
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Määrab ruudu laiuse ja kõrguse
WIDTH = 20
HEIGHT = 20

# Määra ruudu servade vahe
MARGIN = 5

# Loob tühja ruudustik
grid = []
for row in range(10):
    grid.append([])
    for column in range(10):
        grid[row].append({'value': '', 'revealed': False})

# Genereerib juhuslikud bommi positsioonid(5 tk)
bombs = random.sample(range(100), 5)

# Paigutab pommid ruudustikule
for bomb in bombs:
    row = bomb // 10
    column = bomb % 10
    grid[row][column]['value'] = 'B'

pygame.init()

# Määrab akna suuruse
WINDOW_SIZE = [255, 320]
screen = pygame.display.set_mode(WINDOW_SIZE)
# Määrab akna pealkirja
pygame.display.set_caption("Minesweeper")

done = False
game_over = False  # Näitab Kas mäng on läbi
restart_button_rect = pygame.Rect(80, 220, 90, 40)
quit_button_rect = pygame.Rect(80, 270, 90, 40)

clock = pygame.time.Clock()

# Laeb fonti
font = pygame.font.Font(None, 36)

# Funktsioon, mis paljastab ruudustiku
def reveal_cell(row, column):
    global game_over  # Lisage globaalse muutuja viite
    grid[row][column]['revealed'] = True
    if grid[row][column]['value'] == 'B':
        print("Sa vajutasid bommi peale!")
        game_over = True  # Mängu lõpetamiseks määrab game_over
    else:
        print("Vajutasid tühja lahtri peale")

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not game_over:  # Kontrollige, kas mäng on juba läbi
                # Kui hiireklõps toimus, siis määra klõpsatud positsioon
                pos = pygame.mouse.get_pos()
                column = pos[0] // (WIDTH + MARGIN)
                row = pos[1] // (HEIGHT + MARGIN)
                # Revalib vastava ruudu
                reveal_cell(row, column)
            else:
                if restart_button_rect.collidepoint(event.pos):
                    # Restartib mängu
                    game_over = False
                    grid = []
                    for row in range(10):
                        grid.append([])
                        for column in range(10):
                            grid[row].append({'value': '', 'revealed': False})
                    bombs = random.sample(range(100), 5)
                    for bomb in bombs:
                        row = bomb // 10
                        column = bomb % 10
                        grid[row][column]['value'] = 'B'
                elif quit_button_rect.collidepoint(event.pos):
                    done = True  # Lõpeta mäng

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
            pygame.draw.rect(screen, color, [(MARGIN + WIDTH) * column + MARGIN, (MARGIN + HEIGHT) * row + MARGIN, WIDTH, HEIGHT])

    if game_over:
        # Kui mäng on läbi, kuvab "Mäng läbi" teksti ja kaks nuppu
        text_surface = font.render("Mäng läbi", True, RED)
        text_rect = text_surface.get_rect(center=(WINDOW_SIZE[0] // 2, 150))
        screen.blit(text_surface, text_rect)

        pygame.draw.rect(screen, GREEN, restart_button_rect)
        pygame.draw.rect(screen, RED, quit_button_rect)

        restart_text_surface = font.render("Restart", True, BLACK)
        restart_text_rect = restart_text_surface.get_rect(center=(restart_button_rect.centerx, restart_button_rect.centery))
        screen.blit(restart_text_surface, restart_text_rect)

        quit_text_surface = font.render("Quit", True, BLACK)
        quit_text_rect = quit_text_surface.get_rect(center=(quit_button_rect.centerx, quit_button_rect.centery))
        screen.blit(quit_text_surface, quit_text_rect)

    # Piirab fpsi 60 ticki sekundis
    clock.tick(60)
    # Kuvab ekraanile uuendatud kaater kui kasutaja vajutab gridi peale
    pygame.display.flip()

pygame.quit()
