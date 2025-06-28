from pygame import Vector2, mouse
from settings import *
from math import atan2,degrees

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf,groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)
        self.ground = True

class CollisionSprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        # self.image = pygame.Surface(size) old
        self.image = surf
       # self.image.fill('blue')
        self.rect = self.image.get_frect(topleft = pos)

class Gun(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        self.player = player
        self.distance = 140
        self.player_direction = pygame.Vector2(0,1)

        # setup the sprite
        super().__init__(groups)
        self.gun_surface = pygame.image.load(join('Vampire survivor', 'images', 'gun', 'gun.png')).convert_alpha()
        self.image = self.gun_surface
        self.rect = self.image.get_frect(center =self.player.rect.center + self.player_direction * self.distance)
    
    def get_direction(self):
        mouse_pos = pygame.Vector2((pygame.mouse.get_pos()))
        player_pos = pygame.Vector2((WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.player_direction = (mouse_pos - player_pos).normalize()

    def rotate_gun(self):
        angle = degrees(atan2(self.player_direction.x,self.player_direction.y)) - 90
        if self.player_direction.x > 0:
            self.image = pygame.transform.rotozoom(self.gun_surface,angle,1)
        else:
            # rotate gun properly when right of the player at 5:34:43
            angle = -angle
            self.image = pygame.transform.rotozoom(self.gun_surface,angle,1)
            self.image = pygame.transform.flip(self.image, False, True)
        
    def update(self,dt):
        self.get_direction()
        self.rotate_gun()
        self.rect.center = self.player.rect.center + self.player_direction * self.distance