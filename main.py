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

        self.text = ""
        self.font = pygame.font.SysFont(None, 40)

    def update(self, text):
        self.image = self.font.render(text, True, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.right = self.screen.get_width()
        

class Game():
    def __init__(self):
        pygame.init()
        self.FULLSCREEN = 0
        self.WINDOWED = 1
        self.DISPLAY_MODE = self.WINDOWED

        pygame.display.set_caption("click to select, space to enter")
        self.res = (800, 600)
        self.set_display()
        self.framerate = 60

        self.bg_color = (20, 20, 80)
        self.bg = pygame.Surface(self.screen.get_size())
        self.bg.fill(self.bg_color)

        self.cursor = Cursor()
        self.stars = pygame.sprite.Group()
        self.clouds = pygame.sprite.Group()

        self.scoreboard = Label(self)
        self.labels = pygame.sprite.Group(self.scoreboard)
        
        self.active_stars = {}
        
    def start(self):
        self.running = True
        self.clock = pygame.time.Clock()
        self.start_stars()
        self.score = 0

        self.cloud_timer = 0
        self.cloud_delay = 0

        self.star_timer = 0
        self.star_delay = 0

        self.__main_loop()

    def stop(self):
        self.running = False

    def __main_loop(self):
        while self.running:
            # get delta time
            self.dt = self.clock.tick(self.framerate) / 1000
            # convert timer to seconds
            self.timer = pygame.time.get_ticks() / 1000
        
            pygame.mouse.set_visible(False)

            self.check_events()
            self.update()
            print(self.timer)

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
        self.labels.update(str(self.score))

        # draw
        self.screen.blit(self.bg, (0, 0))
        self.clouds.draw(self.screen)
        self.draw_lines()
        self.stars.draw(self.screen)
        self.screen.blit(self.cursor.image, self.cursor.rect)
        self.labels.draw(self.screen)
        print(len(self.active_stars))

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
        for i in range(random.randint(8, 16)):
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
        
        # add active stars to list
        for star in self.stars:
            if star.active:
                if star not in self.active_stars:
                    self.active_stars.update({star:star.rect.center})

        # remove dead stars
        for star in self.stars:
            if star.dead:
                if star in self.active_stars:
                    self.active_stars.pop(star)
                self.stars.remove(star)
            # REMOVE STARS THAT ARE OVERSHADOWED BY LARGER STARS

        # make new stars less frequently based on timer
        # BEING TAUGHT WORDS THE FIRST TIME
        if self.timer < 10:
            self.star_delay = 2
            self.star_timer += self.dt
            if self.star_timer >= self.star_delay:
                self.star_timer = 0
                self.make_star("random", size=4)
                
        elif self.timer > 50 and self.timer < 60:
            self.star_delay = 7
            self.star_timer += self.dt
            if self.star_timer >= self.star_delay:
                self.star_timer = 0
                self.make_star("random", size="random")

        elif self.timer > 50:
            self.star_delay = 15
            self.star_timer += self.dt
            if self.star_timer >= self.star_delay:
                self.star_timer = 0
                self.make_star("random", size="random")

    def update_clouds(self):
        """ maintains clouds based on
            current state of a cloud,
            and generates new clouds
        """
        self.clouds.update(self.dt)
        self.cloud_timer += self.dt

        # remove if dead/offscreen
        for cloud in self.clouds:
            if cloud.dead:
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
        if len(self.active_stars) > 1:
            points = tuple(self.active_stars.values())
            pygame.draw.lines(self.screen, (200, 200, 255), True,
                              points, 2)

    def submit_stars(self):
        """ creates a new star based on
            currently selected stars

            - getting points make stars grow
              and clouds fade

            - the amount that stars grow depends
              on the number and size of stars
              submitted, as well as their
              proximity to nearby clouds

            - the amount that clouds fade depends
              on the above as well, this also
              applies to points gained

            - amount of points gained is not
              affected by the transparency
              of the cloud

            - if multiple stars are used in
              a submission, a new star will
              be created at the centroid of
              those stars, ONLY if points
              are gained
        """
        # find centroid of all active stars
        if self.active_stars:
            if len(self.active_stars) < 2:
                centroid = self.active_stars.values()
                
            elif len(self.active_stars) > 1:
                # find centroid of all points
                points = self.active_stars.values()
                x = [p[0] for p in points]
                y = [p[1] for p in points]
                centroid = (sum(x) / len(points),
                            sum(y) / len(points))
                # create new star at center point
                size = (16/ len(points))
                self.make_star(centroid, size)

            for cloud in self.clouds:
                near_clouds = 0
                distance = int(math.hypot(centroid[0] - cloud.rect.centerx,
                                  centroid[1] - cloud.rect.centery))
                if distance < 50:
                    near_clouds += 1
                    for star in self.active_stars:
                        self.score += int(star.size)
                        cloud.life -= 20 / (distance + len(self.active_stars)
                                            * star.size)
                    
                        star.size += 10 / len(self.active_stars)

        # deactivate other active stars
        self.active_stars.clear()
        for star in self.stars:
            star.active = False

  
def main():
    game = Game()
    game.start()

if __name__ == "__main__":
    main()
