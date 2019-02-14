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
        self.active = False
        self.hit = False
        self.shrink_speed = .07
        self.min_size = 3
        self.max_size = 20

        self.active_time = 4
        self.timer = 0

    def update(self, delta_time, cursor, stars):
        self.dt = delta_time

        if self.active:
            self.image.fill(self.active_clr)
            self.timer += self.dt
            for star in stars:
                if star.hit:
                    self.timer = 0
            if self.timer >= self.active_time:
                self.active = False
                self.timer = 0
        else:
            self.image.fill(self.color)

        self.set_size()
        self.check_events(cursor)

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
        if pygame.sprite.collide_rect(cursor, self):
            if cursor.active:
                self.active = True
                self.hit = True
            else:
                self.hit = False

    def fade_in(self):
        if self.alpha < 255:
            self.alpha += 4
            self.image.set_alpha(self.alpha)

    def fade_out(self):
        if self.alpha > 0:
            self.alpha -= 4
            self.image.set_alpha(self.alpha)
        else:
            self.active = False
            self.dead = True
