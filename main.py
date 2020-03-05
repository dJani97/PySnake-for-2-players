import pygame
import random
from constants import *

from model.apple import Apple
from model.snake import Snake

pygame.init()


green_head = pygame.image.load('data/SnakeHeadGreen.png')
purple_head = pygame.image.load('data/SnakeHeadPurple.png')
apple_img = pygame.image.load('data/Apple.png')
font = pygame.font.SysFont("comicsansms", 50)
small_font = pygame.font.SysFont("comicsansms", 25)
large_font = pygame.font.SysFont("comicsansms", 85)


display = pygame.display.set_mode((res_x, res_y))

pygame.display.set_caption("Snake Game")
pygame.display.set_icon(apple_img)
clock = pygame.time.Clock()

direction = "right"
apples = set([])


def pause():
    paused = True
    message_screen("Paused", black, -100, "large")
    message_screen("Press Space to continue or Escape to quit", black, 25)
    pygame.display.update()
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = False
                elif event.key == pygame.K_ESCAPE:
                    exit_game()
        clock.tick(10)


def score(new_score, pos, color):
    text = small_font.render("Score: " + str(new_score), True, color)
    display.blit(text, pos)


def text_objects(text, color, size="small"):
    if size == "small":
        text_surface = small_font.render(text, True, color)
    elif size == "medium":
        text_surface = font.render(text, True, color)
    else:
        text_surface = large_font.render(text, True, color)
    return text_surface, text_surface.get_rect()


def text_to_button(msg, color, pos, size="small"):
    text_surf, text_rect = text_objects(msg, color, size)
    text_rect.center = (pos[0] + (pos[2] / 2), pos[1] + (pos[3] / 2))
    display.blit(text_surf, text_rect)


def message_screen(msg, color, y_displace=0, size="small"):
    text_surf, text_rect = text_objects(msg, color, size)
    text_rect.center = (res_x / 2), (res_y / 2) + y_displace
    display.blit(text_surf, text_rect)


def generate_random_apple():
    new_apple = Apple([round(random.randrange(apple_size, res_x - apple_size) / 10) * 10,
                       round(random.randrange(apple_size, res_y - apple_size) / 10) * 10],
                      apple_size, display, apple_img)
    return new_apple


def game_controls():
    controls = True
    display.fill(white)
    message_screen("Controls", green, -120, "large")
    message_screen("Green movement: Arrow keys", green, -30, "small")
    message_screen("Purple movement: W, A, S, D keys", purple, 10, "small")
    message_screen("Pause: P", black, 60, "small")
    while controls:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    controls = False
                elif event.key == pygame.K_ESCAPE:
                    exit_game()

        controls = button("Main Menu", (res_x / 2 - 70, res_y - 150, 140, 50), yellow, light_yellow, action="switch")
        button("Quit", (res_x / 2 + 120, res_y - 150, 100, 50), red, light_red, action="quit")

        clock.tick(30)
        pygame.display.update()


def button(text, pos, color1, color2, action, text_color=black):
    cur = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if pos[0] + pos[2] > cur[0] > pos[0] and pos[1] + pos[3] > cur[1] > pos[1]:
        pygame.draw.rect(display, color2, pos)
        if click[0] == 1:
            if action == "switch":
                return False
            elif action == "controls":
                clock.tick(6)
                game_controls()
                clock.tick(6)
            elif action == "quit":
                exit_game()
    else:
        pygame.draw.rect(display, color1, pos)
    text_to_button(text, text_color, pos)

    return True


def game_intro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    intro = False
                elif event.key == pygame.K_ESCAPE:
                    exit_game()

        display.fill(white)
        message_screen("Snake Game", green, -120, "large")
        message_screen("Collect apples, and do", black, -30, "small")
        message_screen("not hit yourself!", black, 10, "small")
        intro = button("Play", (res_x / 2 - 220, res_y - 150, 100, 50), green, light_green, action="switch")
        button("Controls", (res_x / 2 - 60, res_y - 150, 120, 50), yellow, light_yellow, action="controls")
        button("Quit", (res_x / 2 + 120, res_y - 150, 100, 50), red, light_red, action="quit")
        clock.tick(30)
        pygame.display.update()


def game_loop():
    global apple_count
    game_exit = False
    game_over = False
    while apple_count > len(apples):
        apple = generate_random_apple()
        apples.add(apple)
    snake1 = Snake([((res_x / 2 - 5 * block_size) / 10) * 10, (res_y / 20) * 10], [0, 0], None, green_head, display)
    snake2 = Snake([((res_x / 2 - 5 * block_size) / 10) * 10, (res_y / 20) * 10], [0, 0], None, purple_head, display, purple)

    while not game_exit:
        if apple_count > len(apples):
            apple = generate_random_apple()
            apples.add(apple)
        elif apple_count < len(apples):
            apples.pop()

        if game_over:
            message_screen("Game Over!", red, -50, "large")
            message_screen("Press Space to restart or Esc to quit.", black, 30)
            pygame.display.update()
            while game_over:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit_game()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            exit_game()
                        if event.key == pygame.K_SPACE:
                            game_loop()

        for event in pygame.event.get():  # Events LEAD
            if event.type == pygame.QUIT:
                game_exit = True
            if event.type == pygame.KEYDOWN:

                # Snake1 events:
                if event.key == pygame.K_LEFT:
                    snake1.key_event(Dir.left)

                if event.key == pygame.K_RIGHT:
                    snake1.key_event(Dir.right)

                if event.key == pygame.K_DOWN:
                    snake1.key_event(Dir.down)

                if event.key == pygame.K_UP:
                    snake1.key_event(Dir.up)

                # Snake2 events:
                if event.key == pygame.K_a:
                    snake2.key_event(Dir.left)

                if event.key == pygame.K_d:
                    snake2.key_event(Dir.right)

                if event.key == pygame.K_s:
                    snake2.key_event(Dir.down)

                if event.key == pygame.K_w:
                    snake2.key_event(Dir.up)

                if event.key == pygame.K_SPACE:
                    pause()
                if event.key == pygame.K_ESCAPE:
                    game_exit = True
                if event.key == pygame.K_p:
                    pause()
                if event.key == pygame.K_e:
                    apple_count += 1
                if event.key == pygame.K_q:
                    apple_count = 100

        display.fill(white)

        for apple in apples:
            apple.draw()

        if snake1.update() or snake2.update():
            game_over = True

        snake1.score_display([50, 2], score)
        snake1.eat(apples, generate_random_apple)
        snake2.score_display([res_x - 150, 2], score)
        snake2.eat(apples, generate_random_apple)

        pygame.display.update()

        clock.tick(fps)
    exit_game()


def exit_game():
    pygame.quit()
    quit()


if __name__ == '__main__':
    game_intro()
    game_loop()
