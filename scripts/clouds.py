import random

class Cloud:
    def __init__(self, pos, img, speed, depth):
        self.pos = list(pos)
        self.img = img
        self.speed = speed
        self.depth = depth  

    def update(self):
        self.pos[0] += self.speed

    def render(self, surf, offset=(0, 0)):
        render_pos = (self.pos[0] - offset[0] * self.depth, self.pos[1] - offset[1] * self.depth)  #this is a tuple of (x, y, z) coordinates for 3D rendering    
        surf.blit(self.img, (render_pos[0] % (surf.get_width() + self.img.get_width() - self.img.get_width()),(render_pos[1] % (surf.get_height() + self.img.get_height() - self.img.get_height()))))  # this is a tuple of (x, y) coordinates for 2D rendering

class Clouds:
    def __init__(self, cloud_images, count=16):
        self.clouds = []

        for i in range(count):
            self.clouds.append(Cloud((random.random() * 99999, random.random() * 99999), random.choice(cloud_images), random.random() * 0.2 + 0.2, random.random() * 0.4 + 0.2)) # this is a tuple of (x, y, z) coordinates for 3D rendering
            self.clouds.sort(key=lambda x: x.depth)  # sort clouds by depth
  
    def update(self):
        for cloud in self.clouds:
            cloud.update()

    def render(self, surf, offset=(0, 0)):  
        for cloud in self.clouds:
            cloud.render(surf, offset = offset)  # this is a tuple of (x, y) coordinates for 2D rendering