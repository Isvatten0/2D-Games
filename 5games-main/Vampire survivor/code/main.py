from turtle import window_height
from settings import *
from player import Player
from sprites import *
from random import randint
from pytmx.util_pygame import load_pygame
from groups import AllSprites

class Game:
    def __init__(self):
        # initial setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
        pygame.display.set_caption('Vampire Survival')
        self.clock = pygame.time.Clock()
        self.running = True
        # groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.setup()

        # sprites
        self.player = Player((400,300), self.all_sprites, self.collision_sprites) # Here we are only adding the player to the first group, but giving the player aone more arguement and the player is not in the group only has acces to it so the player does not colllide with itself
        #for i in range(7):
           # x,y = randint(0,WINDOW_WIDTH),randint(0,WINDOW_HEIGHT)
           # z = randint(0,300)
           # self.box = CollisionSprite((x,y), (z,z), (self.all_sprites, self.collision_sprites)) # Here we are adding the sprite to two groups as oppose to above

    def setup(self):
        map = load_pygame(join('Vampire survivor', 'data', 'maps', 'world.tmx'))

        for x,y,image in map.get_layer_by_name('Ground').tiles():
            Sprite((x * TILE_SIZE,y * TILE_SIZE),image,self.all_sprites)

        for objects in map.get_layer_by_name('Objects'): # this function is the most common way to get a layer
            CollisionSprite((objects.x,objects.y),objects.image,(self.all_sprites,self.collision_sprites))

        for collisions in map.get_layer_by_name('Collisions'):
            CollisionSprite((collisions.x,collisions.y), pygame.Surface((collisions.width,collisions.height)),self.collision_sprites)
    def run(self):
        while self.running:
            # delta time
            dt = self.clock.tick() / 1000
            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # update method
            self.all_sprites.update(dt)

            # draw 
            self.display_surface.fill('black')
            self.all_sprites.draw(self.player.rect.center)
            pygame.display.update()
        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()