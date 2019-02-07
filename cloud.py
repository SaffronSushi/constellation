import pygame, random

class Cloud(pygame.sprite.Sprite):
    def __init__(self, game, pos, size=16):
        super(Cloud, self).__init__()
        self.screen = game.screen
        self.size = size
        self.radius = int(self.size / 2)

        self.color = (255, 100, 100)
        self.alpha = 0
        
        self.image = pygame.Surface((self.size, self.size))
        self.rect = self.image.get_rect()
        self.image.set_colorkey((0, 0, 0))
        pygame.draw.circle(self.image, self.color,
                           self.rect.center, self.radius)
        self.image.set_alpha(self.alpha)

        self.rect.centerx = random.randint(self.radius,
                        self.screen.get_width() - self.radius)
        self.rect.centery = random.randint(self.radius,
                        self.screen.get_height() - self.radius)

        self.dead = False
        self.max_life = 200
        self.life = random.randint(10, self.max_life)
        self.tick = random.uniform(0.01, 40)
        self.max_speed = 10
        self.dx = random.randint(-(self.max_speed), self.max_speed)
        self.dy = random.randint(-(self.max_speed), self.max_speed)
        (self.x, self.y) = self.rect.center

    def update(self, delta_time):
        self.x += self.dx * delta_time
        self.y += self.dy * delta_time

        # update transparency
        if self.life > self.max_life:
            self.life = self.max_life
            
        self.life -= self.tick * delta_time
        self.image.set_alpha(self.life)
        self.fade_in()

        # check if offscreen
        if (self.rect.left > self.screen.get_width() or
            self.rect.right < 0 or
            self.rect.top > self.screen.get_height() or
            self.rect.bottom < 0):
            self.dead = True

        # update center
        self.rect.center = (self.x, self.y)

    def fade_in(self):
        self.alpha += 0.5
        if self.alpha >= self.life:
            self.alpha = self.life
        self.image.set_alpha(self.alpha)
