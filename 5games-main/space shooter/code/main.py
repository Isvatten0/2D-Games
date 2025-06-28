import pygame
from os.path import join
from random import randint, uniform

class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join('..','images','Player2.png')).convert_alpha()
        # 8 bit self.image = pygame.transform.scale(pygame.image.load(join('..','images','8bitship.png')),(112,75)).convert_alpha()
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH/2,WINDOW_HEIGHT/2))
        self.direction = pygame.Vector2()
        self.speed = 300
        # cooldown
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 400

        # mask 
        self.mask = pygame.mask.from_surface(self.image)

    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks() 
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot = True
    def update(self, dt):
        keys = pygame.key.get_pressed()
        recent_keys = pygame.key.get_just_pressed()
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt
        if int(recent_keys[pygame.K_SPACE]) and self.can_shoot:
            Laser(laser_surf, self.rect.midtop, (all_sprites, laser_sprites))
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()
            laser_sound.play()

        self.laser_timer()

class Stars(pygame.sprite.Sprite):
    def __init__(self, groups, surf):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = (randint(0, WINDOW_WIDTH),randint(0, WINDOW_HEIGHT)))

class Laser(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom = pos)
        # self.mask = pygame.mask.from_surface(self.image) Unneeded since autocreated per docs
    
    def update(self, dt):
        self.rect.centery -= 400 * dt
        if self.rect.bottom < 0:
            self.kill()

class Meteor(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.original_image = surf
        self.image = self.original_image
        self.rect = self.image.get_frect(midtop = pos)
        self.rotation = 0
        self.rotation_speed = randint(50,200)
        self.spin = randint(1,2)
        self.start_time = pygame.time.get_ticks()
        self.lifetime = 3000
        self.direction = pygame.Vector2(uniform(-0.5,0.5),1)
        self.speed = randint(400,500)
        # self.mask = pygame.mask.from_surface(self.image) same as laser
    
    def update(self, dt):
        if self.spin == 1:
            self.rotation = (self.rotation + self.rotation_speed * dt) % 360
        else:
            self.rotation = (self.rotation - self.rotation_speed * dt) % 360
        
        # # Rotate the image
        self.image = pygame.transform.rotozoom(self.original_image, self.rotation, 1)
        # # Update the rect to keep the position centered
        self.rect = self.image.get_frect(center=self.rect.center)
        
        if pygame.time.get_ticks() - self.start_time >= self.lifetime:
            self.kill()
        self.rect.center += self.direction * self.speed * dt
        if self.rect.top >= WINDOW_HEIGHT:
            self.kill()

class AnimatedExplosion(pygame.sprite.Sprite):
    def __init__(self, frames, pos, groups):
        super().__init__(groups)
        self.frames = frames
        self.frames_index = 0
        self.image = self.frames[self.frames_index]
        self.rect = self.image.get_frect(center = pos)
        explosion_sound.play()
    def update(self, dt):
        self.frames_index += 20 * dt
        if self.frames_index < len(self.frames):
            self.image = self.frames[int(self.frames_index)]
        else:
            self.kill()

def collisions():
    global running
    collision_sprites = pygame.sprite.spritecollide(player, meteor_sprites, True, pygame.sprite.collide_mask)
    if collision_sprites:
        running = False
        explosion_sound.play()
        print("Ouch")

    for laser in laser_sprites:
        collided_sprites = pygame.sprite.spritecollide(laser, meteor_sprites, True)
        if collided_sprites:
            AnimatedExplosion(explosion_frames,laser.rect.midtop, all_sprites)  
            laser.kill()  
               

def display_score(start_time):
    current_time = pygame.time.get_ticks() // 1000
    text_surf = font.render(str(current_time - start_time),True, (158, 27, 50)) # Alabama Crimson (158, 27, 50)
    text_rect = text_surf.get_frect(midbottom = (WINDOW_WIDTH/2,WINDOW_HEIGHT - 40))
    display_surface.blit(text_surf,text_rect)
    pygame.draw.rect(display_surface, (158, 27, 50),text_rect.inflate(20,12).move(0,-6), 5,10)

# def display_end_screen():
    # display_surface.fill((0, 0, 0))  # Clear the display (choose your background color)

    # font = pygame.font.Font(None, 36)
    # play_again_text = font.render("Press SPACE to Play Again", True, (255, 255, 255))
    # quit_text = font.render("Press any other key to Quit", True, (255, 255, 255))

    # play_again_rect = play_again_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
    # quit_rect = quit_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))

    # display_surface.blit(play_again_text, play_again_rect)
    # display_surface.blit(quit_text, quit_rect)

    # pygame.display.update()


def game():
    global running
    running = True
    start_time = pygame.time.get_ticks() // 1000
    while running:
        # Frame Rate
        dt = clock.tick() / 1000
        # event loop
        for event in pygame.event.get(): # checks for keyboard/mouse,timers/ui interactions / user wants to close game
            if event.type == pygame.QUIT:
                running = False
                
            if event.type == meteor_event:
                x,y = randint(20,WINDOW_WIDTH),randint(-200, -100)
                Meteor(meteor_surf,(x,y),(all_sprites, meteor_sprites))

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        all_sprites.update(dt)
        collisions()
            #implement a life logic

        # draw background
        display_surface.blit(background,(0,0),((0,0),(WINDOW_WIDTH, WINDOW_HEIGHT)))

        # draw score (time based)
        display_score(start_time)

        # draw sprites
        all_sprites.draw(display_surface)

        pygame.display.update() 



    # display_end_screen()
    # waiting_for_input = True
    # while waiting_for_input:
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             pygame.quit()
    #         elif event.type == pygame.KEYDOWN:
    #             if event.key == pygame.K_SPACE:
    #                 # Restart the game (implement your logic here)
    #                 waiting_for_input = False
    #                 running = True
    #             else:
    #                 # Quit the game
    #                 pygame.quit()
    # pygame.quit()


def main_menu():
    while True:
        display_surface.fill((0,0,0))
        
        x, y = pygame.mouse.get_pos()

        text_surf = font.render("Play",True, (158, 27, 50)) # Alabama Crimson (158, 27, 50)
        text_rect = text_surf.get_frect(midbottom = (int(WINDOW_WIDTH/4),WINDOW_HEIGHT/2))
        display_surface.blit(text_surf,text_rect)
        if text_rect.collidepoint((x,y)):
            if click == True:
                game()
        pygame.draw.rect(display_surface, (158, 27, 50),text_rect.inflate(20,12).move(0,-6), 5,10)

        text_surf = font.render("Exit",True, (158, 27, 50)) # Alabama Crimson (158, 27, 50)
        text_rect = text_surf.get_frect(midbottom = (int(WINDOW_WIDTH/4),WINDOW_HEIGHT/2 + 120))
        display_surface.blit(text_surf,text_rect)
        if text_rect.collidepoint((x,y)):
            if click == True:
                pygame.quit()
        pygame.draw.rect(display_surface, (158, 27, 50),text_rect.inflate(20,12).move(0,-6), 5,10)


        click = False
        for event in pygame.event.get(): # checks for keyboard/mouse,timers/ui interactions / user wants to close game
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        
        pygame.display.update() 

# setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280,720
pygame.display.set_caption("Space Shooter")
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
running = True
clock = pygame.time.Clock()
click = False
# imports
background = pygame.transform.scale(pygame.image.load(join('..','images','Space Background.png')),(WINDOW_WIDTH, WINDOW_HEIGHT)).convert_alpha()
star_surf = pygame.transform.scale(pygame.image.load(join('..','images','star.png')),(randint(8,14),randint(8,14))).convert_alpha()
laser_surf = pygame.image.load(join('..','images','laser.png')).convert_alpha()
meteor_surf = pygame.image.load(join('..','images','meteor.png')).convert_alpha()
font = pygame.font.Font(join('..','images','Oxanium-Bold.ttf'), 40) # Dafont.com for different fonts
explosion_frames = [pygame.image.load(join('..','images','explosion',f'{i}.png')).convert_alpha() for i in range(21)]
laser_sound = pygame.mixer.Sound(join('..', 'audio', 'laser.wav'))
laser_sound.set_volume(0.1)
explosion_sound = pygame.mixer.Sound(join('..', 'audio', 'explosion.wav'))
explosion_sound.set_volume(0.1)
game_sound = pygame.mixer.Sound(join('..', 'audio', 'game_music.wav'))
game_sound.set_volume(0.1)
game_sound.play(loops = -1)
damage_sound = pygame.mixer.Sound(join('..', 'audio', 'damage.ogg'))
damage_sound.set_volume(1)

# sprites
all_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()
for i in range(20):
    Stars(all_sprites, star_surf)
player = Player(all_sprites)

# meteor event
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event,500)
main_menu()


