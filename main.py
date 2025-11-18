import pygame

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Square")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)


# Player properties
player_size = 50
player_x = WIDTH // 4  # Start on the left side
player_y = HEIGHT // 2 - player_size // 2
player_vel = 0
gravity = 0.5
flap_strength = -10


# Pipe properties
pipe_width = 80
pipe_gap = 300
pipe_x = WIDTH
import random
pipe_top_height = random.randint(50, HEIGHT - pipe_gap - 50)
pipe_speed = 4

# Scoring
score = 0
import pygame.freetype
font = pygame.freetype.SysFont(None, 48)
passed_pipe = False

# Game loop
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player_vel = flap_strength


    # Apply gravity
    player_vel += gravity
    player_y += player_vel

    # Keep player within screen bounds
    if player_y < 0:
        player_y = 0
        player_vel = 0
    if player_y > HEIGHT - player_size:
        player_y = HEIGHT - player_size
        player_vel = 0

    # Player and pipe rectangles
    player_rect = pygame.Rect(player_x, int(player_y), player_size, player_size)
    pipe_top_rect = pygame.Rect(pipe_x, 0, pipe_width, pipe_top_height)
    pipe_bottom_rect = pygame.Rect(pipe_x, pipe_top_height + pipe_gap, pipe_width, HEIGHT - (pipe_top_height + pipe_gap))

    # Collision detection
    if player_rect.colliderect(pipe_top_rect) or player_rect.colliderect(pipe_bottom_rect):
        running = False



    # Move pipe
    pipe_x -= pipe_speed
    # Scoring: check if player passed the pipe
    if not passed_pipe and pipe_x + pipe_width < player_x:
        score += 1
        passed_pipe = True
    # Reset pipe
    if pipe_x < -pipe_width:
        pipe_x = WIDTH
        pipe_top_height = random.randint(50, HEIGHT - pipe_gap - 50)
        passed_pipe = False


    # Drawing
    screen.fill(WHITE)  # Fill background
    # Draw pipe (top and bottom)
    pygame.draw.rect(screen, (0, 200, 0), (pipe_x, 0, pipe_width, pipe_top_height))
    pygame.draw.rect(screen, (0, 200, 0), (pipe_x, pipe_top_height + pipe_gap, pipe_width, HEIGHT - (pipe_top_height + pipe_gap)))
    # Draw player
    pygame.draw.rect(screen, RED, player_rect)
    # Draw score
    font.render_to(screen, (20, 20), f"Score: {score}", (0, 0, 0))

    # Update display
    pygame.display.flip()
    clock.tick(60)

# Quit Pygame
pygame.quit()