import pygame, random, math, sys, time
from star import Star
from cloud import Cloud
# Start
# End

class Cursor(pygame.sprite.Sprite):
    def __init__(self):
        super(Cursor, self).__init__()
        self.size = (16, 16)
        self.image = pygame.Surface(self.size)
        self.image.set_colorkey((0, 0, 0))
        self.color = (200, 200, 240)

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
        self.fade_in()

    def fade_in(self):
        self.alpha += .5
        if self.alpha > 200:
            self.alpha = 200
        self.image.set_alpha(self.alpha)

class Label(pygame.sprite.Sprite):
    def __init__(self, game, text = "", size=40, pos=(0, 0), color=(255, 255, 255)):
        super(Label, self).__init__()
        self.screen = game.screen
        self.text = text
        self.pos = pos
        self.color = color
        self.font = pygame.font.SysFont(None, size)

        self.timer = 0

    def update(self):
        self.image = self.font.render(self.text, True, self.color)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

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

        self.fg_color = (240, 240, 240)
        self.fg_alpha = 255
        self.fg = pygame.Surface(self.screen.get_size())
        self.fg.fill(self.fg_color)

        self.cursor = Cursor()
        self.stars = pygame.sprite.Group()
        self.clouds = pygame.sprite.Group()
        self.labels = pygame.sprite.Group()
        
        self.active_stars = []
        self.active_points =[]

        # load audio
        pygame.mixer.music.load("audio/bensound-sadday.mp3")
        pygame.mixer.music.set_volume(0.2)

        self.sound_effect = pygame.mixer.Sound("audio/point_sound.wav")

        # create timestamps for different game events
        self.ts = {
            "game_start":0,
            "game_end":295,
            
            "fade_in_end":10,
            "fade_out_start":260,
            
            "star_1_start":0,
            "star_1_end":30,
            "star_2_start":30,
            "star_2_end":175,
            "star_3_start":175,
            
            "cloud_1_start":0,
            "cloud_1_end":20,
            "cloud_2_start":20,
            "cloud_2_end":200,
            "cloud_3_start":200,
            
            "score_start":50,
            "score_end":265,
            
            "end_event":265
            }

    def start(self):
        while True:
            self.stars.empty()
            self.clouds.empty()
            # use the following start functions for testing 
            #self.test_clouds()
            #self.test_stars()
            
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
        text = ("",
                "The best and most beautiful things in the world",
                "cannot be seen or event touched.",
                "They must be felt with the heart.",
                "- Helen Keller",
                "",
                "Is it really possible to tell someone else what one feels?",
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
            label = font.render(line, 1, self.bg_color)
            labels_2.append(label)

        self.fg_alpha = 255
        self.fg.set_alpha(self.fg_alpha)

        running = True
        while running:
            self.dt = self.clock.tick(self.framerate) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stop()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.stop()
                    elif event.key == pygame.K_f:
                        if self.DISPLAY_MODE == self.FULLSCREEN:
                            self.DISPLAY_MODE = self.WINDOWED
                        else:
                            self.DISPLAY_MODE = self.FULLSCREEN
                        self.set_display()
                    elif event.key == pygame.K_RETURN:
                        running = False

            self.start_ticks = pygame.time.get_ticks() / 1000
            
            self.screen.blit(self.fg, (0, 0))
            for i in range(len(labels_1)):
                self.screen.blit(labels_1[i], (20, 20*i))
            for i in range(len(labels_2)):
                self.screen.blit(labels_2[i], (550, 20*i))
            pygame.display.flip()

    def __main_loop(self):
        self.scoreboard = Label(self)
        
        self.main_running = True
        while self.main_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stop()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.main_running = False

            pygame.mouse.set_visible(False)
            # get delta time
            self.dt = self.clock.tick(self.framerate) / 1000
            # convert timer to seconds
            # reset timer based on intro timer
            self.timer = pygame.time.get_ticks() / 1000 - self.start_ticks
            #print(int(self.timer))
            print(int(self.timer))
            
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

    def fade_screen(self):
        """ changes foreground alpha based
            on different time stamps
        """
        # fade in
        if self.timer < self.ts["fade_in_end"]:
            self.fg_alpha -= 70 * self.dt
            if self.fg_alpha < 0:
                self.fg_alpha = 0
            self.fg.set_alpha(self.fg_alpha)
            self.screen.blit(self.fg, (0, 0))
            
        # fade out and end game
        # game lasts 300 seconds
        elif self.timer > self.ts["fade_out_start"]:
            # roughly 40 second fade time
            self.fg_alpha += 10 * self.dt
            if self.fg_alpha >= 255:
                self.fg_alpha = 255
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
        if pygame.mouse.get_pressed() != (0, 0, 0):
            self.cursor.active = True
        elif pygame.mouse.get_pressed() == (0, 0, 0):
            if self.cursor.active:
                self.submit_stars()
                self.cursor.active = False


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
        self.show_score()
        self.fade_screen()
        pygame.display.flip()

        if self.timer >= self.ts["game_end"]:
            self.main_running = False

    def make_star(self, pos="random", size="random"):
        if size == "random":
            size = random.randint(5, 15)
        elif size == "large":
            size = random.randint(6, 8)
        elif size == "medium":
            size = 5
        elif size == "small":
            size = 4
            
        if pos == "random":
            radius = int(size / 2)
            pos = (random.randint(radius,
                    self.screen.get_width() - radius),
                   random.randint(radius,
                    self.screen.get_height() - radius))
            
        star = Star(self, pos, size)
        self.stars.add(star)

        return star

    def make_cloud(self, pos="random", size="random", life="random"):
        if size == "random":
            size = random.randint(5, 100)
            radius = int(size / 2)

        if pos == "random":
            pos = (random.randint(0, self.screen.get_width()),
               random.randint(0, self.screen.get_height()))
            
        cloud = Cloud(self, pos, size)
        if life != "random":
            life = life
            
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
        self.star_timer += self.dt

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
            if star.dead:
                if star in self.active_stars:
                    self.active_stars.remove(star)
                if star.rect.center in self.active_points:
                    self.active_points.remove(star.rect.center)
                self.stars.remove(star)

        # STAGE 1: small words arrive one at a time
        if (self.timer > self.ts["star_1_start"] and
            self.timer < self.ts["star_1_end"]):
            self.star_delay = 9
            if self.star_timer >= self.star_delay:
                self.star_timer = 0
                self.make_star(size="small")
                
        # STAGE 2: learn to use
        elif (self.timer > self.ts["star_2_start"] and
            self.timer < self.ts["star_2_end"]):
            self.star_delay = 6
            if self.star_timer >= self.star_delay:
                self.star_timer = 0
                self.make_star(size="medium")
                
        # STAGE 3: more focus on what's predetermined
        elif (self.timer > self.ts["star_3_start"]):
            self.star_delay = 3
            if self.star_timer >= self.star_delay:
                self.star_timer = 0
                self.make_star(size="medium")

        # ENDING
        if self.timer > self.ts["end_event"]:
            for star in self.stars:
                self.make_cloud(star.rect.center, size=16, life=200)
                self.make_cloud((self.screen_rect.width - 10, 8),
                                size=16, life=200)
                self.make_cloud(self.cursor.rect.center, size=16, life=200)

                star.size = 3

    def update_clouds(self):
        """ maintains clouds based on
            current state of a cloud,
            and generates new clouds
        """
        self.clouds.update(self.dt)
        self.cloud_timer += self.dt

        # remove cloud if dead/offscreen
        for cloud in self.clouds:
            if cloud.dead:
                self.clouds.remove(cloud)
        
        # STAGE 1: burst of sensation
        if (self.timer > self.ts["cloud_1_start"] and
            self.timer < self.ts["cloud_1_end"]):
            self.cloud_delay = 0
            if self.cloud_timer >= self.cloud_delay:
                self.cloud_timer = 0
                for i in range(3):
                    self.make_cloud()

        # STAGE 2: less new sensation
        elif (self.timer > self.ts["cloud_2_start"] and
            self.timer < self.ts["cloud_2_end"]):
            self.cloud_delay = random.randint(1, 4)
            if self.cloud_timer >= self.cloud_delay:
                self.cloud_timer = 0
                self.cloud_delay = random.uniform(0, 1)
                self.make_cloud()

        # STAGE 3: rarely suprised
        elif self.timer > self.ts["cloud_3_start"]:
            self.cloud_delay = random.randint(6, 12)
            if self.cloud_timer >= self.cloud_delay:
                self.cloud_timer = 0
                self.cloud_delay = random.uniform(0, 1)
                self.make_cloud()

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
              and clouds fades

            - if multiple stars are used in
              a submission, a new star will
              be created at the centroid of
              those stars

            - if there is a collision between
              a cloud and the central point,
              points will be earned

            - the amount of points earned
              per cloud depends on the
              number of active star
        """
        collided = False
    
        if self.active_stars:
            
            # find center point of all active stars
            if len(self.active_stars) == 1:
                centroid = self.active_points[0]
                center_star = self.active_stars[0]

            # if multiple stars active, a new star is made
            elif len(self.active_stars) > 1:
                x = [p[0] for p in self.active_points]
                y = [p[1] for p in self.active_points]
                centroid = (sum(x) / len(self.active_points),
                            sum(y) / len(self.active_points))
                center_star = self.make_star(centroid, size=4)

            # check for collisions with clouds
            for cloud in self.clouds:
                if pygame.sprite.collide_circle(center_star, cloud):
                    collided = True

                    # update score
                    points = int(5 / len(self.active_points))
                    if points < 1:
                        points = 1
                    self.score += points

                    # calculate position of score icon
                    if center_star.rect.collidepoint(cloud.rect.center):
                        pos = (center_star.rect.centerx,
                           center_star.rect.y - center_star.rect.height)
                    else:
                        pos = cloud.rect.center
                        
                    self.show_new_score(points, pos)
                    
                    # update clouds
                    cloud.life -= 60

                    # play sound effect
                    self.sound_effect.play()

            # update stars
            if collided:
                for star in self.active_stars:
                        star.size += 1
                if len(self.active_stars) < 2:
                    center_star.size += 1

        # disable active stars
        self.active_stars.clear()
        self.active_points.clear()
        for star in self.stars:
            star.active = False

    def show_score(self):
        if self.timer > self.ts["score_start"]:
            if not self.timer > self.ts["end_event"]:   
                self.scoreboard.text = str(int(self.score))
            else:
                self.scoreboard.text = ""

            self.scoreboard.update()
            self.scoreboard.rect.right = self.screen_rect.width
            self.scoreboard.rect.top = 0
            self.screen.blit(self.scoreboard.image, self.scoreboard.rect)

            self.labels.update()
            self.labels.draw(self.screen)
            for label in self.labels:
                label.timer += 1 * self.dt
                if label.timer >= 1:
                    self.labels.remove(label)
                    
        else:
            self.score = 0
            self.labels.empty()

    def show_new_score(self, points, pos):
        """ displays a text icon near collision
            to better display points earned
        """
        score = Label(self, "+" + str(points), size=30,
                      pos=pos, color=(255, 150, 150))
        self.labels.add(score)

  
def main():
    game = Game()
    game.start()

if __name__ == "__main__":
    main()
