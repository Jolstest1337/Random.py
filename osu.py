import pygame
import random
import time

# Pyshit
pygame.init()

WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
FONT_COLOR = (0, 0, 0)
TARGET_RADIUS = 30
FPS = 60
CIRCLE_LIFE_TIME = 2  # seconds
APPROACH_TIME = 1.5  # seconds
GAME_DURATION = 60  # seconds

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Osu! Simplified")

font = pygame.font.SysFont(None, 36)
num_font = pygame.font.SysFont(None, 24)

score = 0
start_time = time.time()
circles = []
circle_number = 1
keybinds = [pygame.K_z, pygame.K_x]

running = True
clock = pygame.time.Clock()

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

def spawn_circle(number):
    x = random.randint(TARGET_RADIUS, WIDTH - TARGET_RADIUS)
    y = random.randint(TARGET_RADIUS, HEIGHT - TARGET_RADIUS)
    circles.append({'pos': (x, y), 'spawn_time': time.time(), 'number': number})

def draw_circle(circle):
    current_time = time.time()
    elapsed_time = current_time - circle['spawn_time']
    if elapsed_time > APPROACH_TIME:
        radius = TARGET_RADIUS
    else:
        radius = int(TARGET_RADIUS + (WIDTH // 2 - TARGET_RADIUS) * (1 - elapsed_time / APPROACH_TIME))
    pygame.draw.circle(screen, BLUE, circle['pos'], radius, 2)
    pygame.draw.circle(screen, RED, circle['pos'], TARGET_RADIUS)
    number_text = num_font.render(str(circle['number']), True, FONT_COLOR)
    screen.blit(number_text, (circle['pos'][0] - number_text.get_width() // 2, circle['pos'][1] - number_text.get_height() // 2))

def score_circle(circle, click_time):
    elapsed_time = click_time - circle['spawn_time']
    approach_ratio = elapsed_time / APPROACH_TIME
    if approach_ratio <= 0.1:
        return 300
    elif approach_ratio <= 0.3:
        return 200
    elif approach_ratio <= 0.5:
        return 100
    elif approach_ratio <= 0.75:
        return 50
    else:
        return 0

def main_menu():
    global keybinds
    selected_key = None
    while True:
        screen.fill(WHITE)
        draw_text('Main Menu', font, FONT_COLOR, screen, WIDTH // 2 - 80, HEIGHT // 2 - 200)
        draw_text('Press Enter to start the game', font, FONT_COLOR, screen, WIDTH // 2 - 150, HEIGHT // 2 - 100)
        draw_text('Press 1 to select keybind 1', font, FONT_COLOR, screen, WIDTH // 2 - 150, HEIGHT // 2)
        draw_text('Press 2 to select keybind 2', font, FONT_COLOR, screen, WIDTH // 2 - 150, HEIGHT // 2 + 50)
        draw_text(f'Keybind 1: {pygame.key.name(keybinds[0])}', font, FONT_COLOR, screen, WIDTH // 2 - 80, HEIGHT // 2 + 150)
        draw_text(f'Keybind 2: {pygame.key.name(keybinds[1])}', font, FONT_COLOR, screen, WIDTH // 2 - 80, HEIGHT // 2 + 200)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if selected_key is not None:
                    keybinds[selected_key] = event.key
                    selected_key = None
                elif event.key == pygame.K_RETURN:
                    return
                elif event.key == pygame.K_1:
                    selected_key = 0
                elif event.key == pygame.K_2:
                    selected_key = 1

while running:
    main_menu()
    score = 0
    start_time = time.time()
    circles = []
    circle_number = 1

    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time

        if elapsed_time > GAME_DURATION:
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key in keybinds:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for circle in circles[:]:
                    circle_x, circle_y = circle['pos']
                    dist = ((mouse_x - circle_x) ** 2 + (mouse_y - circle_y) ** 2) ** 0.5
                    if dist < TARGET_RADIUS:
                        click_time = time.time()
                        points = score_circle(circle, click_time)
                        if points > 0:
                            score += points
                        circles.remove(circle)
                        break

        if random.random() < 0.5:
            spawn_circle(circle_number)
            circle_number += 1

        circles = [circle for circle in circles if current_time - circle['spawn_time'] < CIRCLE_LIFE_TIME]

        screen.fill(WHITE)
        for circle in circles:
            draw_circle(circle)
        score_text = font.render(f'Score: {score}', True, FONT_COLOR)
        screen.blit(score_text, (10, 10))
        time_text = font.render(f'Time: {int(GAME_DURATION - elapsed_time)}', True, FONT_COLOR)
        screen.blit(time_text, (WIDTH - 150, 10))
        pygame.display.flip()
        clock.tick(FPS)

    # Game over screen
    screen.fill(WHITE)
    game_over_text = font.render(f'Game Over! Your Score: {score}', True, FONT_COLOR)
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(3000)

pygame.quit()
