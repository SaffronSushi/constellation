import pygame, random

class Cloud(pygame.sprite.Sprite):
    def __init__(self, game):
        super(Cloud, self).__init__()
        self.screen = game.screen

        self.size = random.randint(5, 100)
        self.radius = int(self.size / 2)
        #self.points = int(100 / self.size)
        self.image = pygame.Surface((self.size, self.size))
        #self.image.set_colorkey((0, 0, 0))
        self.image.fill((255, 100, 100))
        self.image.set_alpha(75)
        self.rect = self.image.get_rect()

        self.rect.centerx = random.randint(self.radius,
                        self.screen.get_width() - self.radius)
        self.rect.centery = random.randint(self.radius,
                        self.screen.get_height() - self.radius)

        self.offscreen = False
        self.max_speed = 100
        self.dx = random.randint(-(self.max_speed), self.max_speed)
        self.dy = random.randint(-(self.max_speed), self.max_speed)

    def update(self, delta_time):
        self.rect.x += self.dx * delta_time
        self.rect.y += self.dy * delta_time

        if (self.rect.left > self.screen.get_width() or
            self.rect.right < 0 or
            self.rect.top > self.screen.get_height() or
            self.rect.bottom < 0):
            self.offscreen = True
