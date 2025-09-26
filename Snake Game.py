import random
import pygame
import sys

pygame.init()

width, height = 600, 600
block_size = 20
game_screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game by RAVI KUMAR")

bg_color = (30, 30, 30)
snake_color = (0, 200, 100)
food_color = (255, 80, 0)
text_color = (255, 255, 255)

clock = pygame.time.Clock()

snake_x, snake_y = width // 2, height // 2
change_x, change_y = 0, 0
snake_body = [(snake_x, snake_y)]

def spawn_food():
    return (
        random.randrange(0, width // block_size) * block_size,
        random.randrange(0, height // block_size) * block_size,
    )

food_x, food_y = spawn_food()

score = 0
font = pygame.font.SysFont("Arial", 30, bold=True)
speed = 8

pygame.mixer.music.load(r"C:\Users\hp\OneDrive\Desktop\Snake-Game-main\background sound.mp3")
pygame.mixer.music.play(-1)
eat_sound = pygame.mixer.Sound(r"C:\Users\hp\OneDrive\Desktop\Snake-Game-main\Eating sound.wav")
gameover_sound = pygame.mixer.Sound(r"C:\Users\hp\OneDrive\Desktop\Snake-Game-main\game over sound.wav")

def display_snake_and_food():
    global snake_x, snake_y, food_x, food_y, score, speed, snake_color
    snake_x = (snake_x + change_x) % width
    snake_y = (snake_y + change_y) % height
    if (snake_x, snake_y) in snake_body[1:]:
        game_over()
    snake_body.append((snake_x, snake_y))
    if food_x == snake_x and food_y == snake_y:
        score += 1
        eat_sound.play()
        if score % 5 == 0:
            speed += 1
        snake_color = (0, 150 + score * 2 % 100, 100 + score * 3 % 100)
        food_x, food_y = spawn_food()
        flash_screen()
    else:
        del snake_body[0]
    game_screen.fill(bg_color)
    pygame.draw.rect(game_screen, food_color, [food_x, food_y, block_size, block_size])
    for (x, y) in snake_body:
        pygame.draw.rect(game_screen, snake_color, [x, y, block_size, block_size])
    score_text = font.render(f"Score: {score}", True, text_color)
    game_screen.blit(score_text, [10, 10])
    pygame.display.update()

def flash_screen():
    game_screen.fill((255, 255, 100))
    pygame.display.update()
    pygame.time.delay(80)

def game_over():
    gameover_sound.play()
    game_screen.fill((200, 30, 30))
    game_over_text = font.render("GAME OVER!", True, text_color)
    restart_text = font.render("Press R to Restart or Q to Quit", True, text_color)
    game_screen.blit(game_over_text, [width // 2 - game_over_text.get_width() // 2,
                                      height // 2 - 50])
    game_screen.blit(restart_text, [width // 2 - restart_text.get_width() // 2,
                                    height // 2 + 10])
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_r:
                    restart_game()
                    return

def restart_game():
    global snake_x, snake_y, change_x, change_y, snake_body, food_x, food_y, score, speed, snake_color
    snake_x, snake_y = width // 2, height // 2
    change_x, change_y = 0, 0
    snake_body = [(snake_x, snake_y)]
    food_x, food_y = spawn_food()
    score = 0
    speed = 8
    snake_color = (0, 200, 100)

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and change_x == 0:
                change_x = -block_size
                change_y = 0
            elif event.key == pygame.K_RIGHT and change_x == 0:
                change_x = block_size
                change_y = 0
            elif event.key == pygame.K_UP and change_y == 0:
                change_x = 0
                change_y = -block_size
            elif event.key == pygame.K_DOWN and change_y == 0:
                change_x = 0
                change_y = block_size
    display_snake_and_food()
    clock.tick(speed)
