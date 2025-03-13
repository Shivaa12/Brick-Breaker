import pygame
import random
import time
import os

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sheetal's Brick Breaker")

# Colors
BLACK = (10, 10, 10)
WHITE = (255, 255, 255)
NEON_BLUE = (0, 255, 255)
NEON_PINK = (255, 0, 255)
NEON_GREEN = (0, 255, 0)
NEON_YELLOW = (255, 255, 0)
NEON_PURPLE = (160, 32, 240)
RED = (255, 0, 0)

# Get the directory where the script is running
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Sounds (use absolute paths)
hit_sound = pygame.mixer.Sound(os.path.join(BASE_DIR, "hit.wav"))
break_sound = pygame.mixer.Sound(os.path.join(BASE_DIR, "break.wav"))
game_over_sound = pygame.mixer.Sound(os.path.join(BASE_DIR, "gameover.wav"))
victory_sound = pygame.mixer.Sound(os.path.join(BASE_DIR, "victory.wav"))

# Paddle properties
paddle_width, paddle_height = 120, 15
paddle = pygame.Rect(WIDTH//2 - paddle_width//2, HEIGHT - 40, paddle_width, paddle_height)

# Ball properties
ball_size = 12
ball = pygame.Rect(WIDTH//2, HEIGHT//2, ball_size, ball_size)
ball_speed = [4, -4]
ball_color = random.choice([NEON_BLUE, NEON_PINK, NEON_GREEN, NEON_YELLOW, NEON_PURPLE])
ball_trail = []

# Brick properties
brick_rows, brick_cols = 6, 10
brick_width, brick_height = 70, 25
bricks = []
brick_colors = [NEON_BLUE, NEON_PINK, NEON_GREEN, NEON_YELLOW, NEON_PURPLE]
particles = []

for row in range(brick_rows):
    for col in range(brick_cols):
        brick = pygame.Rect(col * (brick_width + 5) + 35, row * (brick_height + 5) + 50, brick_width, brick_height)
        bricks.append((brick, random.choice(brick_colors)))

# Game variables
running = True
game_over = False
victory = False
clock = pygame.time.Clock()
score = 0
lives = 3
background_pulse = 0

# Loading Screen
def loading_screen():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 50)
    text = font.render("LOADING...", True, random.choice(brick_colors))
    screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
    pygame.display.flip()
    time.sleep(2)

loading_screen()

def draw_particles():
    for particle in particles[:]:
        pygame.draw.circle(screen, particle[2], (particle[0], particle[1]), particle[3])
        particle[0] += particle[4]
        particle[1] += particle[5]
        particle[3] -= 0.2
        if particle[3] <= 0:
            particles.remove(particle)

def draw_game_over_popup(message, color):
    popup_width, popup_height = 400, 200
    popup_x, popup_y = (WIDTH - popup_width) // 2, (HEIGHT - popup_height) // 2
    pygame.draw.rect(screen, color, (popup_x, popup_y, popup_width, popup_height), border_radius=15)
    pygame.draw.rect(screen, WHITE, (popup_x, popup_y, popup_width, popup_height), 5, border_radius=15)
    
    font = pygame.font.Font(None, 50)
    text = font.render(message, True, WHITE)
    screen.blit(text, (popup_x + popup_width//2 - text.get_width()//2, popup_y + 20))
    
    font = pygame.font.Font(None, 35)
    restart_text = font.render("Press R to Restart", True, WHITE)
    quit_text = font.render("Press Q to Quit", True, WHITE)
    
    screen.blit(restart_text, (popup_x + popup_width//2 - restart_text.get_width()//2, popup_y + 80))
    screen.blit(quit_text, (popup_x + popup_width//2 - quit_text.get_width()//2, popup_y + 120))

# Main game loop
while running:
    screen.fill((background_pulse % 30, 0, background_pulse % 30))
    background_pulse += 1
    
    pygame.draw.rect(screen, NEON_BLUE, paddle, border_radius=8)
    ball_trail.append((ball.x, ball.y, ball_color))
    if len(ball_trail) > 10:
        ball_trail.pop(0)
    for pos in ball_trail:
        pygame.draw.ellipse(screen, pos[2], (pos[0], pos[1], ball_size, ball_size), 2)
    pygame.draw.ellipse(screen, ball_color, ball)
    
    for brick, color in bricks:
        pygame.draw.rect(screen, color, brick, border_radius=5)
    
    draw_particles()
    
    font = pygame.font.Font(None, 35)
    score_text = font.render(f"Score: {score}  Lives: {lives}", True, WHITE)
    screen.blit(score_text, (20, 10))
    
    if not game_over and not victory:
        ball.x += ball_speed[0]
        ball.y += ball_speed[1]
        
        if ball.left <= 0 or ball.right >= WIDTH:
            ball_speed[0] *= -1
        if ball.top <= 0:
            ball_speed[1] *= -1
        
        if ball.colliderect(paddle):
            ball_speed[1] *= -1
            hit_sound.play()
        
        for brick, color in bricks[:]:
            if ball.colliderect(brick):
                bricks.remove((brick, color))
                ball_speed[1] *= -1
                score += 10
                break_sound.play()
                break
        
        if not bricks:
            victory = True
            victory_sound.play()
        
        if ball.bottom >= HEIGHT:
            lives -= 1
            if lives == 0:
                game_over = True
                game_over_sound.play()
            else:
                ball.x, ball.y = WIDTH//2, HEIGHT//2
                ball_speed = [4, -4]
    
    if game_over:
        draw_game_over_popup("GAME OVER", RED)
    elif victory:
        draw_game_over_popup("YOU WIN!", NEON_GREEN)
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.left > 0:
        paddle.move_ip(-8, 0)
    if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
        paddle.move_ip(8, 0)
    
    pygame.display.flip()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
            if event.key == pygame.K_r and (game_over or victory):
                game_over = False
                victory = False
                score = 0
                lives = 3
                bricks = [(pygame.Rect(col * (brick_width + 5) + 35, row * (brick_height + 5) + 50, brick_width, brick_height), random.choice(brick_colors)) for row in range(brick_rows) for col in range(brick_cols)]
    
    clock.tick(60)

pygame.quit()
