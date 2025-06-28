from pickle import OBJ
from pygame import Vector2
from settings import *

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.Vector2()

    def draw(self, target_pos):
        self.offset.x = -(target_pos[0] - WINDOW_WIDTH / 2) #camera
        self.offset.y = -(target_pos[1] - WINDOW_HEIGHT / 2) #camera

        ground_sprites = [sprite for sprite in self if hasattr(sprite, 'ground')]
        object_sprites = [sprite for sprite in self if not hasattr(sprite, 'ground')] 
        for layer in [ground_sprites,object_sprites]: # ground being before object important to allow the body to not be half cut off!
            for sprite in sorted(layer, key = lambda sprite: sprite.rect.centery): # this allows things to look good by sorting by y and thus having objects view differently by y level
                self.display_surface.blit(sprite.image,sprite.rect.topleft + self.offset)