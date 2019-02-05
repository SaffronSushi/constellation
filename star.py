import pygame

class Star(pygame.sprite.Sprite):
    def __init__(self, game, pos, size=8):
        super(Star, self).__init__()
        self.screen = game.screen
        self.size = size

        self.color = ((255, 255, 255))
        self.active_clr = ((200, 200, 255))
        self.life = int(self.size)
        self.radius = int(self.size / 2)
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.center = pos

        self.clicked = False
        self.active = False

    def update(self, delta_time, cursor):
        self.dt = delta_time

        self.set_size()
        self.check_events(cursor)
        if self.active:
            self.image.fill(self.active_clr)
        else:
            self.image.fill(self.color)

    def set_size(self):
        old_center = self.rect.center
        self.life -= 4 * self.dt
        if self.life < 0:
            self.life = 0
            
        self.size = int(self.life / 10)
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = old_center

    def check_events(self, cursor):
        if pygame.mouse.get_pressed() == (1, 0, 0):
            if pygame.sprite.collide_rect(cursor, self):
                self.clicked = True

        if self.clicked == True:
            if pygame.mouse.get_pressed() == (0, 0, 0):
                self.clicked = False
                if pygame.sprite.collide_rect(cursor, self):
                    self.active = True
