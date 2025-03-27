import sys
import pygame
from scripts.utils import load_images #this will load the images from the tiles folder
from scripts.tilemap import Tilemap

RENDER_SCALE = 2.0 #this will set the scale of the render

class Editor:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('editor')
        self.screen = pygame.display.set_mode((640, 480)) #this will set the screen size of the game

        self.display = pygame.Surface((320, 240)) #this will set the display size of the game. it is used to render the game at a lower display then scale it up to the screen size

        self.clock = pygame.time.Clock() #this will be used to control the frame rate of the game
        
    

        self.assets = {
            'decor': load_images('tiles/decor'),
            'grass': load_images('tiles/grass'),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone'),
           
        }
        self.movement = [False, False,False, False] #this will be used to move the player left and right

        self.tilemap = Tilemap(self, tile_size = 16)

        try:
            self.tilemap.load('map.json') #this will load the tilemap from a file
        except:
            self.tilemap = Tilemap(self, tile_size = 16) #this will create a new tilemap if the file does not exist
        self.scroll = [0, 0] #this will be used to scroll the tilemap

        self.tile_list = list(self.assets)
        self.tile_group = 0 
        self.tile_variant = 0
        self.clicking = False #this will be used to check if the mouse is clicking
        self.right_clicking = False
        self.shift = False #this will be used to check if the shift key is pressed
        self.on_grid = True #this will be used to check if the mouse is on the grid
    def run(self):
        while True:
            self.display.fill((0, 0, 0)) #this will clear the display

            self.scroll[0] += (self.movement[1] - self.movement[0]) * 2 #this will scroll the tilemap to the left or right depending on the player position
            self.scroll[1] += (self.movement[3] - self.movement[2]) * 2 
            
            render_scroll = (int(self.scroll[0]), int(self.scroll[1])) #this will set the scroll position of the tilemap

            self.tilemap.render(self.display, offset= render_scroll) #this will render the tilemap to the display

            current_tile_img = self.assets[self.tile_list[self.tile_group]][self.tile_variant].copy() #this will get the current tile image
            current_tile_img.set_alpha(100) #this will set the alpha of the image to 100

            mpos = pygame.mouse.get_pos() #this will get the mouse position
            mpos = (mpos[0] / RENDER_SCALE, mpos[1] / RENDER_SCALE) #this will set the mouse position to the render scale
            tile_pos = (int((mpos[0] +self.scroll[0]) // self.tilemap.tile_size), int((mpos[1] + self.scroll[1]) // self.tilemap.tile_size)) #this will set the tile position to the tile size

            if self.on_grid:
                self.display.blit(current_tile_img, (tile_pos[0] * self.tilemap.tile_size - self.scroll[0], tile_pos[1] * self.tilemap.tile_size - self.scroll[1])) #this will blit the image to the display
            else:
                self.display.blit(current_tile_img, mpos)
            if self.clicking and self.on_grid:
                self.tilemap.tilemap[str(tile_pos[0]) + ';' + str(tile_pos[1])] = {'type': self.tile_list[self.tile_group], 'variant': self.tile_variant, 'pos': tile_pos} #this will set the tile type and variant to the tile position
           
            if self.right_clicking:
                tile_loc = str(tile_pos[0]) + ';' + str(tile_pos[1]) #this will set the tile location to the tile position
                if tile_loc in self.tilemap.tilemap:
                    del self.tilemap.tilemap[tile_loc]
                for tile in self.tilemap.offgrid_tiles.copy():
                    tile_img = self.assets[tile['type']][tile['variant']]
                    tile_r = pygame.Rect(tile['pos'][0] - self.scroll[0], tile['pos'][1] - self.scroll[1], tile_img.get_width(), tile_img.get_height())
                    if tile_r.collidepoint(mpos):
                        self.tilemap.offgrid_tiles.remove(tile)
            self.display.blit(current_tile_img, (5, 5)) #this will blit the image to the display
            for event in pygame.event.get():  
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit() #this will exit the game

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.clicking = True #this will set the clicking variable to true
                        if not self.on_grid:
                            self.tilemap.offgrid_tiles.append({'type': self.tile_list[self.tile_group], 'variant': self.tile_variant, 'pos': (mpos[0] + self.scroll[0], mpos[1] + self.scroll[1])}) #this will set the tile type and variant to the tile position
                    if event.button == 3:
                        self.right_clicking = True
                    if self.shift:
                        if event.button == 4:
                            self.tile_variant = (self.tile_variant - 1) % len(self.assets[self.tile_list[self.tile_group]]) #this will change the tile variant to the next one
                        if event.button == 5:
                            self.tile_variant = (self.tile_variant + 1) % len(self.assets[self.tile_list[self.tile_group]]) #this will change the tile variant to the next one
                    else:
                        if event.button == 4:
                            self.tile_group = (self.tile_group - 1) % len(self.tile_list) #this will change the tile group to the next one
                            self.tile_variant = 0
                        if event.button == 5:
                            self.tile_group = (self.tile_group + 1) % len(self.tile_list) #this will change the tile group to the next one
                            self.tile_variant = 0
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.clicking = False
                    if event.button == 3:
                        self.right_clicking = False
                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_a:
                        self.movement[0] = True
                    if event.key == pygame.K_d:
                        self.movement[1] = True #this will move the image to the right
                    if event.key == pygame.K_w :
                        self.movement[2] = True
                    if event.key == pygame.K_s :
                        self.movement[3] = True
                    if event.key == pygame.K_g:
                        self.on_grid = not self.on_grid
                    if event.key == pygame.K_t:
                        self.tilemap.autotile()
                    if event.key == pygame.K_o:
                        self.tilemap.save('map.json') #this will save the tilemap to a file
                    if event.key == pygame.K_LSHIFT:
                        self.shift = True #this will set the shift variable to true
                                     
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_d:
                        self.movement[1] = False            
                    if event.key == pygame.K_w :
                        self.movement[2] = False
                    if event.key == pygame.K_s :
                        self.movement[3] = False
                    if event.key == pygame.K_LSHIFT:
                        self.shift = False #this will set the shift variable to false
                        
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0)) #this will scale the display to the screen size
            pygame.display.update()
            self.clock.tick(60) #this will make the game run at 60 frames per second

Editor().run() #this will run the editor       