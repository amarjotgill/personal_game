"""
This is a simple rocket battle game that I have made, the game ends when one user's health is under 10.
The game will restart it's self after a 5 second delay, to quit the game press the exit button in the top right corner.
"""

import pygame
pygame.font.init()

WIDTH = 600
HEIGHT = 400
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
# different colors used through project
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
CANT_CROSS = pygame.Rect(295, 0, 10, 400)

# creating event to detect bullet hitting
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

HEALTH_FONT = pygame.font.SysFont("comicsans", 40)
END_FONT = pygame.font.SysFont("comicsans", 80)

FPS = 60
VELOCITY = 5
BULLET_SPEED = 6
NUM_BULLETS = 3
# Game window size
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
# text at top
pygame.display.set_caption("Rocket Battle!")


YELLOW_SPACESHIP = pygame.image.load("spaceship_yellow.png")
YELLOW_SPACESHIP_SiZE = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP, (55, 40)), 90)

RED_SPACESHIP = pygame.image.load("spaceship_red.png")
RED_SPACESHIP_SiZE = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP, (55, 40)), 270)

SPACE_BACKGROUND = pygame.transform.scale(pygame.image.load("space.png"), (WIDTH, HEIGHT))


# draws the game onto the window
def draw_game(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    # how to get background
    WINDOW.blit(SPACE_BACKGROUND, (0, 0))
    # border in middle
    pygame.draw.rect(WINDOW, BLACK, CANT_CROSS)
    red_health_text = HEALTH_FONT.render("Health:" + str(red_health), True, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health:" + str(yellow_health), True, WHITE)

    WINDOW.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WINDOW.blit(yellow_health_text, (10, 10))
    WINDOW.blit(YELLOW_SPACESHIP_SiZE, (yellow.x, yellow.y))
    WINDOW.blit(RED_SPACESHIP_SiZE, (red.x, red.y))
    # used to project red bullet in game
    for bullet in red_bullets:
        pygame.draw.rect(WINDOW, RED, bullet)
    # used to project yellow bullet
    for bullet in yellow_bullets:
        pygame.draw.rect(WINDOW, YELLOW, bullet)

    pygame.display.update()


def move_yellow(keys_pressed, yellow):
    if keys_pressed[pygame.K_a]:
        if yellow.x - VELOCITY > 0:
            yellow.x -= VELOCITY
    # right
    if keys_pressed[pygame.K_d]:
        if yellow.x + VELOCITY + yellow.width < CANT_CROSS.x:
            yellow.x += VELOCITY
    # up
    if keys_pressed[pygame.K_w]:
        if yellow.y - VELOCITY > 0:
            yellow.y -= VELOCITY
    # down
    if keys_pressed[pygame.K_s]:
        if yellow.y + VELOCITY + yellow.height < HEIGHT - 15:
            yellow.y += VELOCITY


def move_red(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT]:
        if red.x - VELOCITY > CANT_CROSS.x:
            red.x -= VELOCITY
    # right
    if keys_pressed[pygame.K_RIGHT]:
        if red.x + VELOCITY + red.width < WIDTH:
            red.x += VELOCITY
    # up
    if keys_pressed[pygame.K_UP]:
        if red.y - VELOCITY > 0:
            red.y -= VELOCITY
    # down
    if keys_pressed[pygame.K_DOWN]:
        if red.y + VELOCITY + red.height < HEIGHT - 15:
            red.y += VELOCITY


def shoot_bullet(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_SPEED
        # will detect if yellow bullet hits red hit box
        if red.colliderect(bullet):
            # triggers the event
            pygame.event.post(pygame.event.Event(RED_HIT))
            # gets rid of the bullet
            yellow_bullets.remove(bullet)

        elif bullet.x > WIDTH:
            # if the bullet goes off the screen it will get rid of it
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_SPEED
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)

        elif bullet.x < 0:
            red_bullets.remove(bullet)


def winner_of_game(text):
    draw = END_FONT.render(text, True, WHITE)
    WINDOW.blit(draw, (WIDTH / 2 - draw.get_width() / 2, HEIGHT / 2 - draw.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(500)


def main():
    # creates the hit boxes for both red and yellow
    red = pygame.Rect(350, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    # to get it to run at 60 fps
    clock = pygame.time.Clock()
    run_game = True

    red_bullets = []
    yellow_bullets = []
    # base health
    red_health = 10
    yellow_health = 10

    while run_game:
        # control for 60 fps
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_game = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < NUM_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)

                if event.key == pygame.K_SPACE and len(red_bullets) < NUM_BULLETS:
                    bullet = pygame.Rect(red.x - red.width, red.y + red.height // 2 - 2, 10, 5)
                    red_bullets.append(bullet)

            if event.type == RED_HIT:
                red_health -= 1

            if event.type == YELLOW_HIT:
                yellow_health -= 1
        winner = ""
        if red_health <= 0:
            winner = "Yellow wins!"

        if yellow_health <= 0:
            winner = "Red wins!"

        if winner != "":
            winner_of_game(winner)
            break

        keys_pressed = pygame.key.get_pressed()
        move_yellow(keys_pressed, yellow)
        move_red(keys_pressed, red)

        shoot_bullet(yellow_bullets, red_bullets, yellow, red)

        draw_game(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)
    # reruns game after someone wins
    main()


if __name__ == "__main__":
    main()
