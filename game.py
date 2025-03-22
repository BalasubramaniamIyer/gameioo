import sys
import pygame
from scripts.utils import load_image, load_images
from scripts.entities import PhysicsEntity
from scripts.tilemap import Tilemap

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
            'player': load_image('entities/player.png')
        }
        
        self.player = PhysicsEntity(self, 'player', (50, 50), (8, 15)) 

        self.tilemap = Tilemap(self, tile_size = 16)
    def run(self):
        while True:
            self.display.fill((14, 219, 248)) #this will set the background color of the game
            self.tilemap.render(self.display) #this will render the tilemap to the display
            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
            self.player.render(self.display)


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit() #this will exit the game

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True #this will move the image to the right
                    if event.key == pygame.K_UP:
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