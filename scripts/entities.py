import pygame

class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game 
        self.type = e_type 
        self.pos = list(pos) 
        self.size = size 
        self.velocity = [0, 0] 

        
    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])


    def update(self, tilemap, movement = (0, 0)):
        self.collision = {'up': False, 'down': False, 'left': False, 'right': False} #this will help us to determine if the char is colliding with something

        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1]) #this will help us to determine how the char in that frame

        self.pos[0] += frame_movement[0]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0:
                    entity_rect.right = rect.left
                    self.collision['right'] = True
                if frame_movement[0] < 0:
                    entity_rect.left = rect.right
                    self.collision['left'] = True
                self.pos[0] = entity_rect.x

        self.pos[1] += frame_movement[1]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collision['down'] = True
                if frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collision['up'] = True
                self.pos[1] = entity_rect.y

        self.velocity[1] = min(5, self.velocity[1] + 0.1) #this will help us to determine how fast the char is falling

        if self.collision['down'] or self.collision['up']:
            self.velocity[1] = 0

    def render(self, surf, offset = (0, 0)):
        surf.blit(self.game.assets['player'], (self.pos[0] - offset[0], self.pos[1] - offset[1])) #this will render the player to the screen