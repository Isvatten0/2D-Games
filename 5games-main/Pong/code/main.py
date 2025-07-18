from settings import * 

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
        pygame.display.set_caption("Pong Classic")
        self.clock = pygame.time.Clock()
        self.running = True

    def run(self):
        while self.running:
            # Setup delta time. Get Ticks then divide by 1000 get dt in miliseconds
            dt = self.clock.tick() / 1000

            # Set Up the game condition, so the game can exit
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Update the game logic
            
            # Draw the game
            self.display_surface.fill(COLORS['bg'])
            pygame.display.update()  # Can use flip as well

        pygame.quit()
 
if __name__ == '__main__':
    game = Game()
    game.run()