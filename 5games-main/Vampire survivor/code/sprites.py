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
        self.gun_surface = pygame.image.load(join('images', 'gun', 'gun.png')).convert_alpha()
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
            # rotate gun properly when right of the player at 5:41:19
            angle = -angle
            self.image = pygame.transform.rotozoom(self.gun_surface,angle,1)
            self.image = pygame.transform.flip(self.image, False, True)
        
    def update(self,dt):
        self.get_direction()
        self.rotate_gun()
        self.rect.center = self.player.rect.center + self.player_direction * self.distance

class Bullet(pygame.sprite.Sprite):
    def __init__(self,surface,pos,direction,groups):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_frect(center = pos)
        self.direction = direction
        self.speed = 1200
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = 1000

    def update(self,dt):
        self.rect.center += self.direction * self.speed * dt
        if pygame.time.get_ticks() - self.spawn_time >= self.lifetime:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self,pos,frames,groups,player,collision_sprites):
        super().__init__(groups)
        self.player = player

        # create the image
        self.frames = frames
        self.frames_index = 0
        self.image = self.frames[self.frames_index]
        self.animation_speed = 6

        #rect
        self.rect = self.image.get_frect(center = pos)
        self.hitbox_rect = self.rect.inflate(-20,-40)
        self.collision_sprites = collision_sprites
        self.direction = pygame.Vector2()
        self.speed = 350

        #timer
        self.death_time = 0
        self.death_duration = 100

    def animate(self,dt):
        self.frames_index += self.animation_speed * dt
        self.image = self.frames[int(self.frames_index) % len(self.frames)]
    

    def move(self, dt):
        # get enemy direction
        player_pos = pygame.Vector2(self.player.rect.center)
        enemy_pos = pygame.Vector2(self.rect.center)
        self.direction = (player_pos - enemy_pos).normalize()

        # update movement of rect
        self.hitbox_rect.x += self.direction.x * self.speed * dt
        # after horizontal movement, call collisions with the hiorizonatal collisions
        self.collision('horizontal')
        self.hitbox_rect.y += self.direction.y * self.speed * dt
        # same thing, vertical
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
    
    def destroy(self):
        # start a timer for death of sprite of enemy
        self.death_time = pygame.time.get_ticks()

        # change the image to white
        surf = pygame.mask.from_surface(self.frames[0]).to_surface()
        surf.set_colorkey('black')
        self.image = surf

    def death_timer(self):
        if pygame.time.get_ticks() - self.death_time >= self.death_duration:
            self.kill()

    def update(self,dt):
        if self.death_time == 0:
            self.move(dt)
            self.animate(dt)
        else:
            self.death_timer()
