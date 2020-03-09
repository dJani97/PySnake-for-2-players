
class Apple:
    def __init__(self, pos, size, game_display, image=None):
        self.pos = pos
        self.img = image
        self.size = size
        self.game_display = game_display

    def draw(self):
        # pygame.draw.rect(Display, red,[self.pos[0], self.pos[1], self.size, self.size])
        self.game_display.blit(self.img, self.pos)
