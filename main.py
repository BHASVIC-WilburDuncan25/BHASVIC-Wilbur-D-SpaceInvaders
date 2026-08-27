import pygame
import random
import math
import sys

pygame.init()

screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

width = 800
height = 600

Title_font = pygame.font.Font(None, 90)
button_font = pygame.font.Font(None, 50)
font = pygame.font.Font('freesansbold.ttf', 32)

menu = 0
paused = 1
playing = 2
game_over = 3
game_state = menu
lives = 3


Black = (0, 0, 0)
White = (255, 255, 255)
Red = (255, 0, 0)
Grey = (100, 100, 100)
Dark_grey = (40, 40, 40)


def display_text(text, font, colour, x, y):
    screen_surf = font.render(text, True, colour)
    rectangle = screen_surf.get_rect(center=(x, y))
    screen.blit(screen_surf, rectangle)


def display_menu():
    screen.fill(Black)

    # Title
    display_text("SPACE INVADERS", Title_font, White, width // 2, 120)

    # Play button
    play_button = pygame.Rect(275, 230, 250, 70)
    pygame.draw.rect(screen, Dark_grey, play_button)
    pygame.draw.rect(screen, White, play_button, 3)
    display_text("PLAY", button_font, White, width // 2, 265)

    # Exit button
    exit_button = pygame.Rect(275, 330, 250, 70)
    pygame.draw.rect(screen, Dark_grey, exit_button)
    pygame.draw.rect(screen, White, exit_button, 3)
    display_text("EXIT", button_font, White, width // 2, 365)

    return play_button, exit_button


def pause_draw():
    overlay = pygame.Surface((width, height))
    overlay.set_alpha(180)
    overlay.fill(Black)
    screen.blit(overlay, (0, 0))

    display_text("PAUSED", Title_font, White, width // 2, 120)

    # Resume button
    resume_button = pygame.Rect(275, 200, 250, 60)
    pygame.draw.rect(screen, Dark_grey, resume_button)
    pygame.draw.rect(screen, White, resume_button, 3)
    display_text("RESUME", button_font, White, width // 2, 230)

    # Restart button
    restart_button = pygame.Rect(275, 290, 250, 60)
    pygame.draw.rect(screen, Dark_grey, restart_button)
    pygame.draw.rect(screen, White, restart_button, 3)
    display_text("RESTART", button_font, White, width // 2, 320)

    # Main menu button
    menu_button = pygame.Rect(275, 380, 250, 60)
    pygame.draw.rect(screen, Dark_grey, menu_button)
    pygame.draw.rect(screen, White, menu_button, 3)
    display_text("MAIN MENU", button_font, White, width // 2, 410)

    return resume_button, restart_button, menu_button


def restart_game():
    global playerX, playerY, playerX_change
    global enemyX, enemyY, enemyX_change, enemyY_change
    global bulletX, bulletY, bullet_state, score_value, lives

    playerX = 370
    playerY = 480
    playerX_change = 0
    score_value = 0
    bulletX = 0
    bulletY = 480
    bullet_state = "ready"
    lives = 3

    for i in range(num_of_enemies):
        enemyX[i] = random.randint(0, 735)
        enemyY[i] = random.randint(50, 150)
        enemyX_change[i] = 2
        enemyY_change[i] = 40


def reset_game():
    global playerX, playerY, playerX_change
    global enemyX, enemyY, enemyX_change, enemyY_change
    global bulletX, bulletY, bullet_state

    playerX = 370
    playerY = 480
    playerX_change = 0

    bulletX = 0
    bulletY = 480
    bullet_state = "ready"

    for i in range(num_of_enemies):
        enemyX[i] = random.randint(0, 735)
        enemyY[i] = random.randint(50, 150)
        enemyX_change[i] = 2
        enemyY_change[i] = 40


pygame.display.set_caption("Space Invaders")

icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

playerImg = pygame.image.load('spaceship.png')
playerX = 370
playerY = 480
playerX_change = 0

num_of_enemies = 6
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('ufo.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(2)
    enemyY_change.append(40)

bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 6
bullet_state = "ready"

score_value = 0
textX = 10
textY = 10
livesX = 650
livesY = 10

over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, White)
    screen.blit(score, (x, y))

def show_lives(x, y):
    liveDisplay = font.render("Lives : " + str(lives), True, White)
    screen.blit(liveDisplay, (x, y))
def game_over_text():
    over_text = over_font.render("GAME OVER!!!", True, White)
    screen.blit(over_text, (200, 250))

def player(x, y):
    screen.blit(playerImg, (x, y))
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(
        math.pow(enemyX - bulletX, 2) +
        math.pow(enemyY - bulletY, 2)
    )
    if distance < 27:
        return True
    else:
        return False


# Game Lop
running = True
while running:
    screen.fill(Black)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if game_state == menu:

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                play_button, exit_button = display_menu()

                if play_button.collidepoint(mouse_pos):
                    restart_game()
                    game_state = playing

                elif exit_button.collidepoint(mouse_pos):
                    running = False

        elif game_state == playing:

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_state = paused
                if event.key == pygame.K_LEFT:
                    playerX_change = -5

                if event.key == pygame.K_RIGHT:
                    playerX_change = 5
                if event.key == pygame.K_SPACE:

                    if bullet_state == "ready":
                        bulletX = playerX
                        fire_bullet(bulletX, bulletY)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0

        elif game_state == paused:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_state = playing

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                resume_button, restart_button, menu_button = pause_draw()

                if resume_button.collidepoint(mouse_pos):
                    game_state = playing
                elif restart_button.collidepoint(mouse_pos):
                    restart_game()
                    game_state = playing

                elif menu_button.collidepoint(mouse_pos):
                    restart_game()
                    game_state = menu


    # Menu
    if game_state == menu:
        display_menu()
    # Playing
    elif game_state == playing:
        playerX += playerX_change
        if playerX <= 0:
            playerX = 0
        elif playerX >= 736:
            playerX = 736
        for i in range(num_of_enemies):
            if enemyY[i] > 440:
                lives = lives - 1

                if lives <= 0:
                    game_state = game_over
                else:
                    reset_game()

                break
            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = 2
                enemyY[i] += enemyY_change[i]

            elif enemyX[i] >= 736:
                enemyX_change[i] = -2
                enemyY[i] += enemyY_change[i]

            collision = isCollision(
                enemyX[i],
                enemyY[i],
                bulletX,
                bulletY
            )
            if collision:
                bulletY = 480
                bullet_state = "ready"
                score_value += 1

                enemyX[i] = random.randint(0, 735)
                enemyY[i] = random.randint(50, 150)

            enemy(enemyX[i], enemyY[i], i)

        if bulletY <= 0:
            bulletY = 480
            bullet_state = "ready"
        if bullet_state == "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change

        player(playerX, playerY)
        show_score(textX, textY)
        show_lives(livesX, livesY)

    elif game_state == paused:
        for i in range(num_of_enemies):
            enemy(enemyX[i], enemyY[i], i)
        if bullet_state == "fire":
            screen.blit(bulletImg, (bulletX + 16, bulletY + 10))

        player(playerX, playerY)
        show_score(textX, textY)
        pause_draw()

    elif game_state == game_over:
        game_over_text()
    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()

