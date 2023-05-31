import pygame
import random

# Värvid RGB formaadis
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Määrab lahtri laius ja kõrgus
WIDTH = 20
HEIGHT = 20

# Määrab vahemaa lahtrite vahel
MARGIN = 5

# Määrab raskusastmed
difficulties = {
    "beginner": {"size": (8, 8), "mines": 10},
    "intermediate": {"size": (random.randint(13, 16), random.randint(15, 16)), "mines": 40},
    "expert": {"size": (16, 30), "mines": 99}
}

# Alustab pygami
pygame.init()

# Määrab akna suuruse
WINDOW_SIZE = [300, 200]
screen = pygame.display.set_mode(WINDOW_SIZE)
# Määrab akna pealkirja 
pygame.display.set_caption("Minesweeper")

done = False
selected_difficulty = None

clock = pygame.time.Clock()

# Laeb fondi
font = pygame.font.Font(None, 36)

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if 50 <= pos[0] <= 250:
                if 50 <= pos[1] <= 80:
                    selected_difficulty = "beginner"
                    done = True
                elif 90 <= pos[1] <= 120:
                    selected_difficulty = "intermediate"
                    done = True
                elif 130 <= pos[1] <= 160:
                    selected_difficulty = "expert"
                    done = True

    screen.fill(BLACK)

    # Joonistab menüü teksti
    beginner_text_surface = font.render("Beginner", True, WHITE)
    beginner_text_rect = beginner_text_surface.get_rect(center=(WINDOW_SIZE[0] // 2, 65))
    screen.blit(beginner_text_surface, beginner_text_rect)

    intermediate_text_surface = font.render("Intermediate", True, WHITE)
    intermediate_text_rect = intermediate_text_surface.get_rect(center=(WINDOW_SIZE[0] // 2, 105))
    screen.blit(intermediate_text_surface, intermediate_text_rect)

    expert_text_surface = font.render("Expert", True, WHITE)
    expert_text_rect = expert_text_surface.get_rect(center=(WINDOW_SIZE[0] // 2, 145))
    screen.blit(expert_text_surface, expert_text_rect)

    pygame.display.flip()

# Kui raskustase on valitud alustab mängu
if selected_difficulty:
    difficulty = difficulties[selected_difficulty]

    # Loob tühia ruudustiku
    grid = []
    for row in range(difficulty["size"][0]):
        grid.append([])
        for column in range(difficulty["size"][1]):
            grid[row].append({"value": "", "revealed": False})

    # Genereelib suvalised bommi tükkide positsioonid
    bombs = random.sample(range(difficulty["size"][0] * difficulty["size"][1]), difficulty["mines"])

    # Paneb bommid ruudustikule
    for bomb in bombs:
        row = bomb // difficulty["size"][1]
        column = bomb % difficulty["size"][1]
        grid[row][column]["value"] = "B"

    # Määrab mänguakna suuruse ruudustiku põhjal
    WINDOW_SIZE = [
        (WIDTH + MARGIN) * difficulty["size"][1] + MARGIN,
        (HEIGHT + MARGIN) * difficulty["size"][0] + MARGIN + 100,
    ]
    # pygame.display.set_mode() funktsioon ja määramine ekraani pealkirja pygame.display.set_caption() abil.
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Minesweeper")

    done = False
    game_over = False
    restart_button_rect = pygame.Rect((WINDOW_SIZE[0] - 200) // 2, WINDOW_SIZE[1] - 110, 90, 40)
    quit_button_rect = pygame.Rect((WINDOW_SIZE[0] - 200) // 2 + 110, WINDOW_SIZE[1] - 110, 90, 40)
    #reveal_cell() funktsioon:See funktsioon võtab argumendina rea ja veeru ning avastab vastava ruudu. Kui ruut on pomm, siis mäng lõppeb ja game_over muutub tõeks.
    def reveal_cell(row, column):
        global game_over
        grid[row][column]["revealed"] = True
        if grid[row][column]["value"] == "B":
            print("You clicked on a bomb!")
            game_over = True
        else:
            print("You clicked on an empty cell")
    #count_neighbor_bombs() funktsioon:See funktsioon võtab argumendina rea ja veeru ning loeb naaber-ruutudes olevate pommide arvu.
    def count_neighbor_bombs(row, column):
        count = 0
        for i in range(row - 1, row + 2):
            for j in range(column - 1, column + 2):
                if 0 <= i < difficulty["size"][0] and 0 <= j < difficulty["size"][1]:
                    if grid[i][j]["value"] == "B":
                        count += 1
        return count
    #kuni done muutuja väärtus muutub tõeks. See tsükkel kontrollib pygame'i sündmusi sealhulgas kasutaja hiireklõpse ja programmist väljumist. Kui mäng ei ole lõppenud kontrollib hiireklõpsu positsiooni arvutab rea ja veeru indeksid ning kutsutakse välja reveal_cell() funktsioon vastavate indeksitega. Kui mäng on lõppenud kontrollitakse, kas klõpsati taaskäivitamise või lõpetamise nuppu ning siis muudab game_over väärtus või done väärtust.
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not game_over:
                    pos = pygame.mouse.get_pos()
                    column = pos[0] // (WIDTH + MARGIN)
                    row = pos[1] // (HEIGHT + MARGIN)
                    if 0 <= row < difficulty["size"][0] and 0 <= column < difficulty["size"][1]:
                        reveal_cell(row, column)
                else:
                    if restart_button_rect.collidepoint(event.pos):
                        # Taaskäivitab mängu
                        game_over = False
                        grid = []
                        for row in range(difficulty["size"][0]):
                            grid.append([])
                            for column in range(difficulty["size"][1]):
                                grid[row].append({"value": "", "revealed": False})
                        bombs = random.sample(range(difficulty["size"][0] * difficulty["size"][1]), difficulty["mines"])
                        for bomb in bombs:
                            row = bomb // difficulty["size"][1]
                            column = bomb % difficulty["size"][1]
                            grid[row][column]["value"] = "B"
                    elif quit_button_rect.collidepoint(event.pos):
                        done = True
        #Ekraani täitmine musta värviga: Enne iga tsükli iteratsiooni täidetakse ekraan musta värviga screen.fill(BLACK), et kustutada eelmine tsükkel ja valmistada ette uus grid.
        screen.fill(BLACK)

        # Joonistab ruudustik ekraanile
        for row in range(difficulty["size"][0]):
            for column in range(difficulty["size"][1]):
                color = WHITE
                if grid[row][column]["revealed"]:
                    if grid[row][column]["value"] == "B":
                        color = RED
                    else:
                        color = GREEN
                pygame.draw.rect(
                    screen,
                    color,
                    [
                        (MARGIN + WIDTH) * column + MARGIN,
                        (MARGIN + HEIGHT) * row + MARGIN,
                        WIDTH,
                        HEIGHT,
                    ],
                )

                if grid[row][column]["revealed"] and grid[row][column]["value"] != "B":
                    neighbor_bombs = count_neighbor_bombs(row, column)
                    if neighbor_bombs > 0:
                        number_text_surface = font.render(str(neighbor_bombs), True, BLACK)
                        number_text_rect = number_text_surface.get_rect(center=(
                            (MARGIN + WIDTH) * column + MARGIN + WIDTH // 2,
                            (MARGIN + HEIGHT) * row + MARGIN + HEIGHT // 2
                        ))
                        screen.blit(number_text_surface, number_text_rect)
        #Kui kasutaja vajutab bommi peale või võidab siis kuvatakse see tekst.
        if game_over:
            text_surface = font.render("Game Over", True, RED)
            text_rect = text_surface.get_rect(center=(WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] - 150))
            screen.blit(text_surface, text_rect)

            pygame.draw.rect(screen, GREEN, restart_button_rect)
            pygame.draw.rect(screen, RED, quit_button_rect)

            restart_text_surface = font.render("Restart", True, BLACK)
            restart_text_rect = restart_text_surface.get_rect(center=(restart_button_rect.centerx, restart_button_rect.centery))
            screen.blit(restart_text_surface, restart_text_rect)

            quit_text_surface = font.render("Quit", True, BLACK)
            quit_text_rect = quit_text_surface.get_rect(center=(quit_button_rect.centerx, quit_button_rect.centery))
            screen.blit(quit_text_surface, quit_text_rect)

        pygame.display.flip()

    pygame.quit()
else:
    pygame.quit()
