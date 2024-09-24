import pygame
import random

# Inicializa o pygame
pygame.init()

# Definindo cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
LIGHT_BLUE = (173, 216, 230)
YELLOW = (255, 255, 102)

# Dimensões da tela
WIDTH = 800
HEIGHT = 800
DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Remake Muito Pro')

# Relógio do jogo
CLOCK = pygame.time.Clock()

# Tamanho da cobra e velocidade
SNAKE_BLOCK = 10
SNAKE_SPEED = 15

# Fonte do texto
FONT_STYLE = pygame.font.SysFont("bahnschrift", 25)

# Funções auxiliares
def show_score(score):
    value = FONT_STYLE.render(f"Pontuação: {score}", True, YELLOW)
    DISPLAY.blit(value, [10, 10])

def draw_snake(snake_list):
    for segment in snake_list:
        pygame.draw.rect(DISPLAY, GREEN, [segment[0], segment[1], SNAKE_BLOCK, SNAKE_BLOCK])

def message(msg, color, pos):
    mesg = FONT_STYLE.render(msg, True, color)
    DISPLAY.blit(mesg, pos)

def load_sounds():
    try:
        eat_sound = pygame.mixer.Sound('eat.wav')
        game_over_sound = pygame.mixer.Sound('game_over.wav')
        return eat_sound, game_over_sound
    except pygame.error:
        print("Erro ao carregar os sons.")
        return None, None

def handle_input(event, x1_change, y1_change, paused):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT and x1_change == 0:
            return -SNAKE_BLOCK, 0, paused
        elif event.key == pygame.K_RIGHT and x1_change == 0:
            return SNAKE_BLOCK, 0, paused
        elif event.key == pygame.K_UP and y1_change == 0:
            return 0, -SNAKE_BLOCK, paused
        elif event.key == pygame.K_DOWN and y1_change == 0:
            return 0, SNAKE_BLOCK, paused
        elif event.key == pygame.K_p:
            paused = not paused
    return x1_change, y1_change, paused

# Menu principal
def main_menu():
    menu = True
    while menu:
        DISPLAY.fill(BLACK)
        message("Snake Remake", WHITE, [WIDTH / 3, HEIGHT / 4])
        message("Pressione 1 para Jogar", WHITE, [WIDTH / 3, HEIGHT / 2])
        message("Pressione 2 para Sair", WHITE, [WIDTH / 3, HEIGHT / 2 + 30])
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    game_loop()
                if event.key == pygame.K_2:
                    pygame.quit()
                    quit()

# Loop do jogo principal
def game_loop():
    eat_sound, game_over_sound = load_sounds()

    game_over = False
    game_close = False
    paused = False

    x1, y1 = WIDTH / 2, HEIGHT / 2
    x1_change, y1_change = 0, 0

    snake_list = []
    length_of_snake = 1

    foodx = round(random.randrange(0, WIDTH - SNAKE_BLOCK) / SNAKE_BLOCK) * SNAKE_BLOCK
    foody = round(random.randrange(0, HEIGHT - SNAKE_BLOCK) / SNAKE_BLOCK) * SNAKE_BLOCK

    while not game_over:
        while game_close:
            DISPLAY.fill(BLACK)
            message("Game Over! Pressione C pra Continuar ou Q pra Sair", RED, [WIDTH / 6, HEIGHT / 3])
            show_score(length_of_snake - 1)
            pygame.display.update()

            if game_over_sound:
                game_over_sound.play()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            x1_change, y1_change, paused = handle_input(event, x1_change, y1_change, paused)

        if paused:
            DISPLAY.fill(BLACK)
            message("Jogo Pausado. Pressione P para continuar.", WHITE, [WIDTH / 6, HEIGHT / 3])
            pygame.display.update()
            continue

        if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        DISPLAY.fill(LIGHT_BLUE)

        pygame.draw.rect(DISPLAY, RED, [foodx, foody, SNAKE_BLOCK, SNAKE_BLOCK])

        snake_head = [x1, y1]
        snake_list.append(snake_head)

        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_close = True

        draw_snake(snake_list)
        show_score(length_of_snake - 1)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, WIDTH - SNAKE_BLOCK) / SNAKE_BLOCK) * SNAKE_BLOCK
            foody = round(random.randrange(0, HEIGHT - SNAKE_BLOCK) / SNAKE_BLOCK) * SNAKE_BLOCK
            length_of_snake += 1
            if eat_sound:
                eat_sound.play()

        CLOCK.tick(SNAKE_SPEED)

    main_menu()

# Inicia o jogo
main_menu()
pygame.quit()
