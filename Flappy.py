import pygame
import random

# Pyshit
pygame.init()

# Window Prop
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

gravity = 0.5
bird_movement = 0
game_active = False
game_start = False
score = 0
high_score = 0

game_font = pygame.font.Font(None, 40)

# Real bird not fish
bird_surface = pygame.Surface((50, 30), pygame.SRCALPHA)
pygame.draw.ellipse(bird_surface, BLACK, (0, 0, 50, 30))  # Body
pygame.draw.polygon(bird_surface, RED, [(10, 15), (0, 5), (0, 25)])  # Beak
bird_rect = bird_surface.get_rect(center=(100, SCREEN_HEIGHT // 2))

pipe_gap = 200
pipe_height = [400, 600, 800]
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_surface = pygame.Surface((80, SCREEN_HEIGHT))
pipe_surface.fill(GREEN)

bg_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
bg_surface.fill(WHITE)

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(SCREEN_WIDTH, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom=(SCREEN_WIDTH, random_pipe_pos - pipe_gap))
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        screen.blit(pipe_surface, pipe)

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False
    if bird_rect.top <= 0 or bird_rect.bottom >= SCREEN_HEIGHT:
        return False
    return True

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 3, 1)
    return new_bird

def display_score(game_state):
    if game_state == "main_game":
        score_surface = game_font.render(f'Score: {int(score)}', True, BLACK)
        score_rect = score_surface.get_rect(center=(SCREEN_WIDTH // 2, 50))
        screen.blit(score_surface, score_rect)
    if game_state == "game_over":
        score_surface = game_font.render(f'Score: {int(score)}', True, BLACK)
        score_rect = score_surface.get_rect(center=(SCREEN_WIDTH // 2, 50))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High Score: {int(high_score)}', True, BLACK)
        high_score_rect = high_score_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(high_score_surface, high_score_rect)

def display_main_menu():
    title_surface = game_font.render('Flappy Bird', True, BLACK)
    title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    screen.blit(title_surface, title_rect)

    start_surface = game_font.render('Press SPACE to Start', True, BLACK)
    start_rect = start_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
    screen.blit(start_surface, start_rect)

clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_start:
                game_start = True
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, SCREEN_HEIGHT // 2)
                bird_movement = 0
                score = 0
            elif event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 10
            elif event.key == pygame.K_SPACE and not game_active:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, SCREEN_HEIGHT // 2)
                bird_movement = 0
                score = 0
        if event.type == SPAWNPIPE and game_start:
            pipe_list.extend(create_pipe())

    screen.blit(bg_surface, (0, 0))

    if game_start:
        if game_active:
            bird_movement += gravity
            bird_rect.centery += bird_movement
            rotated_bird = rotate_bird(bird_surface)
            screen.blit(rotated_bird, bird_rect)
            game_active = check_collision(pipe_list)

            pipe_list = move_pipes(pipe_list)
            draw_pipes(pipe_list)

            score += 0.01
            display_score('main_game')
        else:
            high_score = max(score, high_score)
            display_score('game_over')
    else:
        display_main_menu()

    pygame.display.update()
    clock.tick(120)
