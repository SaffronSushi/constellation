import pygame

class Star(pygame.sprite.Sprite):
    def __init__(self, game, pos, size=8):
        super(Star, self).__init__()
        self.screen = game.screen
        self.size = size

        self.color = ((255, 255, 255))
        self.active_clr = ((200, 200, 255))
        self.alpha = 0

        self.radius = int(self.size / 2)
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill(self.color)
        self.image.set_alpha(self.alpha)
        self.rect = self.image.get_rect()
        self.rect.center = pos

        self.clicked = False
        self.active = False

    def update(self, delta_time, cursor):
        self.dt = delta_time
        self.tick = self.dt / 3

        self.set_size()
        self.check_events(cursor)
        if self.active:
            self.image.fill(self.active_clr)
        else:
            self.image.fill(self.color)
        self.fade_in()


    def set_size(self):
        old_center = self.rect.center
        self.size -= self.tick
        if self.size < 0:
            self.size = 0
            
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

    def fade_in(self):
        self.alpha += 0.3
        self.image.set_alpha(self.alpha)
