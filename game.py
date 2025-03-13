import sys
import pygame

class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('Vegabong')
        self.screen = pygame.display.set_mode((640, 480)) #this will set the screen size of the game

        self.clock = pygame.time.Clock() #this will be used to control the frame rate of the game
    
        self.img = pygame.image.load('data\images\clouds\cloud_1.png') #this will load the image of the game
        
        self.img.set_colorkey((0, 0, 0)) #this will set the color of the image to be transparent
        
        self.img_pos = [160, 260] #this will set the position of the image
        
        self.movements = [False, False]

        self.collision_area = pygame.Rect(50, 50, 300,  50) #this will set the collision area of the image

    def run(self):
        while True:
            self.screen.fill((14, 219, 248)) #this will set the background color of the game

            self.img_pos[1] += (self.movements[0] - self.movements[1]) * 5 #this will move the image up and down
           
            self.screen.blit(self.img, self.img_pos) #this will draw the image on the screen

            img_r = pygame.Rect(self.img_pos[0], self.img_pos[1], self.img.get_width(), self.img.get_height()) #this will set the position of the image
            
            if img_r.colliderect(self.collision_area): #this will check if the image collides with the collision area
                pygame.draw.rect(self.screen, (0, 100, 255), self.collision_area) #this will draw the collision area on the screen
            else:
                pygame.draw.rect(self.screen, (0, 50, 155), self.collision_area)

            self.img_pos[1] += (self.movements[0] - self.movements[1]) * 5 #this will move the image up and down
            self.screen.blit(self.img, self.img_pos) #this will draw the image on the screen
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit() #this will exit the game

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.movements[0] = True
                    if event.key == pygame.K_DOWN:
                        self.movements[1] = True #this will move the image up and down  
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        self.movements[0] = False
                    if event.key == pygame.K_DOWN:
                        self.movements[1] = False            

            pygame.display.update()
            self.clock.tick(60) #this will make the game run at 60 frames per second

Game().run() #this will run the game        