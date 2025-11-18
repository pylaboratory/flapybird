
import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Square")


# Asset paths
ASSET_PATH = "flappy-bird-assets/sprites/"

# Load images
background_img = pygame.image.load(ASSET_PATH + "background-day.png")
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
_bird_raw_imgs = [
    pygame.image.load(ASSET_PATH + "yellowbird-downflap.png"),
    pygame.image.load(ASSET_PATH + "yellowbird-midflap.png"),
    pygame.image.load(ASSET_PATH + "yellowbird-upflap.png"),
]
# Double the size
bird_imgs = [pygame.transform.scale(img, (img.get_width()*2, img.get_height()*2)) for img in _bird_raw_imgs]
pipe_img = pygame.image.load(ASSET_PATH + "pipe-green.png")
pipe_img = pygame.transform.scale(pipe_img, (80, HEIGHT))

# Load sounds
import os
SOUND_PATH = os.path.join("flappy-bird-assets", "audio")
flap_sound = pygame.mixer.Sound(os.path.join(SOUND_PATH, "wing.wav"))
score_sound = pygame.mixer.Sound(os.path.join(SOUND_PATH, "point.wav"))
hit_sound = pygame.mixer.Sound(os.path.join(SOUND_PATH, "hit.wav"))



# Player properties
player_size = bird_imgs[0].get_width(), bird_imgs[0].get_height()  # (width, height)
player_x = WIDTH // 4  # Start on the left side
player_y = HEIGHT // 2 - player_size[1] // 2
player_vel = 0
gravity = 0.5
flap_strength = -10
bird_frame = 0
bird_frame_counter = 0
bird_tilt = 0


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

def reset_game():
    global player_x, player_y, player_vel, pipe_x, pipe_top_height, score, passed_pipe, bird_frame, bird_frame_counter, bird_tilt
    player_x = WIDTH // 4
    player_y = HEIGHT // 2 - player_size[1] // 2
    player_vel = 0
    pipe_x = WIDTH
    pipe_top_height = random.randint(50, HEIGHT - pipe_gap - 50)
    score = 0
    passed_pipe = False
    bird_frame = 0
    bird_frame_counter = 0
    bird_tilt = 0

clock = pygame.time.Clock()

def draw_gameover():
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0,0,0,128))
    screen.blit(overlay, (0,0))
    font.render_to(screen, (WIDTH//2-120, HEIGHT//2-40), "Game Over!", (255,255,255))
    font.render_to(screen, (WIDTH//2-180, HEIGHT//2+10), "Press SPACE to retry or ESC to quit", (255,255,255))
    pygame.display.flip()

def game_loop():
    global player_x, player_y, player_vel, pipe_x, pipe_top_height, score, passed_pipe, bird_frame, bird_frame_counter, bird_tilt
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player_vel = flap_strength
                    flap_sound.play()

        # Apply gravity
        player_vel += gravity
        player_y += player_vel

        # Bird animation: cycle frames every 5 ticks
        bird_frame_counter += 1
        if bird_frame_counter >= 5:
            bird_frame = (bird_frame + 1) % 3
            bird_frame_counter = 0

        # Bird tilt: tilt down when flapping, up when falling (reversed)
        if player_vel < -1:
            bird_tilt = min(60, bird_tilt + 8)   # tilt down (flap)
        elif player_vel > 1:
            bird_tilt = max(-25, bird_tilt - 4)  # tilt up (fall)
        else:
            bird_tilt = int(bird_tilt * 0.9)     # relax tilt

        # Keep player within screen bounds
        if player_y < 0:
            player_y = 0
            player_vel = 0
        if player_y > HEIGHT - player_size[1]:
            player_y = HEIGHT - player_size[1]
            player_vel = 0

        # Player and pipe rectangles
        player_rect = pygame.Rect(player_x, int(player_y), player_size[0], player_size[1])
        pipe_top_rect = pygame.Rect(pipe_x, 0, pipe_width, pipe_top_height)
        pipe_bottom_rect = pygame.Rect(pipe_x, pipe_top_height + pipe_gap, pipe_width, HEIGHT - (pipe_top_height + pipe_gap))

        # Collision detection
        if player_rect.colliderect(pipe_top_rect) or player_rect.colliderect(pipe_bottom_rect):
            hit_sound.play()
            pygame.time.delay(500)
            return False  # Game over

        # Move pipe
        pipe_x -= pipe_speed
        # Scoring: check if player passed the pipe
        if not passed_pipe and pipe_x + pipe_width < player_x:
            score += 1
            score_sound.play()
            passed_pipe = True
        # Reset pipe
        if pipe_x < -pipe_width:
            pipe_x = WIDTH
            pipe_top_height = random.randint(50, HEIGHT - pipe_gap - 50)
            passed_pipe = False

        # Drawing
        screen.blit(background_img, (0, 0))
        # Draw pipes (top and bottom)
        top_pipe_img = pygame.transform.flip(pipe_img, False, True)
        screen.blit(top_pipe_img, (pipe_x, pipe_top_height - HEIGHT))
        screen.blit(pipe_img, (pipe_x, pipe_top_height + pipe_gap))
        # Draw player (bird) with tilt and animation
        bird_img = bird_imgs[bird_frame]
        rotated_bird = pygame.transform.rotate(bird_img, bird_tilt)
        bird_rect = rotated_bird.get_rect(center=(player_x + player_size[0] // 2, int(player_y) + player_size[1] // 2))
        screen.blit(rotated_bird, bird_rect.topleft)
        # Draw score
        font.render_to(screen, (20, 20), f"Score: {score}", (0, 0, 0))

        # Update display
        pygame.display.flip()
        clock.tick(60)
    return True
while True:
    result = game_loop()
    if result:
        break  # quit
    draw_gameover()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    reset_game()
                    waiting = False
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        pygame.time.wait(50)
    else:
        continue
    break

# Quit Pygame
pygame.quit()