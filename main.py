import pygame
from pygame.locals import *
import time
import random

# Constants
SIZE = 40
BACKGROUND_COLOR = (110, 110, 5)

class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("Resources/apple.jpg").convert()
        self.x = 120
        self.y = 120

    def draw(self):
        """Draw the apple on the screen."""
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        """Move apple to a new random position on the screen."""
        self.x = random.randint(1, 24) * SIZE
        self.y = random.randint(1, 19) * SIZE


class Snake:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("Resources/block.jpg").convert()
        self.direction = 'down'
        self.length = 1
        self.x = [SIZE]
        self.y = [SIZE]

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def walk(self):
        """Move the snake in the current direction."""
        # Update body positions to follow the head
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        # Update head position
        if self.direction == 'left':
            self.x[0] -= SIZE
        elif self.direction == 'right':
            self.x[0] += SIZE
        elif self.direction == 'up':
            self.y[0] -= SIZE
        elif self.direction == 'down':
            self.y[0] += SIZE

        self.draw()

    def draw(self):
        """Draw the snake on the screen."""
        for i in range(self.length):
            self.parent_screen.blit(self.image, (self.x[i], self.y[i]))
        pygame.display.flip()

    def increase_length(self):
        """Increase the length of the snake by one."""
        self.length += 1
        self.x.append(-1)  # Add new segment with placeholder values
        self.y.append(-1)


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Tirth's game ")
        
        # Initialize sound and background music
        pygame.mixer.init()
        self.play_background_music()

        # Set up screen and game objects
        self.surface = pygame.display.set_mode((1000, 800))
        self.snake = Snake(self.surface)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def play_background_music(self):
        """Play background music in a loop."""
        pygame.mixer.music.load('Resources/bg_music_1.mp3')
        pygame.mixer.music.play(-1, 0)

    def play_sound(self, sound_name):
        """Play a sound effect based on the action."""
        sound = pygame.mixer.Sound(f"Resources/{sound_name}.mp3")
        pygame.mixer.Sound.play(sound)

    def reset(self):
        """Reset the game to initial state."""
        self.snake = Snake(self.surface)
        self.apple = Apple(self.surface)
        self.snake.draw()
        self.apple.draw()

    def is_collision(self, x1, y1, x2, y2):
        """Check if two positions collide."""
        return x1 == x2 and y1 == y2

    def render_background(self):
        """Render the background image."""
        bg = pygame.image.load("Resources/background.jpg")
        self.surface.blit(bg, (0, 0))

    def play(self):
        """Main gameplay logic including drawing and collision checking."""
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        # Check for collision with the apple
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound("ding")
            self.snake.increase_length()
            self.apple.move()

        # Check for collision with the snake's own body
        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound('crash')
                raise Exception("Collision Occurred")

        # Check for collision with the boundaries
        if (self.snake.x[0] < 0 or self.snake.x[0] >= 1000 or 
            self.snake.y[0] < 0 or self.snake.y[0] >= 800):
            self.play_sound('crash')
            raise Exception("Collision with boundary")

    def display_score(self):
        """Display the current score on the screen."""
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"Score: {self.snake.length}", True, (200, 200, 200))
        self.surface.blit(score, (850, 10))

    def show_game_over(self):
        """Display the game over screen and options to restart or exit."""
        self.render_background()
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"Game is over! Your score is {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(line1, (200, 300))
        line2 = font.render("To play again press Enter. To exit press Escape!", True, (255, 255, 255))
        self.surface.blit(line2, (200, 350))
        pygame.mixer.music.pause()
        pygame.display.flip()

    def run(self):
        """Run the main game loop."""
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    elif event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False

                    if not pause:
                        if event.key == K_LEFT:
                            self.snake.move_left()
                        elif event.key == K_RIGHT:
                            self.snake.move_right()
                        elif event.key == K_UP:
                            self.snake.move_up()
                        elif event.key == K_DOWN:
                            self.snake.move_down()

                elif event.type == QUIT:
                    running = False

            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()
                time.sleep(1)  # Delay to prevent immediate restart

            time.sleep(0.1)  # Increased game speed


if __name__ == '__main__':
    game = Game()
    game.run()
    