from queue import Full
from settings import *

class Player (pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)
        # edited from the tutorial, added 'Vampire survivor', 
        self.load_images() # must be before self.image
        self.state, self.frame_index =  'down', 0
        self.image = pygame.image.load(join('Vampire survivor', 'images', 'player', 'down', '0.png')).convert_alpha()
        self.rect = self.image.get_frect(center = pos)
        self.hitbox_rect = self.rect.inflate(-60,-100) # makes it so that it looks pixel perfect without having to use a mask

        # movement
        self.direction = pygame.Vector2(1,0)
        self.speed = 500

        self.collision_sprites = collision_sprites

    def load_images(self):
        self.frames = {'left': [],'right': [],'up': [],'down': []} # must match folders where animation is held

        for state in self.frames.keys():
            for folder_path, sub_folders, file_names in walk(join('Vampire survivor','images','player',state)):
                if file_names:
                    for file_name in sorted(file_names, key= lambda name: int(name.split('.')[0])):
                        full_path = join(folder_path, file_name)
                        surf = pygame.image.load(full_path).convert_alpha()
                        self.frames[state].append(surf)
        # print(self.frames)

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT] or keys[pygame.K_d]) - int(keys[pygame.K_LEFT] or keys[pygame.K_a])
        # if self.direction.x > 0 and self.direction.y == 0 :
        #    self.image = pygame.image.load(join('Vampire survivor', 'images', 'player', 'right', '0.png')).convert_alpha()
        # if self.direction.x < 0 and self.direction.y == 0 :
        #    self.image = pygame.image.load(join('Vampire survivor', 'images', 'player', 'left', '0.png')).convert_alpha()
        # if self.direction.y < 0:
        #    self.image = pygame.image.load(join('Vampire survivor', 'images', 'player', 'up', '0.png')).convert_alpha()
        # if self.direction.y > 0:
        #    self.image = pygame.image.load(join('Vampire survivor', 'images', 'player', 'down', '0.png')).convert_alpha()
        
        self.direction.y = int(keys[pygame.K_DOWN] or keys[pygame.K_s]) - int(keys[pygame.K_UP] or keys[pygame.K_w])
        if self.direction:
            self.direction = self.direction.normalize()
        else:
            self.direction = self.direction

    def move(self,dt):
        #self.rect.x += self.direction.x * dt * self.speed
        self.hitbox_rect.x += self.direction.x * dt * self.speed
        self.collision('horizontal')
        #self.rect.y += self.direction.y * dt * self.speed
        self.hitbox_rect.y += self.direction.y * dt * self.speed
        self.collision('vertical')
        self.rect.center = self.hitbox_rect.center

    def collision(self, direction):
        # if direction move back opposite direction
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if direction == 'horizontal':
                    if self.direction.x > 0:
                        self.hitbox_rect.right = sprite.rect.left
                    if self.direction.x < 0:
                        self.hitbox_rect.left = sprite.rect.right
                if direction == 'vertical':
                    if self.direction.y > 0:
                        self.hitbox_rect.bottom = sprite.rect.top
                    if self.direction.y < 0:
                        self.hitbox_rect.top = sprite.rect.bottom

    def animate(self, dt):
        # get the state
        if self.direction.x > 0: self.state = 'right'
        elif self.direction.x < 0: self.state = 'left'
        elif self.direction.y > 0: self.state = 'down'
        elif self.direction.y < 0: self.state = 'up'
        # thoughts if self.direction.y < 0 AND self.direction.x > 0: self.state = 'diagonalup' 
        # then I would add to others the opposite direction is equal to 0

        # animate 
        self.frame_index = self.frame_index + (5 * dt) if self.direction else 0
        self.image = self.frames[self.state][int(self.frame_index) % len(self.frames[self.state])]

    def update(self, dt):
        self.input()
        self.move(dt)
        self.animate(dt)