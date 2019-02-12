import pygame, random, math, sys
from star import Star
from cloud import Cloud

class Cursor(pygame.sprite.Sprite):
    def __init__(self):
        super(Cursor, self).__init__()
        self.size = (16, 16)
        self.image = pygame.Surface(self.size)
        self.image.set_colorkey((0, 0, 0))
        self.color = (175, 175, 255)

        self.default_img = pygame.Surface(self.size)
        self.default_img.set_colorkey((0, 0, 0))
        self.rect = self.default_img.get_rect()
        pygame.draw.rect(self.default_img, self.color, self.rect, 3)

        self.active_img = self.default_img.copy()
        self.active_img.fill(self.color)

        self.alpha = 0
        self.active = False

    def update(self):
        if self.active :
            self.image = self.active_img
        else:
            self.image = self.default_img
    
        self.rect.center = pygame.mouse.get_pos()

    def fade_in(self):
        self.alpha += 0.2
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

    def update(self):
        self.image = self.font.render(self.text, True, self.color)
        self.rect = self.image.get_rect()

    def fade_in(self):
        self.image = self.image.set_alpha(self.alpha)
        
class Game():
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        
        self.FULLSCREEN = 0
        self.WINDOWED = 1
        self.DISPLAY_MODE = self.WINDOWED

        pygame.display.set_caption("A Star At Dawn")
        self.icon = pygame.image.load("images/const_logo.bmp")
        pygame.display.set_icon(self.icon)
        self.res = (800, 600)
        self.set_display()
        self.screen_rect = self.screen.get_rect()
        self.framerate = 60
        self.dt = self.framerate / 1000

        self.bg_color = (20, 20, 80)
        self.bg = pygame.Surface(self.screen.get_size())
        self.bg.fill(self.bg_color)

        self.fg_color = (255, 255, 255)
        self.fg_alpha = 255
        self.fg = pygame.Surface(self.screen.get_size())
        self.fg.fill(self.fg_color)

        self.cursor = Cursor()
        self.stars = pygame.sprite.Group()
        self.clouds = pygame.sprite.Group()
        
        self.active_stars = []
        self.active_points =[]

        # load audio
        pygame.mixer.music.load("audio/bensound-sadday.mp3")
        pygame.mixer.music.set_volume(0.2)
        
    def start(self):
        while True:
            self.stars.empty()
            self.clouds.empty()
            # use the following start functions for testing 
            #self.test_clouds()
            self.test_stars()
            
            self.clock = pygame.time.Clock()

            self.score = 0
            self.cloud_timer = 0
            self.cloud_delay = 0
            self.star_timer = 0
            self.star_delay = 0

            self.intro()
            self.timer = 0
            pygame.mixer.music.play(-1)
            self.__main_loop()
            pygame.mixer.music.stop()
            self.fg_alpha = 255

    def stop(self):
        sys.exit()

    def intro(self):
        font = pygame.font.SysFont(None, 25)
        text = ("The best and most beautiful things in the world",
                "cannot be seen or event touched.",
                "They must be felt with the heart.",
                "- Helen Keller",
                "",
                "Is it really possible to someone else what one feels?",
                "- Leo Tolstoy",
                "",
                "For last year's words belong to last year's language",
                "And next year's words await another voice.",
                "- T.S. Elliot",
                "",
                "A classic is a book that has never finished saying",
                "what it has to say.",
                "- Italo Calvino",
                "",
                "Words are, of course,",
                "the most powerful drug used by mankind.",
                "- Rudyard Kipling",
                "",
                "Words are a pretext.",
                "It is the inner bond that draws one person to another,",
                "not words.",
                "- Rumi",
                "",
                "Because event the smallest of words",
                "can be the ones to hurt you, or save you.",
                "- Natsuki Takaya")
        labels_1 = []
        for line in text:
            label = font.render(line, 1, (0, 0, 0))
            labels_1.append(label)

        control_text= ("",
                       "",
                       "PRESS ENTER TO START")
        labels_2 = []
        for line in control_text:
            label = font.render(line, 1, (0, 0, 0))
            labels_2.append(label)



        running = True
        while running:
            self.dt = self.clock.tick(self.framerate) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.stop()
                    elif event.key == pygame.K_RETURN:
                        running = False
                        self.timer = 0
    
            self.screen.blit(self.fg, (0, 0))
            for i in range(len(labels_1)):
                self.screen.blit(labels_1[i], (40, 20*i))
            for i in range(len(labels_2)):
                self.screen.blit(labels_2[i], (550, 20*i))
            pygame.display.flip()

    def __main_loop(self):
        self.scoreboard = Label(self)
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stop()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

            pygame.mouse.set_visible(False)
            # get delta time
            self.dt = self.clock.tick(self.framerate) / 1000
            # convert timer to seconds
            self.timer = pygame.time.get_ticks() / 1000
            #print(int(self.timer))
            
            self.check_events()
            self.update()

    def ending(self):
        running = True

    def set_display(self):
        """ creates either a fullscreen or
            windowed display based on the
            current display state
        """
        if self.DISPLAY_MODE == self.FULLSCREEN:
            self.screen = pygame.display.set_mode(self.res, pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(self.res)

    def fade_in(self):
        if self.fg_alpha > 0:
            self.fg_alpha -= 100 * self.dt
            self.fg.set_alpha(self.fg_alpha)
            self.screen.blit(self.fg, (0, 0))            

    def check_events(self):
        keys = pygame.key.get_pressed()
        
        # screen change events
        if keys[pygame.K_f]:
            if self.DISPLAY_MODE == self.FULLSCREEN:
                self.DISPLAY_MODE = self.WINDOWED
            else:
                self.DISPLAY_MODE = self.FULLSCREEN
            self.set_display()

        # mouse events
        if pygame.mouse.get_pressed() == (1, 0, 0):
            self.cursor.active = True
        elif pygame.mouse.get_pressed() == (0, 0, 0):
            if self.cursor.active:
                self.cursor.active = False
                self.submit_stars()



    def update(self):
        # update
        self.cursor.update()
        self.update_clouds()

        # draw
        self.screen.blit(self.bg, (0, 0))
        self.clouds.draw(self.screen)
        self.draw_lines()
        self.draw_poly()
        self.update_stars()
        self.stars.draw(self.screen)
        self.screen.blit(self.cursor.image, self.cursor.rect)

        if self.timer > 0:#40
            self.scoreboard.text = str(int(self.score))
            self.scoreboard.update()
            self.scoreboard.rect.right = self.screen_rect.width
            self.screen.blit(self.scoreboard.image, self.scoreboard.rect)
        else:
            self.score = 0

        self.fade_in()
        pygame.display.flip()

    def make_star(self, pos, size="random"):
        if size == "random":
            size = random.randint(5, 15)
        elif size == "medium":
            size = random.randint(5, 8)
        elif size == "small":
            size = 5
            
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

    def test_stars(self):
        """ creates new initial group of
            stars at start of game
        """
        self.stars.empty()
        for i in range(random.randint(8, 16)):
            self.make_star("random")

    def test_clouds(self):
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
        self.stars.update(self.dt, self.cursor, self.stars)

        for star in self.stars:
            # check for active stars
            if star.active:
                icon_rect = pygame.Rect(star.rect.x - 3, star.rect.y - 3,
                                star.rect.width + 6, star.rect.width + 6)
                pygame.draw.rect(self.screen, star.active_clr, icon_rect, 2)

                if star not in self.active_stars:
                    self.active_stars.append(star)
                if star.rect.center not in self.active_points:
                    self.active_points.append(star.rect.center)

            # check for inactive stars
            elif not star.active:
                if star in self.active_stars:
                    self.active_stars.remove(star)
                if star.rect.center in self.active_points:
                    self.active_points.remove(star.rect.center)

            # check for dead stars
            elif star.dead:
                if star in self.active_stars:
                    self.active_stars.remove(star)
                if star.rect.center in self.active_points:
                    self.active_points.remove(star.rect.center)
                self.stars.remove(star)
            # REMOVE STARS THAT ARE OVERSHADOWED BY LARGER STARS

        # make new stars less frequently based on timer
        # BEING TAUGHT WORDS THE FIRST TIME
        # LEARN TO USE WORDS INDIVIDUALLY
        if self.timer > 5 and self.timer < 40:
            self.star_delay = 5
            self.star_timer += self.dt
            if self.star_timer >= self.star_delay:
                self.star_timer = 0
                self.make_star("random", size="small")
                
        # MORE FREQUENT, LEARN TO STRING TOGETHER
        elif self.timer > 30 and self.timer < 60:
            self.star_delay = 7
            self.star_timer += self.dt
            if self.star_timer >= self.star_delay:
                self.star_timer = 0
                self.make_star("random", size="medium")

        elif self.timer > 50:
            self.star_delay = 15
            self.star_timer += self.dt
            if self.star_timer >= self.star_delay:
                self.star_timer = 0
                self.make_star("random", size="medium")

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
        
        if self.timer > 10:
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

    def draw_poly(self):
        if self.cursor.active and len(self.active_points) > 2:
            pygame.draw.polygon(self.screen,
                    (200, 200, 255), self.active_points)

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
        collided = False
        
        # find centroid of all active stars
        if self.active_stars:
            if len(self.active_stars) == 1:
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
                    collided = True
                    near_clouds += 1
                    
                    # update clouds, stars and score
                    cloud.life -= 40
                    
                    # POINTS EARNED GOES UP WITH AGE (credibility?)
                    self.score += int(self.timer /
                            10 + near_clouds + len(self.active_stars))
                    
            for star in self.active_stars:
                if collided:
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
