from settings import *

class Player (pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)
        # edited from the tutorial, added 'Vampire survivor', 
        self.image = pygame.image.load(join('Vampire survivor', 'images', 'player', 'down', '0.png')).convert_alpha()
        self.rect = self.image.get_frect(center = pos)
        self.hitbox_rect = self.rect.inflate(-60,0) # makes it so that it looks pixel perfect without having to use a mask

        # movement
        self.direction = pygame.Vector2(1,0)
        self.speed = 500

        self.collision_sprites = collision_sprites

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
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

    def update(self, dt):
        self.input()
        self.move(dt)

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
