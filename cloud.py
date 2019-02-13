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

        self.rect.center = pos

        self.dead = False
        self.min_life = 30
        self.max_life = 200
        self.life = random.randint(self.min_life, self.max_life)
        self.tick = random.uniform(0.01, 40)
        self.max_speed = 10
        self.dx = random.uniform(-(self.max_speed), self.max_speed)
        self.dy = random.uniform(-(self.max_speed), self.max_speed)
        (self.x, self.y) = self.rect.center

    def update(self, delta_time):
        self.dt = delta_time
        self.x += self.dx * self.dt
        self.y += self.dy * self.dt

        self.life -= self.tick * delta_time

        # update transparency
        if self.life < self.min_life:
            self.fade_out()
        elif self.life > self.max_life:
            self.life = self.max_life
        else:
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
        self.alpha += 50 * self.dt
        if self.alpha >= self.life:
            self.alpha = self.life
        self.image.set_alpha(self.alpha)

    def fade_out(self):
        self.alpha -= 200 * self.dt
        if self.alpha <= 0:
            self.alpha = 0
            self.dead = True

        else:
            self.image.set_alpha(self.alpha)
