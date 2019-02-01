import pygame, random
from star import Star
from cloud import Cloud

class Cursor(pygame.sprite.Sprite):
    def __init__(self):
        super(Cursor, self).__init__()
        self.image = pygame.Surface((16, 16))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        pygame.draw.rect(self.image, (200, 200, 255), self.rect, 3)

    def update(self):
        self.rect.center = pygame.mouse.get_pos()   

class Game():
    def __init__(self):
        pygame.init()
        self.FULLSCREEN = 0
        self.WINDOWED = 1
        self.DISPLAY_MODE = self.WINDOWED

        pygame.display.set_caption("constellation")
        self.res = (800, 600)
        self.set_display()
        self.framerate = 100

        self.bg_color = (20, 20, 80)
        self.bg = pygame.Surface(self.screen.get_size())
        self.bg.fill(self.bg_color)

        self.cursor = Cursor()
        self.stars = pygame.sprite.Group()
        self.clouds = pygame.sprite.Group()
        # points as in coordinates, not score
        self.points = []

    def start(self):
        self.running = True
        self.clock = pygame.time.Clock()
        self.make_stars()
        self.make_clouds()

        self.delay = random.randint(0, 1)
        self.pause = 0

        self.__main_loop()

    def stop(self):
        self.running = False

    def __main_loop(self):
        while self.running:
            self.dt = self.clock.tick(self.framerate) / 1000
            pygame.mouse.set_visible(False)

            self.check_events()
            self.update()

    def set_display(self):
        """ creates either a fullscreen or
            windowed display based on the
            current display state
        """
        if self.DISPLAY_MODE == self.FULLSCREEN:
            self.screen = pygame.display.set_mode(self.res, pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(self.res)

    def check_events(self):
        keys = pygame.key.get_pressed()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        if keys[pygame.K_f]:
            if self.DISPLAY_MODE == self.FULLSCREEN:
                self.DISPLAY_MODE = self.WINDOWED
            else:
                self.DISPLAY_MODE = self.FULLSCREEN
                
            self.set_display()

        if keys[pygame.K_SPACE]:
            if len(self.points) > 1:
                self.make_star()

        if keys[pygame.K_r]:
            self.start()

    def update(self):
        self.cursor.update()
        self.clouds.update(self.dt)
        self.check_clouds()
        self.stars.update(self.dt, self.cursor)
        for star in self.stars:
            if star.life <= 0:
                for point in self.points:
                    if point == star.rect.center:
                        self.points.remove(point)
                self.stars.remove(star)

        self.screen.blit(self.bg, (0, 0))
        self.clouds.draw(self.screen)
        self.draw_lines()
        self.stars.draw(self.screen)
        self.screen.blit(self.cursor.image, self.cursor.rect)

        pygame.display.flip()

    def make_stars(self):
        self.stars.empty()
        for i in range(random.randint(10, 20)):
            size = random.randint(5, 200)
            star = Star(self, size)
            self.stars.add(star)

    def make_clouds(self):
        self.clouds.empty()
        for i in range(random.randint(5, 12)):
            cloud = Cloud(self)
            self.clouds.add(cloud)

    def draw_lines(self):
        for star in self.stars:
            if star.active:
                if star.rect.center not in self.points:
                    self.points.append(star.rect.center)

        if len(self.points) > 1:
            pygame.draw.lines(self.screen, (200, 200, 255),
                                  True, self.points, 3)

    def make_star(self):
        x = [p[0] for p in self.points]
        y = [p[1] for p in self.points]
        centroid = (sum(x) / len(self.points), sum(y) / len(self.points))

        star = Star(self, 150/ len(self.points))
        star.rect.center = centroid
        self.stars.add(star)

        self.points.clear()
        for star in self.stars:
            star.active = False

    def check_clouds(self):
        for cloud in self.clouds:
            if cloud.offscreen or cloud.dead:
                self.clouds.remove(cloud)
                
        self.pause += self.dt
        if self.pause >= self.delay:
            self.pause = 0
            cloud = Cloud(self)
            self.clouds.add(cloud)

  
def main():
    game = Game()
    game.start()

if __name__ == "__main__":
    main()
