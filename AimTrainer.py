import pygame
import random
import time

# Pyshit
pygame.init()

# window property
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
RED = (255, 0, 0)
FONT_COLOR = (0, 0, 0)
TARGET_RADIUS = 20
FPS = 60

# Creation of the window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Aim Trainer")

font = pygame.font.SysFont(None, 36)

score = 0
start_time = time.time()
game_duration = 30  # seconds
target_pos = (random.randint(TARGET_RADIUS, WIDTH - TARGET_RADIUS), random.randint(TARGET_RADIUS, HEIGHT - TARGET_RADIUS))

# Main menu
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

def main_menu():
    while True:
        screen.fill(WHITE)
        draw_text('Main Menu', font, FONT_COLOR, screen, WIDTH // 2 - 80, HEIGHT // 2 - 200)
        draw_text('1. Normal', font, FONT_COLOR, screen, WIDTH // 2 - 80, HEIGHT // 2 - 100)
        draw_text('2. Competitive', font, FONT_COLOR, screen, WIDTH // 2 - 80, HEIGHT // 2)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    normal_mode()
                if event.key == pygame.K_2:
                    competitive_menu()

def competitive_menu():
    while True:
        screen.fill(WHITE)
        draw_text('Competitive Menu', font, FONT_COLOR, screen, WIDTH // 2 - 80, HEIGHT // 2 - 200)
        draw_text('1. Easy', font, FONT_COLOR, screen, WIDTH // 2 - 80, HEIGHT // 2 - 100)
        draw_text('2. Medium', font, FONT_COLOR, screen, WIDTH // 2 - 80, HEIGHT // 2)
        draw_text('3. Hard', font, FONT_COLOR, screen, WIDTH // 2 - 80, HEIGHT // 2 + 100)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    competitive_mode(3)
                if event.key == pygame.K_2:
                    competitive_mode(2)
                if event.key == pygame.K_3:
                    competitive_mode(0.5)

def normal_mode():
    global score, start_time, target_pos
    score = 0
    start_time = time.time()
    target_pos = (random.randint(TARGET_RADIUS, WIDTH - TARGET_RADIUS), random.randint(TARGET_RADIUS, HEIGHT - TARGET_RADIUS))
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                dist = ((mouse_x - target_pos[0]) ** 2 + (mouse_y - target_pos[1]) ** 2) ** 0.5
                if dist < TARGET_RADIUS:
                    score += 1
                    target_pos = (random.randint(TARGET_RADIUS, WIDTH - TARGET_RADIUS), random.randint(TARGET_RADIUS, HEIGHT - TARGET_RADIUS))

        elapsed_time = time.time() - start_time
        if elapsed_time > game_duration:
            running = False

        screen.fill(WHITE)
        pygame.draw.circle(screen, RED, target_pos, TARGET_RADIUS)
        score_text = font.render(f'Score: {score}', True, FONT_COLOR)
        screen.blit(score_text, (10, 10))
        time_text = font.render(f'Time: {int(game_duration - elapsed_time)}', True, FONT_COLOR)
        screen.blit(time_text, (WIDTH - 150, 10))
        pygame.display.flip()
        clock.tick(FPS)

    game_over()

def competitive_mode(display_time):
    global score, start_time, target_pos
    score = 0
    start_time = time.time()
    target_pos = (random.randint(TARGET_RADIUS, WIDTH - TARGET_RADIUS), random.randint(TARGET_RADIUS, HEIGHT - TARGET_RADIUS))
    running = True
    clock = pygame.time.Clock()
    target_start_time = time.time()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                dist = ((mouse_x - target_pos[0]) ** 2 + (mouse_y - target_pos[1]) ** 2) ** 0.5
                if dist < TARGET_RADIUS:
                    score += 1
                    target_start_time = time.time()  # Reset the timer for the new target
                    target_pos = (random.randint(TARGET_RADIUS, WIDTH - TARGET_RADIUS), random.randint(TARGET_RADIUS, HEIGHT - TARGET_RADIUS))

        elapsed_time = time.time() - start_time
        if elapsed_time > game_duration:
            running = False

        current_target_time = time.time() - target_start_time
        if current_target_time >= display_time:
            target_pos = (random.randint(TARGET_RADIUS, WIDTH - TARGET_RADIUS), random.randint(TARGET_RADIUS, HEIGHT - TARGET_RADIUS))
            target_start_time = time.time()

        screen.fill(WHITE)
        pygame.draw.circle(screen, RED, target_pos, TARGET_RADIUS)
        score_text = font.render(f'Score: {score}', True, FONT_COLOR)
        screen.blit(score_text, (10, 10))
        time_text = font.render(f'Time: {int(game_duration - elapsed_time)}', True, FONT_COLOR)
        screen.blit(time_text, (WIDTH - 150, 10))
        pygame.display.flip()
        clock.tick(FPS)

    game_over()

def game_over():
    screen.fill(WHITE)
    game_over_text = font.render(f'Game Over! Your Score: {score}', True, FONT_COLOR)
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(3000)
    main_menu()

main_menu()
pygame.quit()
