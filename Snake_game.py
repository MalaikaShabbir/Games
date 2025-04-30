import pygame
import random
import time

# Initialize pygame
pygame.init()

# Game Constants
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 20
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Create game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Fonts
font = pygame.font.Font(None, 30)
large_font = pygame.font.Font(None, 40)

# Function to display text
def display_text(text, x, y, color=WHITE, font=font):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

# Welcome screen
def welcome_screen():
    screen.fill(BLACK)
    display_text("WELCOME TO SNAKE GAME", WIDTH // 4, HEIGHT // 4, GREEN, large_font)
    display_text("Developed by Malaika", WIDTH // 4, HEIGHT // 4 + 40, WHITE, font)
    display_text("Enjoy it and don't forget to share your experience!", WIDTH // 8, HEIGHT // 4 + 80, WHITE, font)
    display_text("Press SPACE to Start", WIDTH // 4, HEIGHT // 4 + 120, RED, large_font)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False

# Game function
def snake_game():
    running = True
    clock = pygame.time.Clock()

    snake = [(WIDTH // 2, HEIGHT // 2)]
    direction = (GRID_SIZE, 0)
    food = (random.randint(0, (WIDTH // GRID_SIZE) - 1) * GRID_SIZE,
            random.randint(0, (HEIGHT // GRID_SIZE) - 1) * GRID_SIZE)
    special_food = None
    global score
    score=0
    level = 1
    food_count = 0
    special_timer = 0

    while running:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != (0, GRID_SIZE):
                    direction = (0, -GRID_SIZE)
                elif event.key == pygame.K_DOWN and direction != (0, -GRID_SIZE):
                    direction = (0, GRID_SIZE)
                elif event.key == pygame.K_LEFT and direction != (GRID_SIZE, 0):
                    direction = (-GRID_SIZE, 0)
                elif event.key == pygame.K_RIGHT and direction != (-GRID_SIZE, 0):
                    direction = (GRID_SIZE, 0)

        # Move the snake
        new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

        # Wrap around screen
        if new_head[0] < 0:
            new_head = (WIDTH - GRID_SIZE, new_head[1])
        elif new_head[0] >= WIDTH:
            new_head = (0, new_head[1])
        if new_head[1] < 0:
            new_head = (new_head[0], HEIGHT - GRID_SIZE)
        elif new_head[1] >= HEIGHT:
            new_head = (new_head[0], 0)

        # Check self collision
        if new_head in snake:
            running = False

        # Add new head to snake
        snake.insert(0, new_head)

        # Check if food is eaten
        if new_head == food:
            score += 2
            food = (random.randint(0, (WIDTH // GRID_SIZE) - 1) * GRID_SIZE,
                    random.randint(0, (HEIGHT // GRID_SIZE) - 1) * GRID_SIZE)
            food_count += 1
            if food_count % 5 == 0:
                special_food = (random.randint(0, (WIDTH // GRID_SIZE) - 1) * GRID_SIZE,
                                random.randint(0, (HEIGHT // GRID_SIZE) - 1) * GRID_SIZE)
                special_timer = time.time() + 5
        else:
            snake.pop()

        # Check if special food is eaten
        if special_food and new_head == special_food:
            score += 30
            special_food = None
            food_count = 0

        # Remove special food after time limit
        if special_food and time.time() > special_timer:
            special_food = None

        # Adjust level and speed
        level = (score // 50) + 1
        speed = 2 + level
        
        # Draw snake
        for segment in snake:
            pygame.draw.rect(screen, GREEN, pygame.Rect(segment[0], segment[1], GRID_SIZE, GRID_SIZE))
        
        # Draw food
        pygame.draw.rect(screen, RED, pygame.Rect(food[0], food[1], GRID_SIZE, GRID_SIZE))
        
        # Draw special food
        if special_food:
            pygame.draw.rect(screen, BLUE, pygame.Rect(special_food[0], special_food[1], GRID_SIZE, GRID_SIZE))
        
        # Display score and level
        display_text(f"Score: {score}", 10, 10)
        display_text(f"Level: {level}", 10, 30)
        
        pygame.display.flip()
        clock.tick(speed)
       
def display_final_score(score):
    screen.fill(BLACK)
    display_text(f"FINAL SCORE: {score}", WIDTH // 4, HEIGHT // 4, GREEN, large_font)
    display_text("Press SPACE to Quit", WIDTH // 4, HEIGHT // 4 + 40, RED, large_font)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False
   
# Run the game
welcome_screen()
snake_game()
display_final_score(score)
pygame.quit()
