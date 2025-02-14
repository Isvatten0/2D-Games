from settings import *

class CollisionSprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        # self.image = pygame.Surface(size) old
        self.image = surf
       # self.image.fill('blue')
        self.rect = self.image.get_frect(center = pos)