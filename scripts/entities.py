import pygame

class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game 
        self.type = e_type 
        self.pos = list(pos) 
        self.size = size 
        self.velocity = [0, 0] 
        self.collision = { 'up': False, 'down': False, 'right': False, 'left': False}

        self.action = ''
        self.anim_offset = (-3, -3)
        self.flip = False
        self.set_action('idle') #this will set the action to idle
        self.last_movement = [0, 0]
        
        
    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.game.assets[self.type + '/' + self.action].copy() #this will copy the animation of the player

    def update(self, tilemap, movement = (0, 0)):
        self.collision = { 'up': False, 'down': False, 'right': False, 'left': False} #this will reset the collision
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

        if movement[0] > 0:
            self.flip = False
        if movement[0] < 0:
            self.flip = True

        self.last_movement = movement
        

        self.velocity[1] = min(5, self.velocity[1] + 0.1) #this will help us to determine how fast the char is falling

        if self.collision['down'] or self.collision['up']:
            self.velocity[1] = 0

            self.animation.update()

    def render(self, surf, offset = (0, 0)):
        surf.blit(pygame.transform.flip(self.animation.img(), self.flip, False),(self.pos[0] - offset[0] + self.anim_offset[0], self.pos[1] - offset[1] + self.anim_offset[1])) #this will render the player to the screen

class Player(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, 'player', pos, size) #this will call the constructor of the parent class
        self.air_time = 0
        self.jumps = 1
        self.wall_slide = False

        

    def update(self, tilemap, movement=(0, 0)):
        super().update(tilemap, movement = movement)

        self.air_time += 1
        if self.collision['down']:
            self.air_time = 0
            self.jumps = 1
        
        self.wall_slide = False


        if (self.collision['right'] or self.collision['left']) and self.air_time  > 4:
            self.wall_slide = True
            self.velocity[1] = min(self.velocity[1], 0.5)
            if self.collision['right']:
                self.flip = False
            else:
                self.flip = True
            self.set_action('wall_slide')

        if not self.wall_slide:
            if self.air_time > 4:
                self.set_action('jump')
            elif movement[0] != 0:
                self.set_action('run')
            else:
                self.set_action('idle')

            

        if self.velocity[0] > 0:
            self.velocity[0] = max(self.velocity[0] - 0.1, 0)
        else:
            self.velocity[0] = min(self.velocity[0] + 0.1, 0)
           

    def jump(self):
        if self.wall_slide:
            if self.flip and self.last_movement[0] < 0:
                self.velocity[0] = 3.5
                self.velocity[1] = -2.5
                self.air_time = 5
                self.jumps = max(0, self.jumps - 1)
                return True
            elif not self.flip and self.last_movement[0] > 0:
                self.velocity[0] = -3.5
                self.velocity[1] = -2.5
                self.air_time = 5
                self.jumps = max(0, self.jumps - 1)
                return True
            
        elif self.jumps:
            self.velocity[1] = -3
            self.jumps -= 1
            self.air_time = 5
            return True
