from queue import Full
from turtle import back, window_height
from settings import *
from player import Player
from sprites import *
from random import randint
from pytmx.util_pygame import load_pygame
from groups import AllSprites
from random import choice

class Game:
    def __init__(self):
        # initial setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
        pygame.display.set_caption('Vampire Survival')
        self.clock = pygame.time.Clock()
        self.running = True

        # enemy timer
        self.enemy_event = pygame.event.custom_type()
        pygame.time.set_timer(self.enemy_event, 300)
        self.spawn_positions = []

        # groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()


        # timer for the gun
        self.can_shoot = True
        self.bullet_shoot_time = 0
        self.cooldown_duration = 100

        # audio
        self.background_music = pygame.mixer.Sound(join('audio','music.wav'))
        self.background_music.set_volume(0.1)
        self.shoot_sound = pygame.mixer.Sound(join('audio','shoot.wav'))
        self.shoot_sound.set_volume(0.2)
        self.impact_sound = pygame.mixer.Sound(join('audio','impact.ogg'))
        self.impact_sound.set_volume(0.2)

        # setup
        self.load_images()
        self.setup()       
        



        # sprites
        #self.player = Player((400,300), self.all_sprites, self.collision_sprites) # Here we are only adding the player to the first group, but giving the player aone more arguement and the player is not in the group only has acces to it so the player does not colllide with itself
        #for i in range(7):
           # x,y = randint(0,WINDOW_WIDTH),randint(0,WINDOW_HEIGHT)
           # z = randint(0,300)
           # self.box = CollisionSprite((x,y), (z,z), (self.all_sprites, self.collision_sprites)) # Here we are adding the sprite to two groups as oppose to above
    
    def bullet_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks() 
            if current_time - self.bullet_shoot_time >= self.cooldown_duration:
                self.can_shoot = True

    def load_images(self):
        self.bullet_surf = pygame.image.load(join('images', 'gun', 'bullet.png')).convert_alpha()

        folders = list(walk(join('images', 'enemies')))[0][1]
        self.enemy_frames = {}
        for folder in folders:
            # print(folder)
            for folder_path, _, file_names in walk(join('images', 'enemies', folder)):
                self.enemy_frames[folder] = []
                for file_name in sorted(file_names, key = lambda name: int(name.split('.')[0])):
                    full_path = join(folder_path,file_name)
                    surface = pygame.image.load(full_path).convert_alpha()
                    self.enemy_frames[folder].append(surface)
        # print(self.enemy_frames)

    def input(self):
       if pygame.mouse.get_pressed()[0] and self.can_shoot == True:
           # print('shoot')
           pos = self.gun.rect.center + self.gun.player_direction * 40
           Bullet(self.bullet_surf, pos, self.gun.player_direction, (self.all_sprites,self.bullet_sprites))
           self.shoot_sound.play()
           self.can_shoot = False
           self.bullet_shoot_time = pygame.time.get_ticks()

    def setup(self):
        map = load_pygame(join('data', 'maps', 'world.tmx'))

        for x,y,image in map.get_layer_by_name('Ground').tiles():
            Sprite((x * TILE_SIZE,y * TILE_SIZE),image,self.all_sprites)

        for objects in map.get_layer_by_name('Objects'): # this function is the most common way to get a layer
            CollisionSprite((objects.x,objects.y),objects.image,(self.all_sprites,self.collision_sprites))

        for collisions in map.get_layer_by_name('Collisions'):
            CollisionSprite((collisions.x,collisions.y), pygame.Surface((collisions.width,collisions.height)),self.collision_sprites)

        for entity in map.get_layer_by_name('Entities'):
            if entity.name == 'Player':
                self.player = Player((entity.x,entity.y), self.all_sprites, self.collision_sprites)
                self.gun = Gun(self.player, self.all_sprites)
            else:
                self.spawn_positions.append((entity.x,entity.y))

        self.background_music.play()

    def bullet_collision(self):
        if self.bullet_sprites:
            for bullet in self.bullet_sprites:
                # collision_sprites = pygame.sprite.spritecollide(sprite,group, dokill)
                collision_sprites = pygame.sprite.spritecollide(bullet,self.enemy_sprites, False, pygame.sprite.collide_mask)
                if collision_sprites:
                    self.impact_sound.play()
                    for sprite in collision_sprites:
                        sprite.destroy()
                    bullet.kill()

    def player_collision(self):
        if pygame.sprite.spritecollide(self.player,self.enemy_sprites, False,pygame.sprite.collide_mask):
            self.running = False
                
    def run(self):
        while self.running:
            # delta time
            dt = self.clock.tick() / 1000
            # event loop
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == self.enemy_event:
                    Enemy(choice(self.spawn_positions),choice(list(self.enemy_frames.values())),(self.all_sprites,self.enemy_sprites),self.player,self.collision_sprites)

            # update method
            self.bullet_timer()
            self.input()
            self.all_sprites.update(dt)
            self.bullet_collision()
            self.player_collision()
            

            # draw 
            self.display_surface.fill('black')
            self.all_sprites.draw(self.player.rect.center)
            pygame.display.update()

            # test bullet sprites
            # print(self.bullet_sprites)
        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()