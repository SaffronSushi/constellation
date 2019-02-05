import pygame, random

class Cloud(pygame.sprite.Sprite):
    def __init__(self, game, pos, size=16):
        super(Cloud, self).__init__()
        self.screen = game.screen
        self.size = size
        self.radius = int(self.size / 2)

        self.image = pygame.Surface((self.size, self.size))
        self.rect = self.image.get_rect()
        self.image.set_colorkey((0, 0, 0))
        pygame.draw.circle(self.image, (255, 100, 100),
                           self.rect.center, self.radius)
        self.image.set_alpha(75)

        self.rect.centerx = random.randint(self.radius,
                        self.screen.get_width() - self.radius)
        self.rect.centery = random.randint(self.radius,
                        self.screen.get_height() - self.radius)

        self.offscreen = False
        self.dead = False
        self.life = random.randint(10, 200)
        self.tick = random.randint(1, 10)
        self.max_speed = 80
        self.dx = random.randint(-(self.max_speed), self.max_speed)
        self.dy = random.randint(-(self.max_speed), self.max_speed)
        (self.x, self.y) = self.rect.center

    def update(self, delta_time):
        self.x += self.dx * delta_time
        self.y += self.dy * delta_time

        self.life -= self.tick * delta_time
        self.image.set_alpha(self.life)
        
        if (self.rect.left > self.screen.get_width() or
            self.rect.right < 0 or
            self.rect.top > self.screen.get_height() or
            self.rect.bottom < 0):
            self.offscreen = True

        self.rect.center = (self.x, self.y)
