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
        self.image = pygame.Surface((int(self.size), int(self.size)))
        self.image.fill(self.color)
        self.image.set_alpha(self.alpha)
        self.rect = self.image.get_rect()
        self.rect.center = pos

        self.dead = False
        self.clicked = False
        self.active = False
        self.shrink_speed = .2
        self.min_size = 3
        self.max_size = 10

    def update(self, delta_time, cursor):
        self.dt = delta_time

        self.set_size()
        self.check_events(cursor)
        self.set_color()

    def set_size(self):
        shrink_amt = self.dt * self.shrink_speed
        old_center = self.rect.center
        self.size -= shrink_amt

        # check size restrictions
        if self.size < self.min_size:
            self.fade_out()
        elif self.size > self.max_size:
            self.size = self.max_size
        else:
            self.fade_in()

        # scale image
        self.image = pygame.transform.scale(self.image,
                                (int(self.size), int(self.size)))
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
        if self.alpha < 255:
            self.alpha += 4
            self.image.set_alpha(self.alpha)

    def fade_out(self):
        if self.alpha > 0:
            self.alpha -= 4
            self.image.set_alpha(self.alpha)
        else:
            self.dead = True

    def set_color(self):
        if self.active:
            self.image.fill(self.active_clr)
        else:
            self.image.fill(self.color)
