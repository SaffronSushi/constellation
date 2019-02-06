import pygame, random, math
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

class Label(pygame.sprite.Sprite):
    def __init__(self, game):
        super(Label, self).__init__()
        self.screen = game.screen

        self.text = "0"
        self.font = pygame.font.SysFont(None, 40)
        self.fg_color = ((0x00, 0x00, 0x00))
        self.bg_color = ((0xFF, 0xFF, 0xFF))
        self.center = (100, 100)
        self.size = (150, 30)

        self.image = pygame.Surface(self.size)
        self.image.fill(self.bg_color)
        self.rect = self.image.get_rect()

    def update(self):
        font_surface = self.font.render(self.text, True,
                                self.fg_color, self.bg_color)
        font_rect = font_surface.get_rect()
        font_rect.center = self.rect.center

        self.image.blit(font_surface, font_rect)

class Game():
    def __init__(self):
        pygame.init()
        self.FULLSCREEN = 0
        self.WINDOWED = 1
        self.DISPLAY_MODE = self.WINDOWED

        pygame.display.set_caption("constellation")
        self.res = (800, 600)
        self.set_display()
        self.framerate = 1000

        self.bg_color = (20, 20, 80)
        self.bg = pygame.Surface(self.screen.get_size())
        self.bg.fill(self.bg_color)

        self.cursor = Cursor()
        self.stars = pygame.sprite.Group()
        self.clouds = pygame.sprite.Group()

        self.scoreboard = Label(self)
        self.scoreboard.rect.right = self.screen.get_width()
        self.labels = pygame.sprite.Group(self.scoreboard)
        self.score = 0
        
        # points as in coordinates, not score
        self.points = []

    def start(self):
        self.running = True
        self.clock = pygame.time.Clock()
        self.start_stars()
        #self.start_clouds()

        self.cloud_timer = 0
        self.cloud_delay = 0

        self.star_timer = 0
        self.star_delay = 0

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
            self.submit_stars()

        if keys[pygame.K_r]:
            self.start()

    def update(self):        
        # update
        self.cursor.update()
        self.update_clouds()
        self.update_stars()
        self.labels.update()

        # draw
        self.screen.blit(self.bg, (0, 0))
        self.clouds.draw(self.screen)
        self.draw_lines()
        self.stars.draw(self.screen)
        self.screen.blit(self.cursor.image, self.cursor.rect)
        self.labels.draw(self.screen)

        pygame.display.flip()

    def make_star(self, pos, size="random"):
        if size == "random":
            size = random.randint(5, 15)
            
        if pos == "random":
            radius = int(size / 2)
            pos = (random.randint(radius,
                    self.screen.get_width() - radius),
                   random.randint(radius,
                    self.screen.get_height() - radius))
            
        star = Star(self, pos, size)
        self.stars.add(star)

    def make_cloud(self, pos, size="random"):
        if size == "random":
            size = random.randint(5, 100)
            radius = int(size / 2)

        if pos == "random":
            pos = (random.randint(0, self.screen.get_width()),
               random.randint(0, self.screen.get_height()))
            
        cloud = Cloud(self, pos, size)
        self.clouds.add(cloud)

    def start_stars(self):
        """ creates new initial group of
            stars at start of game
        """
        self.stars.empty()
        for i in range(random.randint(10, 20)):
            self.make_star("random")

    def start_clouds(self):
        """ creates new initial group of
            clouds at start of game
        """
        self.clouds.empty()
        for i in range(random.randint(3, 12)):
            self.make_cloud("random")

    def update_stars(self):
        """ maintains stars based on
            current state
        """
        self.stars.update(self.dt, self.cursor)
        self.star_timer += self.dt

        for star in self.stars:
            if star.size <= 0:
                for point in self.points:
                    if point == star.rect.center:
                        self.points.remove(point)
                self.stars.remove(star)

        # randomly make new stars
        if self.star_timer >= self.star_delay:
            self.star_timer = 0
            self.star_delay = random.uniform(8, 16)
            self.make_star("random", size="random")

    def update_clouds(self):
        """ maintains clouds based on
            current state of a cloud,
            and generates new clouds
        """
        self.clouds.update(self.dt)
        self.cloud_timer += self.dt

        # remove if dead or offscreen
        for cloud in self.clouds:
            if cloud.offscreen or cloud.dead:
                self.clouds.remove(cloud)

        # create new cloud based on timer
        if self.cloud_timer >= self.cloud_delay:
            self.cloud_timer = 0
            self.cloud_delay = random.uniform(0, 1)
            size = random.randint(5, 100)
            radius = int(size / 2)
            pos = (random.randint(0, self.screen.get_width()),
                   random.randint(0, self.screen.get_height()))
            self.make_cloud(pos, size)

    def draw_lines(self):
        """ draws lines onscreen based on
            which stars are currently active
        """
        for star in self.stars:
            if star.active:
                if star.rect.center not in self.points:
                    self.points.append(star.rect.center)

        if len(self.points) > 1:
            pygame.draw.lines(self.screen, (200, 200, 255),
                                  True, self.points, 3)

    def submit_stars(self):
        """ creates a new star based on
            currently selected stars
        """
        # find centroid of all active stars
        if len(self.points) > 0:
            if len(self.points) < 2:
                centroid = self.points[0]
                
            if len(self.points) > 1:
                x = [p[0] for p in self.points]
                y = [p[1] for p in self.points]
                centroid = (sum(x) / len(self.points),
                            sum(y) / len(self.points))
                size = (16/ len(self.points))
                self.make_star(centroid, size)

            for cloud in self.clouds:
                near_clouds = 0
                
                distance = int(math.hypot(centroid[0] - cloud.rect.centerx,
                                  centroid[1] - cloud.rect.centery))
                if distance < 100:
                    near_clouds += 1
                    for star in self.stars:
                        if star.rect.center == centroid:
                            star.size += 2

        # deactivate other active stars
        self.points.clear()
        for star in self.stars:
            star.active = False

  
def main():
    game = Game()
    game.start()

if __name__ == "__main__":
    main()
