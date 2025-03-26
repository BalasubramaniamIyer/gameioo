import sys
import pygame
from scripts.utils import load_image, load_images
from scripts.entities import PhysicsEntity
from scripts.tilemap import Tilemap
from scripts.clouds import Clouds

class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('Vegabong')
        self.screen = pygame.display.set_mode((640, 480)) #this will set the screen size of the game

        self.display = pygame.Surface((320, 240)) #this will set the display size of the game. it is used to render the game at a lower display then scale it up to the screen size

        self.clock = pygame.time.Clock() #this will be used to control the frame rate of the game
        
        self.movement = [ False, False]
        

        self.assets = {
            'decor': load_images('tiles/decor'),
            'grass': load_images('tiles/grass'),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone'),
            'player': load_image('entities/player.png'),
            'background': load_image('background.png'),
            'clouds': load_images('clouds')
        }

        self.clouds = Clouds(self.assets['clouds'], count=16) #this will create a list of clouds
        
        self.player = PhysicsEntity(self, 'player', (50, 50), (8, 15)) 

        self.tilemap = Tilemap(self, tile_size = 16)

        self.scroll = [0, 0] #this will be used to scroll the tilemap

    def run(self):
        while True:
            self.display.blit(self.assets['background'], (0, 0)) #this will clear the display
            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30 #this will scroll the tilemap to the left or right depending on the player position
            self.scroll[1] += (self.player.rect().centerx - self.display.get_height() / 2 - self.scroll[1]) / 30
            render_scroll = (int(self.scroll[0]), int(self.scroll[1])) #this will set the scroll position of the tilemap
            self.clouds.update()
            self.clouds.render(self.display, offset = render_scroll)
            self.tilemap.render(self.display, offset = render_scroll) #this will render the tilemap to the display
            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
            self.player.render(self.display, offset= render_scroll)


            for event in pygame.event.get():  
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit() #this will exit the game

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True #this will move the image to the right
                    if event.key == pygame.K_SPACE:
                        self.player.velocity[1] = -3
                                     
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False            

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0)) #this will scale the display to the screen size
            pygame.display.update()
            self.clock.tick(60) #this will make the game run at 60 frames per second

Game().run() #this will run the game        