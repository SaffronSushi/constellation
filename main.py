import pygame, random, math, sys
from star import Star
from cloud import Cloud

class Cursor(pygame.sprite.Sprite):
    def __init__(self):
        super(Cursor, self).__init__()
        self.image = pygame.Surface((16, 16))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        pygame.draw.rect(self.image, (200, 200, 255), self.rect, 3)

        self.alpha = 0

    def update(self):
        self.rect.center = pygame.mouse.get_pos()
        self.fade_in()

    def fade_in(self):
        self.alpha += 4
        if self.alpha > 255:
            self.alpha = 255
        self.image.set_alpha(self.alpha)

class Label(pygame.sprite.Sprite):
    def __init__(self, game, text = "", color=(255, 255, 255)):
        super(Label, self).__init__()
        self.screen = game.screen
        self.text = text
        self.color = color
        self.font = pygame.font.SysFont(None, 40)

    def update(self, text):
        self.image = self.font.render(text, True, self.color)
        self.rect = self.image.get_rect()
        self.rect.right = self.screen.get_width()

    def fade_in(self):
        self.image = self.image.set_alpha(self.alpha)
        
class Game():
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        
        self.FULLSCREEN = 0
        self.WINDOWED = 1
        self.DISPLAY_MODE = self.WINDOWED

        pygame.display.set_caption("mouse, LMB")
        self.icon = pygame.image.load("images/const_logo.bmp")
        pygame.display.set_icon(self.icon)
        self.res = (800, 600)
        self.set_display()
        self.screen_rect = self.screen.get_rect()
        self.framerate = 60

        self.bg_color = (20, 20, 80)
        self.bg = pygame.Surface(self.screen.get_size())
        self.bg.fill(self.bg_color)

        self.fg_color = (255, 255, 255)
        self.fg_alpha = 255
        self.fg = pygame.Surface(self.screen.get_size())
        self.fg.fill(self.fg_color)

        self.scoreboard = Label(self)
        self.start_button = Label(self, text="START")
        self.start_button.rect = self.screen_rect.center
        self.labels = pygame.sprite.Group(self.scoreboard)

        self.cursor = Cursor()
        self.stars = pygame.sprite.Group()
        self.clouds = pygame.sprite.Group()
        
        self.active_stars = []
        self.active_points =[]

        # load audio
        pygame.mixer.music.load("audio/bensound-sadday.mp3")
        pygame.mixer.music.set_volume(0.2)
        
    def start(self):
        self.running = True
        self.clock = pygame.time.Clock()
        # use the following start functions for testing 
        #self.start_clouds
        #self.start_stars()
        self.score = 0

        self.cloud_timer = 0
        self.cloud_delay = 0

        self.star_timer = 0
        self.star_delay = 0

        #self.__intro()
        #self.running = True

        #pygame.mixer.music.play(0)
        self.__main_loop()

    def stop(self):
        sys.exit()

    def __intro(self):
        while self.running:
            self.screen.blit(self.fg, (0, 0))
            pygame.display.flip()

    def __main_loop(self):
        while self.running:
            # get delta time
            self.dt = self.clock.tick(self.framerate) / 1000

            # convert timer to seconds
            self.timer = pygame.time.get_ticks() / 1000
            #print(int(self.timer))
            
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

    def fade(self):
        if self.timer < 5:
            self.fg_alpha -= 100 * self.dt
            self.fg.set_alpha(self.fg_alpha)
            self.screen.blit(self.fg, (0, 0))            

    def check_events(self):
        keys = pygame.key.get_pressed()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stop()
            #elif event.type == pygame.MOUSEBUTTONDOWN:
             #   self.submit_stars()

        if keys[pygame.K_f]:
            if self.DISPLAY_MODE == self.FULLSCREEN:
                self.DISPLAY_MODE = self.WINDOWED
            else:
                self.DISPLAY_MODE = self.FULLSCREEN
            self.set_display()

        if pygame.mouse.get_pressed() == (1, 0, 0):
            self.submit_stars()

        if keys[pygame.K_r]:
            self.start()

    def update(self):
        # update
        self.cursor.update()
        self.update_clouds()
        self.update_stars()

        # draw
        self.screen.blit(self.bg, (0, 0))
        self.clouds.draw(self.screen)
        self.draw_lines()
        self.stars.draw(self.screen)
        self.screen.blit(self.cursor.image, self.cursor.rect)

        if self.timer > 20:
            self.labels.update(str(self.score))
            self.labels.draw(self.screen)
        else:
            self.score = 0

        self.fade()
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

        return star

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
        for i in range(random.randint(5, 15)):
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
                    self.active_stars.append(star)
                if star.rect.center not in self.active_points:
                    self.active_points.append(star.rect.center)

        # remove dead stars
        for star in self.stars:
            if star.dead:
                if star in self.active_stars:
                    self.active_stars.remove(star)
                if star.rect.center in self.active_points:
                    self.active_points.remove(star.rect.center)
                self.stars.remove(star)
            # REMOVE STARS THAT ARE OVERSHADOWED BY LARGER STARS

        # make new stars less frequently based on timer
        # BEING TAUGHT WORDS THE FIRST TIME
        if self.timer > 7 and self.timer < 30:
            self.star_delay = 2
            self.star_timer += self.dt
            if self.star_timer >= self.star_delay:
                self.star_timer = 0
                self.make_star("random", size=4)
                
        elif self.timer > 30 and self.timer < 60:
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

        # create new clouds based on timer
        # NEW PERCEPTIONS AT BEGINNING
        if self.timer > 3 and self.timer < 7:
            self.cloud_delay = 0
            if self.cloud_timer >= self.cloud_delay:
                self.cloud_timer = 0
                for i in range(4):
                    size = random.randint(5, 100)
                    radius = int(size / 2)
                    pos = (random.randint(0, self.screen.get_width()),
                           random.randint(0, self.screen.get_height()))
                    self.make_cloud(pos, size)

        elif self.timer > 7:
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
        if len(self.active_points) > 1:
            pygame.draw.lines(self.screen, (200, 200, 255), True,
                              self.active_points, 2)

    def submit_stars(self):
        """ creates a new star based on
            currently selected stars

            - getting points make stars grow
              and clouds fade

            - the amount that stars grow depends
              on the number and size of stars
              submitted, as well as their
              proximity to nearby clouds
              (and number of clouds)

            - the amount that clouds fade depends
              on the above as well, this also
              applies to points gained

            - only clouds that are within the
              lines drawn should be included,
              i.e., the centroid

            - amount of points gained is 
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
                centroid = self.active_points[0]
                center_star = self.active_stars[0]
                
            elif len(self.active_stars) > 1:
                # find centroid of all points
                x = [p[0] for p in self.active_points]
                y = [p[1] for p in self.active_points]
                centroid = (sum(x) / len(self.active_points),
                            sum(y) / len(self.active_points))
                center_star = self.make_star(centroid, size=4)

            # check for contact with clouds
            for cloud in self.clouds:
                near_clouds = 0
                '''
                distance = int(math.hypot(centroid[0] - cloud.rect.centerx,
                                  centroid[1] - cloud.rect.centery))
                #if distance < cloud.radius:
                '''
                if pygame.sprite.collide_circle(center_star, cloud):
                    near_clouds += 1
                    print("H")

                    # update clouds, stars and score
                    cloud.life -= 40
                    # POINTS EARNED GOES UP WITH AGE (credibility?)
                    self.score += int(self.timer /
                            10 + near_clouds + len(self.active_stars))
                    for star in self.active_stars:
                        star.size += 2

        # deactivate other active stars
        self.active_stars.clear()
        self.active_points.clear()
        for star in self.stars:
            star.active = False

  
def main():
    game = Game()
    game.start()

if __name__ == "__main__":
    main()
