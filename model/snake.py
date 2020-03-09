import pygame
from constants import *


class Snake:
    def __init__(self, pos, vel, angle, image, game_display, color=green):
        self.pos = pos
        self.vel = vel
        self.angle = angle
        self.img = image
        self.list = []
        self.length = 1
        self.head = self.img
        self.color = color
        self.game_display = game_display

    def score_display(self, pos, score):
        score(self.length - 1, pos, self.color)

    def key_event(self, new_direction):
        self.angle = new_direction

    def eat(self, apples) -> int:
        eaten_apples = 0
        eaten_apple_list = []
        for apple in apples:
            if apple.pos[0] < self.pos[0] < apple.pos[0] + apple_size or self.pos[0] + block_size > apple.pos[0] \
                    and self.pos[0] < apple.pos[0] + apple_size:
                if apple.pos[1] < self.pos[1] < apple.pos[1] + apple.size or self.pos[1] + block_size > apple.pos[1] \
                        and self.pos[1] < apple.pos[1] + apple.size:
                    eaten_apple_list.append(apple)
                    eaten_apples += 1
                    self.length += 1

        for eaten in eaten_apple_list:
            apples.remove(eaten)

        return eaten_apples

    def overlaps(self, obj) -> bool:
        for x in self.list:
            if obj.pos[0] < x[0] < obj.pos[0] + block_size or x[0] + block_size > obj.pos[0] \
                    and x[0] < obj.pos[0] + block_size:
                if x[1] < self.pos[1] < x[1] + block_size or self.pos[1] + block_size > x[1] \
                        and self.pos[1] < x[1] + block_size:
                    return True

        return False

    def update(self):
        game_over = False

        if (self.angle == Dir.right) and (self.vel[0] != -block_size):
            self.vel[0] = +block_size
            self.vel[1] = 0
            self.head = pygame.transform.rotate(self.img, 270)

        if (self.angle == Dir.left) and (self.vel[0] != block_size):
            self.vel[0] = -block_size
            self.vel[1] = 0
            self.head = pygame.transform.rotate(self.img, 90)

        if (self.angle == Dir.up) and (self.vel[1] != block_size):
            self.head = self.img
            self.vel[1] = -block_size
            self.vel[0] = 0

        if (self.angle == Dir.down) and (self.vel[1] != -block_size):
            self.vel[1] = +block_size
            self.vel[0] = 0
            self.head = pygame.transform.rotate(self.img, 180)

        # update movement
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]

        # build the snake
        snake_head = [self.pos[0], self.pos[1]]
        self.list.append(snake_head)
        if len(self.list) > self.length:
            del self.list[0]
        if snake_head in self.list[:-1]:
            game_over = True
        # draw the snake
        for XnY in self.list[:-1]:
            pygame.draw.rect(self.game_display, self.color, [XnY[0], XnY[1], block_size, block_size])
        # draw the snake's head
        self.game_display.blit(self.head, (self.list[-1][0], self.list[-1][1]))

        # check if out of boundries
        if self.pos[0] < 0 or self.pos[0] >= res_x or self.pos[1] < 0 or self.pos[1] >= res_y:
            game_over = True
        return game_over
