import sys
import pygame
import random
import math
from scripts.utils import load_image, load_images, Animation
from scripts.entities import PhysicsEntity, Player
from scripts.tilemap import Tilemap
from scripts.clouds import Clouds
from scripts.particle import Particle

class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('Vegabong')
        self.screen = pygame.display.set_mode((640, 480)) #this will set the screen size of the game

        self.display = pygame.Surface((320, 240)) #this will set the display size of the game. it is used to render the game at a lower display then scale it up to the screen size

        self.clock = pygame.time.Clock() #this will be used to control the frame rate of the game
        
        self.movement = [False, False]
        

        self.assets = {
            'decor': load_images('tiles/decor'),
            'grass': load_images('tiles/grass'),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone'),
            'player': load_image('entities/player.png'),
            'background': load_image('background.png'),
            'clouds': load_images('clouds'),
            'player/idle': Animation(load_images('entities/player/idle'), img_dur=6),
            'player/run': Animation(load_images('entities/player/run'), img_dur=4),
            'player/jump': Animation(load_images('entities/player/jump')),
            'player/slide': Animation(load_images('entities/player/slide')),
            'player/wall_slide': Animation(load_images('entities/player/wall_slide')),  
            'particle/leaf': Animation(load_images('particles/leaf'), img_dur= 20, loop = False),
            'particle/particle': Animation(load_images('particles/particle'), img_dur= 6, loop=False),     

        }

        print(self.assets)

        self.clouds = Clouds(self.assets['clouds'], count=16) #this will create a list of clouds
        
        self.player = Player(self, (50, 50), (8, 15)) 

        self.tilemap = Tilemap(self, tile_size = 16)
        self.tilemap.load('map.json') #this will load the tilemap from a file

        self.scroll = [0, 0] #this will be used to scroll the tilemap
        self.leaf_spawners = []
        for tree in self.tilemap.extract([('large_decor', 2)], keep=True):
            self.leaf_spawners.append(pygame.Rect(4 + tree['pos'][0], 4 + tree['pos'][1], 23, 13)) #this will create a list of leaf spawners
        
        self.particles = [] #this will create a list of particles
        self.scroll = [0 , 0]

    def run(self):
        while True:
            self.display.blit(self.assets['background'], (0, 0)) #this will clear the display

            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30 #this will scroll the tilemap to the left or right depending on the player position
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30
            render_scroll = ((self.scroll[0]), (self.scroll[1])) #this will set the scroll position of the tilemap

            for rect in self.leaf_spawners:
                if random.random() * 49999 < rect.width * rect.height:
                    pos = (rect.x + random.random() * rect.width, rect.y + random.random() * rect.height)
                    self.particles.append(Particle(self, 'leaf', pos, velocity=[-0.1, 0.3], frame=random.randint(0, 20))) #this will create a new particle at the given position

            self.clouds.update()
            self.clouds.render(self.display, offset = render_scroll)

            self.tilemap.render(self.display, offset = self.scroll) #this will render the tilemap to the display

            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 1)) #this will update the player position and animation
            self.player.render(self.display, offset= self.scroll)

            for particle in self.particles.copy():
                kill = particle.update()
                particle.render(self.display, offset= render_scroll)
                if particle.type == 'leaf':
                    particle.pos[0] += math.sin(particle.animation.frame * 0.035) *0.3 
                if kill:
                    self.particles.remove(particle)
                    


            for event in pygame.event.get():  
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit() #this will exit the game

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.movement[0] = True
                    if event.key == pygame.K_d:
                        self.movement[1] = True #this will move the image to the right
                    if event.key == pygame.K_SPACE :
                        self.player.jump()
                    if event.key == pygame.K_w:
                        self.player.dash()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_d:
                        self.movement[1] = False            

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0)) #this will scale the display to the screen size
            pygame.display.update()
            self.clock.tick(60) #this will make the game run at 60 frames per second

Game().run() #this will run the game        