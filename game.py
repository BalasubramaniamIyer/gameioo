import sys
import pygame

class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('Vegabong')
        self.screen = pygame.display.set_mode((640, 480)) #this will set the screen size of the game

        self.clock = pygame.time.Clock() #this will be used to control the frame rate of the game
    
        self.img = pygame.image.load('data\images\clouds\cloud_1.png') #this will load the image of the game

        self.img_pos = [0, 0] #this will set the position of the image

    def run(self):
        while True:
            self.screen.blit(self.img, self.img_pos) #this will draw the image on the screen
    
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit() #this will exit the game

            pygame.display.update()
            self.clock.tick(60) #this will make the game run at 60 frames per second

Game().run() #this will run the game        